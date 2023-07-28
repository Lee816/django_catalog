from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserRegistrationsForm

# Create your views here.


@login_required  # 현재 사용자가 인증된 사용자인지 확인하는 데코레이터
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request):
    if request.method == "post":
        user_form = UserRegistrationsForm(request.POST)
        if user_form.is_valid():
            # 새로운 사용자 객체를생성하지만 저장은 안함
            new_user = user_form.save(commit=False)
            # 선택한 비밀번호를 암호화(해싱) 저장
            new_user.set_password(user_form.cleaned_data["password"])
            # 객체 저장
            new_user.save()
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationsForm()
    return render(request, "account/register.html", {"user_form": user_form})
