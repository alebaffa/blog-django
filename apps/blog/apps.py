from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = "apps.blog"
    label = "posts"  # keeps existing migration history and DB table names intact
