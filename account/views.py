from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationsForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from actions.utils import create_action
from actions.models import Action
# Create your views here.


@login_required  # 현재 사용자가 인증된 사용자인지 확인하는 데코레이터
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    
    if following_ids:
        # If user is following ohters, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user','user__profile').prefetch_related('target')[:10]
    return render(request, "account/dashboard.html", {"section": "dashboard",'actions':actions})


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
            create_action(new_user, 'has created an account')
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

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,'account/user/list.html',{'section':'people','users':users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User,username=username,is_active=True)
    return render(request,'account/user/detail.html',{'section':'people','user':user})

@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except user.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})