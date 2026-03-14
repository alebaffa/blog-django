from django.urls import path

from . import views

app_name = "mastodon"

urlpatterns = [
    path("", views.feed, name="feed"),
]
