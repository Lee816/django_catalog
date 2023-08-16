from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
import redis

from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action
from mysite import settings

# Create your views here.

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

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
            create_action(request.user,'bookmarked image',new_image)
            messages.success(request,'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        # 초기 데이터를 get http 요청을 통해 제공되어야 폼의 인스턴스를 생성할 수 있다. 이 데이터는 외부 웹 사이트의 이미지의 url과 title 속성으로 구성된다.
        form = ImageCreateForm(data=request.GET)
    return render(request,'images/image/create.html',{'section':'iamges','form':form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views by 1
    # incr()명령은 주어진 키의 값을 1씩 증가 시키고 키가 존재하지 않는다면 incr 명령이 키를 생성한다.
    # incr()메서드는 작업을 수생한 후 키의 최종값을 반환한다.
    total_views = r.incr(f'image:{image.id}:views')
    # increment image ranking by 1
    # zincrby() 명령을 사용하여 image_ranking 이라는 정렬된 집합에 이미지 조회수를 저장
    # 이미지 ID와 관련된 점수로 1을 추가하고 이를 정렬된 집합의 해당 요소의 총 점수에 더한다.
    # 이를 통해 전역적으로 모든 이미지 조회수를 추적하고 총 조회수를 기준으로 정렬된 집합을 유지할 수있게 된다.
    r.zincrby('image_ranking',1,image.id)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images', 'image': image,'total_views':total_views})
    
@login_required
def image_ranking(request):
    # get image ranking dectionary
    # zrange() 명령을 사용하여 정렬된 집합의 요소를 가져온다.
    image_ranking = r.zrange('image_ranking',0,-1,desc=True)[:10]
    # 가져온 이미지 ID를 정수 리스트로 저장
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    # 해당 ID를 가진 image 객체를 가져와서 쿼리셋을 리스트로 변환
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    
    return render(request,'images/image/ranking.html',{'section':'images','most_viewed':most_viewed})
    
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user,'likes',image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})

@login_required
def image_list(request):
    # total_likes 필드를 이용한 좋아요수 정렬
    # images_by_popularity = Image.objects.annotate(likes=Count('users_like')).order_by('-likes')
    # or
    # images_by_popularity = Image.objects.order_by('-total_likes')
    
    images = Image.objects.all()
    paginator = Paginator(images,8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request, 'images/image/list_images.html', {'section':images,'images': images})
    return render(request, 'images/image/list.html', {'section':images,'images': images})