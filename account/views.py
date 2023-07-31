from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, UserRegistrationsForm, UserEditForm, ProfileEditForm
from .models import Profile

# Create your views here.


@login_required  # 현재 사용자가 인증된 사용자인지 확인하는 데코레이터
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationsForm(request.POST)
        if user_form.is_valid():
            # 새로운 사용자 객체를생성하지만 저장은 안함
            new_user = user_form.save(commit=False)
            # 선택한 비밀번호를 암호화(해싱) 저장
            new_user.set_password(user_form.cleaned_data["password"])
            # 객체 저장
            new_user.save()
            # 저장한 객체에 확장모델을 생성
            Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationsForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required  # 로그인되어 있는 상태여야함
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(
            instance=request.user, data=request.POST
        )  # 수정 대상이 되는 유저를 user_form 객체를 만들때 instance 인자로서 지정( 기존 유저의 정보를 넘겨줌 )
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )  # data는 text 정보를 files 는 file 정보를 다룬다
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("dashboard")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


class CustomLoginView(LoginView):  # 로그인시 로그인 화면이 출력되지 않게
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)
