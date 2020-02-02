from django.urls import path
from . import views

urlpatterns = [
    path("/", views.worldmap_f, name="worldmap"),
    path("/player_position_up", views.update_player_position, name="player_position_up"),
    path("/player_position_down", views.update_player_position, name="player_position_down"),
    path("/player_position_right", views.update_player_position, name="player_position_right"),
    path("/player_position_left", views.update_player_position, name="player_position_left")
]

