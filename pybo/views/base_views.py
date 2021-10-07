from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q, Count
# from django.http import HttpResponse

from ..models import Question


# Create your views here.


# generic view를 이용한 클래스
# 단순한 모델의 목록 조회나 상세 조회는 간단하게 구현이 가능하나, 복잡한 문제를 해결할 때
# 오히려 개발 난이도를 높이는 경우도 있으므로 주의해야 한다
class IndexView(generic.ListView):
    """
    pybo 목록 출력
    """
    def get_queryset(self):
        return Question.objects.order_by('-create_date')


def index(request):
    """
    pybo 목록 출력
    """
    # 입력인자
    page = request.GET.get('page', '1')     # 페이지
    kw = request.GET.get('kw', '')          # 검색어
    so = request.GET.get('so', 'recent')    # 정렬 기준

    # 정렬
    # order_by() 인자에 '-'가 붙어있으므로 역순으로 정렬하게 된다
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:   # recent
        question_list = Question.objects.order_by('-create_date')

    # 조회
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |                  # 제목 검색
            Q(content__icontains=kw) |                  # 내용 검색
            Q(author__username__icontains=kw) |         # 질문 글쓴이 검색
            Q(answer__content__icontains=kw) |          # 답변 내용 검색
            Q(answer__author__username__icontains=kw)   # 답변 글쓴이 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw}

    # page 요청에 대한 응답을 위해 HttpResponse()를 사용
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}

    return render(request, 'pybo/question_detail.html', context)
