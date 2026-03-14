from django.conf import settings

VALID_THEMES = {"slate", "warm-paper", "forest", "dark"}


def theme(request):
    active = getattr(settings, "BLOG_THEME", "slate")
    if active not in VALID_THEMES:
        active = "slate"
    return {
        "theme": active,
        "author_name": getattr(settings, "BLOG_AUTHOR_NAME", "Your Name"),
        "author_bio": getattr(settings, "BLOG_AUTHOR_BIO", ""),
    }
