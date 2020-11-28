"""
This module includes all the game logic.
"""
from upemtk import attente_clic, clic_x, clic_y, donne_evenement, ferme_fenetre, efface_tout, mise_a_jour, touche, type_evenement
from display import display_controls
from keys import get_keys
from random import choice
from time import time

def handle_pause_menu_interaction(pause_rectangle_coords, zones_coords, pause_key):
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

            for i, (x1, y1, x2, y2, txt) in enumerate(zones_coords):
                if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
                    if txt == "quitter":
                        ferme_fenetre()
                        exit(0)
                    else:
                        # TODO : save the game state in a file
                        pass
                elif not (click_x >= pause_rectangle_coords[0] and click_x <= pause_rectangle_coords[2] and click_y >= pause_rectangle_coords[1] and click_y <= pause_rectangle_coords[3]):
                    unpaused = True
        elif type_ev == "Touche":
            if touche(event).lower() == pause_key:
                unpaused = True
        mise_a_jour()

def handle_main_menu_interaction(zones_coords, window_width, window_height):
    """
    Handles the main menu interactions, such as loading a save or choosing the players count.
    """
    keys = dict()
    nothing_selected = True

    while nothing_selected:
        click_x, click_y, _ = attente_clic()
        for i, (x1, y1, x2, y2) in enumerate(zones_coords):
            if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
                efface_tout()

                players_count = i + 1
                keys = get_keys(players_count)

                display_controls(window_width, window_height, players_count, keys)
                attente_clic()
                nothing_selected = False
                return keys

def next_color(current_color):
	"""
	Return the next color from the given one, in the order "purple", "orange", "yellow", "green".
	"""
	return {"purple": "orange", "orange": "yellow", "yellow": "green", "green": "purple"}[current_color]

def apply_debug_mode(touche, keys, pawns, current_color, debug_mode):
    """
    If the debug mode is enabled, returns a random color and a random key direction. Otherwise, returns the current color and key.
    """
    if debug_mode and (touche == None or touche.lower() != keys["debug"] and touche.lower() != keys["exit"]):
        return choice(list(pawns.keys())), choice([next(iter(keys["up"])), next(iter(keys["left"])), next(iter(keys["down"])), next(iter(keys["right"]))])
    else:
        return current_color, touche.lower()

def invert_hourglass(start_time, timeout):
    """
    Returns a new start time corresponding from which the time elapsed has been inverted according to the timout.
    """
    now = time()
    return now - (timeout * 60 + start_time - now) - 1

def is_time_elapsed(start_time, timeout):
    """
    Returns True if the time has elapsed, and False otherwise.
    """
    return timeout * 60 + start_time - time() <= 0

def update_on_objects(color, pawns, pawns_on_objects, board):
    """
    Update the pawns_on_objects dictionary provided using the new pawns coordinates. If the pawn is at the same coordinates as its object, its value in this dictionnary will be True, otherwise it will be False.
    """
    if board[pawns[color][0]][pawns[color][1]] == color[0:1]:
        pawns_on_objects[color] = True
    else:
        pawns_on_objects[color] = False

def update_on_exit(color, pawns, pawns_outside, exit_available, board):
    """
    Update the pawns_outside dictionary provided using the new pawns coordinates. If the pawn is at the same position as the exit cell, its coordinates are set to -1 to represent the "outside the board" position.
    """
    if exit_available and board[pawns[color][0]][pawns[color][1]] == "e":
        pawns_outside[color] = True
        pawns[color] = [-1,-1]

def update_on_hourglass(color, pawns, board):
    """
    If the given color pawn is on an hourglass cell, set the hourglass cell as used.
    """
    on_hourglass = board[pawns[color][0]][pawns[color][1]] == "h"
    if on_hourglass:
        board[pawns[color][0]][pawns[color][1]] = "µ"
    return on_hourglass

def split_pawns(color, pawns):
    """
    Remove the pawn corresponding to the given color from the dictionary, and returns a tuple with the coordinates of the removed pawn and the pawns dictionary without the removed one.
    """
    current_pawn = pawns[color]
    others = pawns.copy()
    others.pop(color)
    return current_pawn, others

def map_collision(current_pawn, board, walls, offsets):
    """
    Returns True if the pawn, after moving with the given offsets, will be out of the board, on a non available cell, or have to pass through walls, and False otherwise.
    """
    empty_cell = False
    board_limit = False

    if frozenset((((current_pawn[0]), (current_pawn[1])), ((current_pawn[0] + offsets[0]), (current_pawn[1] + offsets[1])))) in walls or (offsets == (-1, 0) and not current_pawn[0] > 0) or (offsets == (1, 0) and not current_pawn[0] < len(board) - 1) or (offsets == (0, -1) and not current_pawn[1] > 0) or (offsets == (0, 1) and not current_pawn[1] < len(board[0]) - 1):
        board_limit = True

    if not board_limit:
        empty_cell = board[current_pawn[0] + offsets[0]][current_pawn[1] + offsets[1]] == "*"

    return empty_cell or board_limit

def pawn_collision(current_pawn, others_pawns, offsets):
    """
    Returns True if the pawn, after moving with the given offsets, will be on the same cell as another pawn, and False otherwise.
    """
    for p in others_pawns.values():
        if p == [current_pawn[0] + offsets[0], current_pawn[1] + offsets[1]]:
            return True
    return False

def get_offsets(direction):
    """
    Returns the x and y offsets according to the given direction.
    """
    return {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}[direction]

def move(color, pawns, pawns_on_objects, pawns_outside, exit_available, walls, board, direction):
    """
    Move the pawn corresponding to the given color in the given direction in the board, and update the game state though pawns_on_objects and pawns_outside.
    """
    on_hourglass = False
    current_pawn, others_pawns = split_pawns(color, pawns)
    
    if current_pawn[0] != -1 and current_pawn[1] != -1: # if coordinates are -1, the pawn is outside the board, it has escaped successfully
        offsets = get_offsets(direction)
        collision = pawn_collision(current_pawn, others_pawns, offsets) or map_collision(current_pawn, board, walls, offsets)

        if not collision:
            pawns[color][0] += offsets[0]
            pawns[color][1] += offsets[1]
    
            update_on_objects(color, pawns, pawns_on_objects, board)
            update_on_exit(color, pawns, pawns_outside, exit_available, board)
            on_hourglass = update_on_hourglass(color, pawns, board)
    return on_hourglass