from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

# Create your views here.


@login_required  # 현재 사용자가 인증된 사용자인지 확인하는 데코레이터
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})
