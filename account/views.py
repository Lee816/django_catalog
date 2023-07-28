from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

# Create your views here.


def user_login2(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )  # authenticate() 메서드를 사용해 데이터베이스에 대해 인증 성공적으로 인증하면 User 객체를 반환, 그렇지 않으면 None을 반환
            if user is not None:
                if user.is_active:  # Django의 User 모델의 속성인 is_active 속성의 상태를 확인
                    login(
                        request, user
                    )  # authenticate()는 사용자 자격증명, login()은 현재 세션에 사용자를 설정
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "account/login2.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )  # authenticate() 메서드를 사용해 데이터베이스에 대해 인증 성공적으로 인증하면 User 객체를 반환, 그렇지 않으면 None을 반환
            if user is not None:
                if user.is_active:  # Django의 User 모델의 속성인 is_active 속성의 상태를 확인
                    login(
                        request, user
                    )  # authenticate()는 사용자 자격증명, login()은 현재 세션에 사용자를 설정
                    return redirect("account:dashboard")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("account:login")


@login_required  # 현재 사용자가 인증된 사용자인지 확인하는 데코레이터
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})
