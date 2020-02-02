from django.shortcuts import render, HttpResponse
import requests
from django.conf import settings
from datamanager import game




def titlescreen_f(request):
    settings.GAME_INSTANCE = game.Game()
    settings.GAME_INSTANCE = settings.GAME_INSTANCE.load_default_settings()
    settings.GAME_INSTANCE.populate_map()

    return render(request, "titlescreen/titlescreen.html", {"button_a": "worldmap", "button_b": "optionsLoadGame"})
