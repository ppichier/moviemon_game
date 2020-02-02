from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404
# Create your views here.


def update_player_position(request):
    settings.GAME_INSTANCE = settings.GAME_INSTANCE.update_player_position(request.path.split("/")[2])
    settings.GAME_INSTANCE.try_to_take_movieball()
    settings.GAME_INSTANCE.try_to_find_moviemon()
    return redirect('worldmap')

def worldmap_f(request):

    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")

    context = {
        "movieballs_nbr": settings.GAME_INSTANCE.datas["movieball_player_nbr"],
        "button_a": "",
        "message_movieball_found": "",
        "message_moviemon_found": "",
        "button_start": "options",
        "button_select" : "moviedex",
        "button_up": "player_position_up",
        "button_down": "player_position_down",
        "button_right": "player_position_right",
        "button_left": "player_position_left",
        "grid_map": range(0, settings.GRID_SIZE),
        "player_position": {'x': settings.GAME_INSTANCE.datas['player_position']['x'], 'y': settings.GAME_INSTANCE.datas['player_position']['y']},
        "moviemon_id": ""   
    }
    
    if settings.GAME_INSTANCE.moviemon_to_capture != None:
        context['message_moviemon_found'] = "MOVIEMON FOUND ! PRESS A FOR THE BATTLE"
        context["moviemon_id"] = settings.GAME_INSTANCE.moviemon_to_capture['imdbID']
        context["button_a"] = "battle"
    
    if settings.GAME_INSTANCE.movieball_found:
        context["message_movieball_found"] = "YOU HAVE FOUND A MOVIEBALL !"

    # if key direction -> update player position
    #open file -> positio, nbr movieball
    return render(request, "worldmap/worldmap.html", context)


## RAISE 404 OTHER PAGES IF NECESSARY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!