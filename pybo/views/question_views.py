from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


# Create your views here.


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # question.create_date에 값이 설정되어 있지 않으므로 에러가 발생한다
            # 그러므로 commit=False 인자를 주어 실제 data는 저장되지 않은 상태로 둔다
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            # create_date에 값이 설정되어 있으므로 이를 수행한다
            question.save()
            return redirect('pybo:index')
    else:   # request.method가 'get'인 경우
        form = QuestionForm()
    context = {'form': form}

    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == 'POST':
        # 현재 내용이 반영되도록 하기 위해서 question 객체를 넣도록 한다
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            # question.create_date에 값이 설정되어 있지 않으므로 에러가 발생한다
            # 그러므로 commit=False 인자를 주어 실제 data는 저장되지 않은 상태로 둔다
            question = form.save(commit=False)
            question.author = request.user
            # 수정 작업이므로 create_date를 제거하고, modified_date를 넣도록 한다
            question.modified_date = timezone.now()
            # create_date에 값이 설정되어 있으므로 이를 수행한다
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:   # request.method가 'get'인 경우
        # 기존 내용이 반영되도록 하기 위해서 question 객체를 넣도록 한다
        form = QuestionForm(instance=question)
    context = {'form': form}

    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    question.delete()

    return redirect('pybo:index')
