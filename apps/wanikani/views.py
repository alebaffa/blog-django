from django.shortcuts import render

from .services import get_stats


def stats(request):
    error = None
    wanikani_stats = {}

    try:
        wanikani_stats = get_stats()
    except Exception as e:  # pylint: disable=broad-exception-caught
        error = str(e)

    return render(
        request,
        "wanikani/stats.html",
        {
            "stats": wanikani_stats,
            "error": error,
        },
    )
