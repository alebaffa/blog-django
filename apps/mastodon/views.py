from django.shortcuts import render

from .services import get_statuses


def feed(request):
    error = None
    posts = []
    replies = []

    try:
        posts, replies = get_statuses()
    except Exception as e:  # pylint: disable=broad-exception-caught
        error = str(e)

    return render(
        request,
        "mastodon/feed.html",
        {
            "posts": posts,
            "replies": replies,
            "error": error,
        },
    )
