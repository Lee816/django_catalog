from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        # 사용자는 폼에서 직접 이미지 URL을 입력하지 않고 외부 사이트에서 아미지를 선택할 수있는 자바스크립트 도구를 사용
        widgets = {
            "url": forms.HiddenInput,
        }

    def clean_url(self):
        # url 필드의 값을 폼 인스턴스의 cleaned_data 사전에서 가져옴
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png"]
        # url 을 분할하여 확장명 검사
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                "The given URL does not match valid image extensions."
            )
        return url

    def save(self, force_insert=False, force_update=False, commit=False):
        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"
        # URL 에서 이미지 다운로드 (get요청을 보내서 이미지를 다운로드)
        response = requests.get(image_url)
        # 다운로드한 파일 내용으로 ContentFile 객체를 생성, 파일이 프로젝트의 미지어 디렉토리에 저장되며 데이터 베이스에는 저장하지 않는다.
        image.image.save(image_name, ContentFile(response.content), save=False)
        # commite 이 True 일때만 데이터베이스에 저장
        if commit:
            image.save()
        return image
