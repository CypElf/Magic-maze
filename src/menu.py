"""
This module handles the different menus interactions.
"""
from src.upemtk import donne_evenement, type_evenement, clic_x, clic_y, ferme_fenetre, touche, mise_a_jour, attente_clic, efface_tout
from src.display import display_controls, display_save_success
from src.logic import make_save
import src.keys as k

def handle_pause_menu_interaction(pause_rectangle_coords, pause_rectangle_width, pause_rectangle_height, zones_coords, pause_key, pawns, pawns_on_objects, pawns_outside, current_color, debug_mode, exit_available, start_time, board, walls, escalators, stock, on_board_cards):
    """
    Handles the pause menu interactions, such as clicking on save or quit.
    """
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
                    else:
                        make_save(pawns, pawns_on_objects, pawns_outside, current_color, debug_mode, exit_available, start_time, board, walls, escalators, stock, on_board_cards)
                        display_save_success(pause_rectangle_coords, pause_rectangle_width, pause_rectangle_height)

                elif not (click_x >= pause_rectangle_coords[0] and click_x <= pause_rectangle_coords[2] and click_y >= pause_rectangle_coords[1] and click_y <= pause_rectangle_coords[3]):
                    unpaused = True
        elif type_ev == "Touche":
            if touche(event).lower() == pause_key:
                unpaused = True
        mise_a_jour()

def handle_save_loading_menu_interaction(zones_coords):
    """
    Handles the first game menu where you can choose between starting a new game on loading a save previously done.
    """
    while True:
        click_x, click_y, _ = attente_clic()
        for i, (x1, y1, x2, y2) in enumerate(zones_coords):
            if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
                return i == 1 # True = want to load a save, False = new game

def handle_players_selection_menu_interaction(zones_coords, window_width, window_height):
    """
    Handles the main menu interactions, such as loading a save or choosing the players count.
    """
    keys = dict()

    while True:
        click_x, click_y, _ = attente_clic()
        for i, (x1, y1, x2, y2) in enumerate(zones_coords):
            if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
                efface_tout()

                players_count = i + 1
                keys = k.get_keys(players_count)

                display_controls(window_width, window_height, players_count, keys)
                attente_clic()
                return keys