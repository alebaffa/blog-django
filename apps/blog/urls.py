from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.post_list, name="list"),
    path("about/", views.about, name="about"),
    path("tags/<slug:slug>/", views.tag_detail, name="tag_detail"),
    path("<slug:slug>/", views.post_detail, name="detail"),
]
