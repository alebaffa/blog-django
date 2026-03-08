from django.urls import path

from . import views

app_name = "wanikani"

urlpatterns = [
    path("", views.stats, name="stats"),
]
