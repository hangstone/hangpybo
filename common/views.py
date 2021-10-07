from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


# Create your views here.

def signup(request):
    """
    회원가입
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # cleaned_data.get() 는 회원가입 화면에서 입력한 값을 얻기 위해 사용하는 함수
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # 회원가입이 완료된 이후에 자동 로그인을 위해서 authenticate()와 login()를 호출
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()

    return render(request, 'common/signup.html', {'form': form})
