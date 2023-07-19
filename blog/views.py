from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import EmailPostForm, CommentForm

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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


def post_share(request, post_id):
    # id로 글 검색
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        # 폼 제출
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 폼 필드가 유효한 경우
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}님이 {post.title}을(를) 추천합니다."
            message = f"{post.title}을(를) 다음에서 읽어보세요.\n\n {cd['name']}의 의견 : {cd['comments']} \n\n {cd['name']}님의 email 주소 : {cd['email']}"
            send_mail(
                subject, message, f"{cd['name']}<1@1>", [cd["to"]]
            )  # cd['email] 불필요 구글 smtp 등로고딘 구글 계정만 보낸사람으로 나옴 email 칸에 아무리 다른걸 써도 smtp 구글 계정만 보낸사람으로 출력
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"
