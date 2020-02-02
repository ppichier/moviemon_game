from django.urls import path
from . import views

urlpatterns = [
    path("/<moviemon_id>", views.battle_f, name="battle"),
    path("/fight/launch_movieball", views.launch_movieball_f, name="launch_movieball"),
]

