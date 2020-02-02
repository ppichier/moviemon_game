from django.conf import settings
import pickle
from django.http import Http404
import requests
import random
import os
from os import path

class Game():


    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    def __init__(self):
        self.datas = {}
        self.strength = settings.PLAYER_START_STRENGTH
        self.moviemons_remaining = []
        self.moviemons_coords = []
        self.movieballs_coords = []
        self.moviemon_to_capture = None
        self.movieball_found = False
        self.moviemon_captured = False
        self.movieindex_index = 0
        self.rate_success = -1
        self.slot_save_position = 0
        self.slot_load_position = 0
        self.load_ok = False
        if os.path.exists('pickle_file.bin'):
            os.remove('pickle_file.bin')
        random.seed()

    def save_data_for_slots(self, slot_name):
        try:
            with open(settings.FILE_SAVE, 'rb') as src:
                datas = pickle.load(src)
                filename = slot_name + "_" + str(self.strength) + "_" + str(len(self.datas['movies_infos_list'])) + ".mmg"
                if not os.path.exists('saved_game'):
                    try:
                        print("yes")
                        os.mkdir('saved_game')
                    except Exception as e:
                        raise Http404("Unable to create dir saved_game ! Reason : ")
                list_file = self.get_slots_state()
                
                for fx in list_file:
                    if fx.startswith(slot_name):
                        try:
                            os.remove(os.path.join(self.BASE_DIR + "/saved_game", fx))
                        except Exception as e:
                            raise Http404("Unable to create slot file ! Reasons : ")
                with open("saved_game/" + filename, "wb") as dest:
                    pickle.dump(datas, dest)
        except Exception as e:
            raise Http404("Unable to create slot file ! Reasons : ")

    def get_slots_state(self):
        if path.exists("saved_game/"):
            saved_game_content = os.listdir("saved_game/")
        else:
            saved_game_content = []
        return(saved_game_content)

    def reload_data_if_load(self):
        all_coords = []
        self.strength = len(self.datas["moviemons_in_moviedex"])
        for i in range(0, settings.GRID_SIZE):
            for j in range(0, settings.GRID_SIZE):
                if j != self.datas['player_position']['x'] or i != self.datas['player_position']['y']:
                    all_coords.append({'x': j, 'y': i})
        
        for i in range(0, self.datas['movieball_player_nbr']):
            rand_index_coord = random.randint(0, len(all_coords) - 1)
            self.movieballs_coords.append(all_coords[rand_index_coord])
            del all_coords[rand_index_coord]

        #remaining list
        remain_moviemons = [i for i in self.datas['movies_infos_list'] if i not in self.datas['moviemons_in_moviedex']]
        self.moviemons_remaining = remain_moviemons
        for i in range(0, len(self.moviemons_remaining)):
            rand_index_coord = random.randint(0, len(all_coords) - 1)
            self.moviemons_coords.append(all_coords[rand_index_coord])
            del all_coords[rand_index_coord]
    

    def load(self, slot_name):
        list_load_files = self.get_slots_state()
        for load_file in list_load_files:
            if load_file.startswith(slot_name):
                try:
                    with open( os.path.join(self.BASE_DIR + "/saved_game", load_file), 'rb') as game_file:
                        self.datas = pickle.load(game_file)
                        self.reload_data_if_load()    
                except Exception as err:
                    print (err)
                    raise Http404("Unable to load save file !")
                self.load_ok = True
                return True
        return False

    def write(self, filename):
        try:
            with open(filename, 'wb') as game_file:
                pickle.dump(self.datas, game_file)
        except Exception:
            raise Http404("Unable to write in save file !")
        return self

    def dump(self):
        return self.datas

    def get_random_movie(self):
        return self.moviemons_remaining[random.randint(0, len(self.moviemons_remaining) - 1)]

    def load_default_settings(self):
        self.datas = {
            "player_position": {'x': settings.PLAYER_START_POSITION['x'], 'y': settings.PLAYER_START_POSITION['y']},
            "movieball_player_nbr": settings.MOVIEBALL_PLAYER_NBR,
            "moviemons_in_moviedex": [],
            "movies_infos_list": []
        }
        for title in settings.MOVIES_TITLE_LIST:
            try: 
                response_json = requests.get(
                    'http://www.omdbapi.com/?apikey=3cc63f26&t="' + title + '"'
                )
                if response_json.status_code != requests.codes.ok:
                    raise Http404("Unable to load moviemons from OMDB !")
                res = response_json.json()
                self.datas['movies_infos_list'].append({k: v for k, v in res.items() if k == "Title" or k == "Poster" or k == "imdbRating" or k == "Year" or k == "Director" or k == "Actors" or k == "Plot" or k == "imdbID"})
                self.moviemons_remaining = self.datas['movies_infos_list'].copy()

            except Exception as err:
                print(err)
                raise Http404("Unable to load moviemons from OMDB !")
        # print(self.datas['movies_infos_list'][9])
        return self
    
    def get_strength(self):
        return self.strength
    
    def get_movie(self, name):
        for movie in self.datas['movies_infos_list']:
            if movie['Title'] == name:
                return movie
            else:
                return None
    
    def populate_map(self):
        all_coords = []
        for i in range(0, settings.GRID_SIZE):
            for j in range(0, settings.GRID_SIZE):
                if j != settings.PLAYER_START_POSITION['x'] or i != settings.PLAYER_START_POSITION['y']:
                    all_coords.append({'x': j, 'y': i})
        
        for i in range(0, settings.MOVIEBALL_TOTAL):
            rand_index_coord = random.randint(0, len(all_coords) - 1)
            self.movieballs_coords.append(all_coords[rand_index_coord])
            del all_coords[rand_index_coord]
        
        for i in range(0, len(settings.MOVIES_TITLE_LIST)):
            rand_index_coord = random.randint(0, len(all_coords) - 1)
            self.moviemons_coords.append(all_coords[rand_index_coord])
            del all_coords[rand_index_coord]

    def update_player_position(self, direction):
        if direction == "player_position_up" and self.datas['player_position']['y'] > 0:
            self.datas['player_position']['y'] -= 1
        elif direction == "player_position_down" and self.datas['player_position']['y'] < settings.GRID_SIZE - 1:
            self.datas['player_position']['y'] += 1
        elif direction == "player_position_left" and self.datas['player_position']['x'] > 0:
            self.datas['player_position']['x'] -= 1
        elif direction == "player_position_right" and self.datas['player_position']['x'] < settings.GRID_SIZE - 1:
            self.datas['player_position']['x'] += 1
        self.write(settings.FILE_SAVE)
        return self
    
    def try_to_find_moviemon(self):
        try:
            index_found = self.moviemons_coords.index(self.datas['player_position'])
            self.moviemon_to_capture = self.get_random_movie()
        except Exception:
            self.moviemon_to_capture = None

    def try_to_take_movieball(self):
        try:
            movieball_index = self.movieballs_coords.index(self.datas['player_position'])
            del self.movieballs_coords[movieball_index]
            self.datas["movieball_player_nbr"] += 1
            self.movieball_found = True
            self.write(settings.FILE_SAVE)

        except Exception:
            self.movieball_found = False

    def calcul_rate_success(self):
        try:
            moviemon_strength = int(float(self.moviemon_to_capture["imdbRating"]))
        except Exception:
            moviemon_strength = 4
        
        chance_rate = 50 - (moviemon_strength * 10) + (self.strength * 5)
        if (chance_rate <= 0):
            chance_rate = 1
        elif (chance_rate > 90):
            chance_rate = 90
        self.rate_success = chance_rate
        return chance_rate
        


    def try_to_capture_moviemon(self):
        self.moviemon_captured = False
        if (self.datas["movieball_player_nbr"] > 0):
            self.datas["movieball_player_nbr"] -= 1
            # C = 50 - (force du monstre * 10) + (force du joueur * 5)
            rand = random.randint(0, 100)
            if (self.rate_success >= rand):
                self.strength += 1
                index_moviemon = self.moviemons_remaining.index(self.moviemon_to_capture)
                self.datas['moviemons_in_moviedex'].append(self.moviemon_to_capture)
                del self.moviemons_remaining[index_moviemon]
                for movie in self.moviemons_remaining:
                    print (movie["Title"])
                index_coord_moviemon = self.moviemons_coords.index(self.datas['player_position'])
                del self.moviemons_coords[index_coord_moviemon]
                self.moviemon_captured = True
                self.write(settings.FILE_SAVE)

    def update_moviedex_cursor(self, direction):

        len_mi = len(self.datas["moviemons_in_moviedex"])
        if direction == "right" and self.movieindex_index < len_mi - 1 :
            self.movieindex_index += 1
        if direction == "left" and self.movieindex_index > 0:
            self.movieindex_index -= 1
        return self

    def slot_save_direction(self, direction):
        if direction == "up" and self.slot_save_position < 2:
            self.slot_save_position += 1
        if direction == "down" and self.slot_save_position > 0:
            self.slot_save_position -= 1
        return self

    def slot_load_position_f(self, direction):
        if direction == "up" and self.slot_load_position < 2:
            self.slot_load_position += 1
        if direction == "down" and self.slot_load_position > 0:
            self.slot_load_position -= 1
        return self
