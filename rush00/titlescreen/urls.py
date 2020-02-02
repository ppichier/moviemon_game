from django.urls import path

from . import views

urlpatterns = [
    path("", views.titlescreen_f, name="titlescreen"),
]
