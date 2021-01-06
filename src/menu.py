"""
This module handles the different menus interactions.
"""
from time import time
from os import path

import src.game_state as gs
import src.keys as k
from src.timer import adjust_timer, get_timer
from src.display import display_controls, display_save_success, display_pause, display_game, display_save_loading_menu, display_players_selection_menu, display_loading_save_error
from src.logic import make_save
from src.upemtk import donne_evenement, type_evenement, clic_x, clic_y, ferme_fenetre, touche, mise_a_jour, attente_clic, efface_tout

def pause_game(pause_key):
    """
    Pause the game, show a pause menu and handle its options.
    """
    current_time = time()
    current_timer = get_timer()

    pause_rectangle_coords, zones_coords = display_pause()
    pause_rectangle_width = pause_rectangle_coords[2] - pause_rectangle_coords[0]
    pause_rectangle_height = pause_rectangle_coords[3] - pause_rectangle_coords[1]

    unpaused = False
    while not unpaused:

        event = donne_evenement()
        type_ev = type_evenement(event)

        if type_ev == "ClicGauche":
            click_x = clic_x(event)
            click_y = clic_y(event)

            for x1, y1, x2, y2, txt in zones_coords:
                if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
                    if txt == "quitter":
                        ferme_fenetre()
                        exit(0)
                    elif txt == "contrôles":
                        display_controls()
                        attente_clic()
                        efface_tout()
                        display_game(timer = current_timer + 1)
                        display_pause()
                    else:
                        make_save()
                        display_save_success(pause_rectangle_coords, pause_rectangle_width, pause_rectangle_height)

                elif not (click_x >= pause_rectangle_coords[0] and click_x <= pause_rectangle_coords[2] and click_y >= pause_rectangle_coords[1] and click_y <= pause_rectangle_coords[3]):
                    unpaused = True
        elif type_ev == "Touche":
            if touche(event).lower() == pause_key:
                unpaused = True
        
        mise_a_jour()
    adjust_timer(gs.start_time, current_time)

def save_loading_menu():
    """
    Display and handle the start menu where you can choose between starting a new game or loading a save previously done. Return True if the user want to load a save. Otherwise, return False.
    """
    zones_coords = display_save_loading_menu()

    wants_to_load_save = False
    chosen = False
    while not chosen:
        click_x, click_y, _ = attente_clic()
        for i, (x1, y1, x2, y2) in enumerate(zones_coords):
            if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
                chosen = True
                if i == 1: # click on the load save area
                    wants_to_load_save = True

                    while wants_to_load_save and not path.isfile("save.json"):
                        display_loading_save_error()
                        wants_to_load_save = save_loading_menu()
    return wants_to_load_save

def players_selection_menu():
    """
    Display and handle the players count selection screen.
    """
    clicked = False
    zones_coords = display_players_selection_menu()
    while not clicked:
        click_x, click_y, _ = attente_clic()
        for i, (x1, y1, x2, y2) in enumerate(zones_coords):
            if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
                efface_tout()

                gs.players_count = i + 1
                gs.keys = k.get_keys()

                display_controls()
                attente_clic()
                clicked = True