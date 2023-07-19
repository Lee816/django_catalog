from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post

# Create your views here.


# def post_list(request):
#     post_list = Post.published.all()
#     # 페이지당 3개의 게시물로 페이지네이션
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get("page", 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger or TypeError:
#         # page_number가 정수가 아닌 경우 첫 번째 페이지 제공
#         posts = paginator.page(1)
#     except EmptyPage:
#         # page_number가 범위를 벗어난 경우 결과의 마지막 페이지 제공
#         posts = paginator.page(paginator.num_pages)
#     return render(request, "blog/post/list.html", {"posts": posts})


# def post_detail(request, id):
#     try:
#         post = Post.published.get(id=id)
#     except Post.DoesNotExist:
#         raise Http404("No Post found.")
#     return render(request, "blog/post/detail.html", {"post": post})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"
