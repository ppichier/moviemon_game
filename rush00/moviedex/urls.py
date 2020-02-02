from django.urls import path

from . import views

urlpatterns = [
    path('/', views.moviedex_f, name="moviedex"),
    path("/<moviedex_id>", views.press_a, name="press_a"),
    path("/direction/right", views.direction_moviedex_f, name="direction_moviedex_right"),
    path("/direction/left", views.direction_moviedex_f, name="direction_moviedex_left")
]