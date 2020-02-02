from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404

# Create your views here.


def options_save(request):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")

    if (settings.GAME_INSTANCE.slot_save_position == 0):
        settings.GAME_INSTANCE.save_data_for_slots("slota")
    elif (settings.GAME_INSTANCE.slot_save_position == 1):
        settings.GAME_INSTANCE.save_data_for_slots("slotb")
    elif (settings.GAME_INSTANCE.slot_save_position == 2):
        settings.GAME_INSTANCE.save_data_for_slots("slotc")
    return redirect("optionsSaveGame")
 
def direction_save_direction_f(request):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")
    settings.GAME_INSTANCE = settings.GAME_INSTANCE.slot_save_direction(request.path.split("/")[4])
    return redirect("optionsSaveGame")


def options_f(request):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")
    return render(request, "option/option.html", {"button_start": "worldmap", "button_b": "titlescreen", "button_a": "optionsSaveGame"})

def options_save_f(request):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")

    #read save slots
    list_slot = settings.GAME_INSTANCE.get_slots_state()
    slot_a_status = "FREE"
    slot_b_status = "FREE"
    slot_c_status = "FREE"
    for slot in list_slot:
        a = slot.split("_")
        if slot.startswith("slota"):
            slot_a_status = a[1] + "_" + a[2]
        if slot.startswith("slotb"):
            slot_b_status = a[1] + "_" + a[2]
        if slot.startswith("slotc"):
            slot_c_status = a[1] + "_" + a[2]
        

    context = {
        "button_up": "directionSaveGameUp",
        "button_down": "directionSaveGameDown",
        "button_b": "options",
        "button_a": "save_slot",
        "slot_a_status": slot_a_status,
        "slot_b_status": slot_b_status,
        "slot_c_status": slot_c_status,
        "slot_save_position": settings.GAME_INSTANCE.slot_save_position,
    }
    return render(request, "option/optionSaveGame.html", context)


def options_load(request):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")
    if (settings.GAME_INSTANCE.slot_load_position == 0):
        settings.GAME_INSTANCE.load("slota")
    elif (settings.GAME_INSTANCE.slot_load_position == 1):
        settings.GAME_INSTANCE.load("slotb")
    elif (settings.GAME_INSTANCE.slot_load_position == 2):
        settings.GAME_INSTANCE.load("slotc")
    return redirect("optionsLoadGame")


def direction_load_direction_f(request):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")
    settings.GAME_INSTANCE.slot_load_position_f(request.path.split("/")[4])
    return redirect("optionsLoadGame")



def options_load_f(request):
    if settings.GAME_INSTANCE == None:
        raise Http404("Game Instance doesn't exist : Game unable to run !")

    list_slot = settings.GAME_INSTANCE.get_slots_state()
    slot_a_status = "FREE"
    slot_b_status = "FREE"
    slot_c_status = "FREE"
    for slot in list_slot:
        a = slot.split("_")
        if slot.startswith("slota"):
            slot_a_status = a[1] + "_" + a[2]
        if slot.startswith("slotb"):
            slot_b_status = a[1] + "_" + a[2]
        if slot.startswith("slotc"):
            slot_c_status = a[1] + "_" + a[2]
        


    context = {
        "button_up": "directionLoadGameUp",
        "button_down": "directionLoadGameDown",
        "button_b": "titlescreen",
        "button_a": "load_slot",
        "msg_load_ok": "",
        "slot_a_status": slot_a_status,
        "slot_b_status": slot_b_status,
        "slot_c_status": slot_c_status,
        "slot_load_position": settings.GAME_INSTANCE.slot_load_position,
    }

    if settings.GAME_INSTANCE.load_ok == True :
        context["button_a"] = "worldmap"
        context["msg_load_ok"] = "File Load ! Press A to go in worldmap !"

    return render(request, "option/optionLoadGame.html", context)