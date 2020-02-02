from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404

# Create your views here.



def direction_moviedex_f(request):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")
    settings.GAME_INSTANCE = settings.GAME_INSTANCE.update_moviedex_cursor(request.path.split("/")[3])
    return redirect("moviedex")

def press_a(request, moviedex_id):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")
    if len(settings.GAME_INSTANCE.datas["moviemons_in_moviedex"]) == 0:
        return redirect("moviedex")
    else:
        contexte = {
            "button_b": "moviedex",
            "current_moviedex": settings.GAME_INSTANCE.datas['moviemons_in_moviedex'][settings.GAME_INSTANCE.movieindex_index]
        }
        return render(request, "moviedex/moviedex-details.html", contexte )
    

def moviedex_f(request):



    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")

    contexte = {
        "button_select": "worldmap",
        "button_right": "direction_moviedex_right",
        "button_left": "direction_moviedex_left",
        "list_moviedex": settings.GAME_INSTANCE.datas['moviemons_in_moviedex'],
        "current_moviedex": "null",
        "moviedex_selected": settings.GAME_INSTANCE.movieindex_index,
        "button_a": "press_a",
        "moviedex_id": "null"
    }

    ref = request.META['HTTP_REFERER'].split('/')
    if (len(ref) > 2):
        if ref[len(ref) - 2] == "moviedex" or ref[len(ref) - 1] == "moviedex":
            contexte["moviedex_selected"] = settings.GAME_INSTANCE.movieindex_index
        else:
            settings.GAME_INSTANCE.movieindex_index = 0
            contexte["moviedex_selected"] = 0


    # if  request.META['HTTP_REFERER']

    if len(settings.GAME_INSTANCE.datas["moviemons_in_moviedex"]) > 0:
        contexte['current_moviedex'] = settings.GAME_INSTANCE.datas['moviemons_in_moviedex'][settings.GAME_INSTANCE.movieindex_index]
        contexte['moviedex_id'] = settings.GAME_INSTANCE.datas["moviemons_in_moviedex"][settings.GAME_INSTANCE.movieindex_index]['imdbID']

    
    return render(request, "moviedex/moviedex.html", contexte)
