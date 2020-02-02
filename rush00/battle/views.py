from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404

# Create your views here.


def launch_movieball_f(request):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")
    settings.GAME_INSTANCE.try_to_capture_moviemon()
    return redirect('battle', moviemon_id=settings.GAME_INSTANCE.moviemon_to_capture['imdbID'])

def battle_f(request, moviemon_id):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")

  

    context = {
        "movieballs_nbr": settings.GAME_INSTANCE.datas["movieball_player_nbr"],
        "button_a": "launch_movieball",
        "button_b": "worldmap",
        "message_movieball_found": "",
        "message_zero_movieball": "",
        "message_success": "",
        "message_not_captured": "",
        "moviemon_id": settings.GAME_INSTANCE.moviemon_to_capture["imdbID"],
        "moviemon_poster": settings.GAME_INSTANCE.moviemon_to_capture["Poster"],
        "moviemon_strength": settings.GAME_INSTANCE.moviemon_to_capture["imdbRating"],
        "player_strength": settings.GAME_INSTANCE.strength,
        "rate_success": settings.GAME_INSTANCE.rate_success
    }


    if settings.GAME_INSTANCE.datas['movieball_player_nbr'] == 0:
        context["message_zero_movieball"] = "HAHA NO MORE MOVIEBALL !"
    else:
        context["message_zero_movieball"] = "Press a to launch Movieball !"
    if settings.GAME_INSTANCE.rate_success == -1:
        context['rate_success'] = settings.GAME_INSTANCE.calcul_rate_success()

    if settings.GAME_INSTANCE.moviemon_captured:
        context["message_not_captured"] = ""
        context["message_zero_movieball"] = ""
        settings.GAME_INSTANCE.rate_success = -1
        context["message_success"] = "MOVIEMON CAPTURED!"
        context["button_a"] = ""
        settings.GAME_INSTANCE.moviemon_to_capture = None
        settings.GAME_INSTANCE.moviemon_captured = False
    else:
        context["message_not_captured"] = "HAHA I'M STILL HERE !"

    return render(request, "battle/battle.html", context)
