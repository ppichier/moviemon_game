from django.urls import path

from . import views

urlpatterns = [
    path("/", views.options_f, name="options"),
    path("/save_game/", views.options_save_f, name="optionsSaveGame"),
    path("/save/direction/up", views.direction_save_direction_f, name="directionSaveGameUp"),
    path("/save/direction/down", views.direction_save_direction_f, name="directionSaveGameDown"),
    path("/save/slot", views.options_save, name="save_slot"),
    path("/load_game/", views.options_load_f, name="optionsLoadGame"),
    path("/load/direction/up", views.direction_load_direction_f, name="directionLoadGameUp"),
    path("/load/direction/down", views.direction_load_direction_f, name="directionLoadGameDown"),
    path("/load/slot", views.options_load, name="load_slot"),
]
