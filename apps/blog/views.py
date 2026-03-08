from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post, Tag


def post_list(request):
    tag_slug = request.GET.get("tag")
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    active_tag = None

    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    tags = Tag.objects.filter(posts__status=Post.Status.PUBLISHED).distinct()
    return render(
        request,
        "posts/post_list.html",
        {
            "posts": posts,
            "tags": tags,
            "active_tag": active_tag,
        },
    )


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    return render(request, "posts/post_detail.html", {"post": post})


def about(request):
    return render(request, "pages/about.html")
