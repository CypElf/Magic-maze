"""
This module includes all the game logic.
"""
from random import choice
from time import time
from json import dump
from itertools import cycle
from src.display import display_selected_vortex, display_game
from src.upemtk import attente_touche_jusqua

def make_save(pawns, pawns_on_objects, pawns_outside, current_color, debug_mode, exit_available, start_time, board):
    with open("save.json", "w") as savefile:
        state = {
            "pawns": pawns,
            "pawns_on_objects": pawns_on_objects,
            "pawns_outside": pawns_outside,
            "current_color": current_color,
            "debug_mode": debug_mode,
            "exit_available": exit_available,
            "start_time": start_time,
            "save_time": time(),
            "board": board
        }
        dump(state, savefile)

def next_color(current_color):
	"""
	Return the next color from the given one, in the order "purple", "orange", "yellow", "green".
	"""
	return {"purple": "orange", "orange": "yellow", "yellow": "green", "green": "purple"}[current_color]

def apply_debug_mode(touche, keys, debug_mode):
    """
    If the debug mode is enabled, returns a random color and a random key direction. Otherwise, returns the current color and key.
    """
    if debug_mode and (touche == None or touche.lower() != keys["debug"] and touche.lower() != keys["exit"]):
        return choice([next(iter(keys["up"])), next(iter(keys["left"])), next(iter(keys["down"])), next(iter(keys["right"])), keys["escalator"], keys["vortex"], next(iter(keys["switch"]))])
    elif touche != None:
        return touche.lower()
    else:
        return touche

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

def use_escalator(current_color, pawns, escalators):
    """
    Move the pawn to the other side of the escalator if he is on one's extremity and if there is no other pawn on the other side.
    """
    current_pawn, other_pawns = split_pawns(current_color, pawns)
    current_position = tuple(current_pawn)

    if current_position[0] != -1 and current_position[1] != -1:
        for coords1, coords2 in escalators:
            if coords1 == current_position and list(coords2) not in other_pawns.values():
                pawns[current_color] = list(coords2)
            elif coords2 == current_position and coords1 not in other_pawns.values():
                pawns[current_color] = list(coords1)

def use_vortex(keys, current_color, pawns, exit_available, walls, escalators, start_time, timeout, debug_mode, game_width, game_height, window_width, window_height, board):
    if not exit_available:
        vortex_color = "v" + current_color[0]
        usable_vortex = {(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == vortex_color}
        if len(usable_vortex) > 0:
            usable_vortex = cycle(usable_vortex)
            currently_selected_vortex = next(usable_vortex)

            while True:
                display_selected_vortex(currently_selected_vortex[0], currently_selected_vortex[1], game_width, game_height, board)
                touche = attente_touche_jusqua(50)
                touche = apply_debug_mode(touche, keys, debug_mode)
                display_game(board, pawns, current_color, exit_available, walls, escalators, start_time, timeout, game_width, game_height, window_width, window_height)
                if touche in keys["switch"]:
                    currently_selected_vortex = next(usable_vortex)
                if touche == keys["vortex"]:
                    break

            pawns[current_color] = list(currently_selected_vortex)