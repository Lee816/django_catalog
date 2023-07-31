from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())  # 패스워드타입 input을 사용하기위해


class UserRegistrationsForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:  # 두개의 비밀번호를 비교하고 다르면 에러 발생
            raise forms.ValidationError("Passwors don't match.")
        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(
            email=data
        ).exists():  # .exists() 메서드는 쿼리셋에 결과가 있으면 True 없으면 False를 반환
            raise forms.ValidationError("Email already in use.")
        return data


class UserEditForm(forms.ModelForm):  # 사용자의 이름과 이메일을 편집하는 폼
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)

        if qs.exists():
            raise forms.ValidationError("Email already in use.")
        return data


class ProfileEditForm(forms.ModelForm):  # 사용자의 확장모델의 생일과 프로필사진을 편집하는 폼
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]
