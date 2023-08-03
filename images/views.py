from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreateForm

# Create your views here.

# 로그인 상태여야 이미지를 등록 할 수 있다
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request,'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        # 초기 데이터를 get http 요청을 통해 제공되어야 폼의 인스턴스를 생성할 수 있다. 이 데이터는 외부 웹 사이트의 이미지의 url과 title 속성으로 구성된다.
        form = ImageCreateForm(data=request.GET)
    return render(request,'images/image/create.html',{'section':'iamges','form':form})