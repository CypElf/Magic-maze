"""
This module includes all the game logic.
"""
from random import choice, choices
from operator import add
from time import time
from json import dump, load
from copy import deepcopy
from itertools import cycle

import src.game_state as gs
from src.timer import invert_timer, adjust_timer
from src.display import display_selected_vortex, display_game, display_selected_card
from src.cards import cards
from src.upemtk import attente_touche_jusqua

# ------------------------------------------------- update game state

def update_on_objects():
    """
    Update the pawns_on_objects dictionary using the current pawns coordinates. If the pawn is at the same coordinates as its object, its value in this dictionary will be True, otherwise it will be False.
    """
    color = gs.current_color
    if not color.startswith("fake"):
        if gs.board[gs.pawns[color][0]][gs.pawns[color][1]] == color[0:1]:
            gs.pawns_on_objects[color] = True
        else:
            gs.pawns_on_objects[color] = False

def update_on_exit():
    """
    Update the pawns_outside dictionary using the current pawns coordinates. If the pawn is at the same position as the exit cell, its coordinates are set to -1 to represent the "outside the board" position.
    """
    color = gs.current_color
    if gs.exit_available and gs.board[gs.pawns[color][0]][gs.pawns[color][1]] == "e" and not color.startswith("fake"):
        gs.pawns_outside[color] = True
        gs.pawns[color] = [-1,-1]

def update_on_hourglass():
    """
    If the currently selected pawn is on an hourglass cell, set the hourglass cell as used and invert the timer.
    """
    color = gs.current_color
    on_hourglass = gs.board[gs.pawns[color][0]][gs.pawns[color][1]] == "h"
    if on_hourglass:
        gs.board[gs.pawns[color][0]][gs.pawns[color][1]] = "µ"
        gs.start_time = invert_timer()

def update_on_board_cards(edited_card):
    """
    Update the on_board_cards by editing the card passed as parameter if already on the board.
    """
    for card in gs.on_board_cards:
        if card["id"] == edited_card["id"]:
            card["rotations"] = edited_card["rotations"]
            card["top_left"] = edited_card["top_left"]
            break

# ------------------------------------------------- cards utilities

def is_card_guarded(coords):
    """
    Return True if the card to which the coordinates passed as a parameter belong is kept by a guard, False otherwise.
    """
    color = gs.current_color
    on_board_cards = gs.on_board_cards
    pawns = gs.pawns
    current_card_id = get_current_card(pawns[color], on_board_cards)
    new_card_id = get_current_card(coords, on_board_cards)

    guarded_cards = list(map(lambda current_color: get_current_card(pawns[current_color], on_board_cards), filter(lambda current_color: (color.startswith("fake") or current_color.startswith("fake")) and current_color != color, pawns.keys())))
    
    if current_card_id in guarded_cards:
        guarded_cards.remove(current_card_id) # prevent movement blocking when two guards are on the same card in a particular case where a reinforcement guard spawn on the same card as another guard

    return new_card_id in guarded_cards

def get_random_card():
    """
    Return a random card and remove it from the stock.
    """
    c = choice(gs.stock)
    gs.stock.remove(c)
    return c

def get_current_card(pawn, on_board_cards):
    """
    Return the ID of the card where the current pawn is positionned.
    """
    i, j = pawn
    for card in on_board_cards:
        if i >= card["top_left"][0] and i < card["top_left"][0] + 4 and j >= card["top_left"][1] and j < card["top_left"][1] + 4:
            return card["id"]

def get_offsets(direction):
    """
    Returns the relative x and y offsets of the neighbor cell in the given direction.
    """
    return {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}[direction]

def next_direction(direction):
    """
    Return the new pointing direction of a direction after a 1/4 rotation to the right.
    """
    return {"d": "l", "r": "d", "u": "r", "l": "u"}[direction]

# ------------------------------------------------- cards manipulation

def align_card(new_card, direction):
    """
    Rotate the new card board in order to make its white arrow to be in the same direction as the given one.
    """
    aligned = False
    i = 0
    while not aligned:
        for row in new_card["board"]:
            for element in row:
                if element.startswith("aw") and element[-1] == direction:
                    aligned = True
        if not aligned:
            i += 1
            one_quarter_right_rotation(new_card)
    new_card["rotations"] = i

def reverse_horizontally(card):
    """
    Reverse a card horizontally.
    >>> card = [[(20, 30, 50), (50, 80, 90)], [(20, 30, 50), (50, 80, 90)]]
    >>> reverse_horizontally(card)
    >>> card
    [[(50, 80, 90), (20, 30, 50)], [(50, 80, 90), (20, 30, 50)]]
    """
    nb_lignes = len(card)
    nb_colonnes = len(card[0])
    for i in range(nb_lignes):
        for j in range(nb_colonnes // 2):
            card[i][j], card[i][nb_colonnes - (j + 1)] = card[i][nb_colonnes - (j + 1)],  card[i][j]

def one_quarter_right_rotation(card):
    """
    Rotate a card by 1/4 to the right, including its escalators and walls.
    >>> card = [[(20, 30, 50), (50, 80, 90)], [(20, 80, 50), (60, 80, 90)]]
    >>> rotation_un_quart(card)
    >>> card
    [[(20, 80, 50), (20, 30, 50)], [(60, 80, 90), (50, 80, 90)]]
    """
    board = card["board"]
    for i in range(len(board)):
        for j in range(i + 1):
            for a, b in {(i, j), (j, i)}:
                if board[a][b][-1] in {"l", "d", "u", "r"}:
                    board[a][b] = board[a][b][:2] + next_direction(board[a][b][-1])
            board[i][j], board[j][i] = board[j][i], board[i][j]
    reverse_horizontally(board)
    card["walls"] = one_quarter_right_rotation_walls(card["walls"])
    if card["escalator"] is not None:
        card["escalator"] = one_quarter_right_rotation_escalators(card["escalator"])

def one_quarter_right_rotation_escalators(escalator):
    """
    Return the escalator coordinates rotated by 1/4. This assumes the escalator is defined for a 4×4 board.
    """
    return ((escalator[0][1], 4 - (escalator[0][0] + 1)), (escalator[1][1], 4 - (escalator[1][0] + 1)))

def one_quarter_right_rotation_walls(walls):
    """
    Return the walls coordinates rotated by 1/4. This assumes the walls are defined for a 4×4 board.
    """
    return {one_quarter_right_rotation_wall(wall) for wall in walls}

def one_quarter_right_rotation_wall(wall):
    """
    Return the wall coordinates rotated by 1/4. This assumes the wall is defined for a 4×4 board.
    """
    (i1, j1), (i2, j2) = wall
    return  ((j1, 4 - (i1 + 1)), (j2, 4 - (i2 + 1)))

# ------------------------------------------------- movement

def move(direction):
    """
    Move the currently selected pawn in the given direction in the board.
    """
    color = gs.current_color
    pawns = gs.pawns
    current_pawn, _ = split_pawns()
    
    if current_pawn[0] != -1 and current_pawn[1] != -1: # if coordinates are -1, the pawn is outside the board, it has escaped successfully
        offsets = get_offsets(direction)
        collision = pawn_collision(offsets) or map_collision(offsets)

        if not collision:
            new_pawn_coords = [pawns[color][0] + offsets[0], pawns[color][1] + offsets[1]]
            guarded = is_card_guarded(new_pawn_coords)

            if not guarded:
                pawns[color] = new_pawn_coords
        
                update_on_objects()
                update_on_exit()
                if not color.startswith("fake"):
                    update_on_hourglass()

# ------------------------------------------------- escalators

def use_escalator():
    """
    Move the pawn to the other side of the escalator if he is on one's extremity and if there is no other pawn on the other side.
    """
    color = gs.current_color
    pawns = gs.pawns
    current_pawn, other_pawns = split_pawns()

    if current_pawn[0] != -1 and current_pawn[1] != -1:
        for coords1, coords2 in gs.escalators:
            coords1, coords2 = list(coords1), list(coords2)
            if coords1 == current_pawn and coords2 not in other_pawns.values():
                pawns[color] = coords2
            elif coords2 == current_pawn and coords1 not in other_pawns.values():
                pawns[color] = coords1

# ------------------------------------------------- vortex

def use_vortex(keys):
    """
    Allow a pawn to choose a vortex of his color to teleport to. This is only allowed if the exit is not available yet.
    """
    if not gs.exit_available:
        color = gs.current_color
        board = gs.board
        pawns = gs.pawns

        vortex_color = "v" + color[0]
        usable_vortex = {(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == vortex_color}
        if len(usable_vortex) > 0:
            usable_vortex = cycle(usable_vortex)
            currently_selected_vortex = next(usable_vortex)
            _, other_pawns = split_pawns()

            while True:
                touche = attente_touche_jusqua(50)
                touche = apply_debug_mode(touche, mode = "vortex")
                display_game()
                display_selected_vortex(currently_selected_vortex)
                if touche in keys["switch"]:
                    currently_selected_vortex = next(usable_vortex)
                elif touche == keys["vortex"]:
                    break
                elif touche == keys["exit"]:
                    return

            currently_selected_vortex = list(currently_selected_vortex)
            if currently_selected_vortex not in other_pawns.values():
                pawns[color] = currently_selected_vortex

# ------------------------------------------------- explore

def explore():
    """
    Add a new card to the board.
    """
    color = gs.current_color
    pawns = gs.pawns
    board = gs.board

    i, j = pawns[color][0], pawns[color][1]
    current_board_element = board[i][j]
    if current_board_element[0] == "a" and current_board_element[1] == color[0]:
        board[i][j] = "."
        new_card = get_random_card()
        direction = current_board_element[2]

        align_card(new_card, direction)

        offset_i, offset_j = get_neighbor_top_left_corner_from_explore(direction)
        top_left_i, top_left_j = i + offset_i, j + offset_j

        add_walls_to_game(new_card["walls"], [top_left_i, top_left_j])
        add_escalator_to_game(new_card["escalator"], [top_left_i, top_left_j])

        gs.on_board_cards.append({"id": new_card["id"], "top_left": (top_left_i, top_left_j), "rotations": new_card["rotations"]})

        for i in range(4):
            for j in range(4):
                current_i = top_left_i + i
                current_j = top_left_j + j

                board[current_i][current_j] = new_card["board"][i][j]
                if board[current_i][current_j] == "f":
                    pawns[f"fake_{len(pawns) - 4}"] = [current_i, current_j]

        remove_unusable_exploration_cells(direction)

    if len(gs.stock) == 0:
        remove_all_exploration_cells()

def add_walls_to_game(walls, top_left):
    """
    Add walls to the board. The walls coordinates must be relative to the top left of a 4×4 card, whose coordinates on the board are passed as a parameter.
    """
    for (i1, j1), (i2, j2) in walls:
        gs.walls.add(((i1 + top_left[0], j1 + top_left[1]), (i2 + top_left[0], j2 + top_left[1])))

def add_escalator_to_game(escalator, top_left):
    """
    Add an escalator to the board. The escalator coordinates must be relative to the top left of a 4×4 card, whose coordinates on the board are passed as a parameter.
    """
    if escalator is not None:
        gs.escalators.add(((escalator[0][0] + top_left[0], escalator[0][1] + top_left[1]), (escalator[1][0] + top_left[0], escalator[1][1] + top_left[1])))

# ------------------------------------------------- telekinesis

def use_telekinesis():
    """
    Use the elfe telekinesis power to teleport a card from a location to another. 
    """
    color = gs.current_color
    board = gs.board
    pawns = gs.pawns

    pawn_i, pawn_j = pawns[color][0], pawns[color][1]
    current_board_element = board[pawn_i][pawn_j]

    if color == "green" and current_board_element[0] == "a" and gs.telekinesis_times_used < 2:
        movable_cards = get_movable_cards()

        if movable_cards:
            movable_cards = cycle(movable_cards)
            teleported_card = next(movable_cards)

            while True:
                touche = attente_touche_jusqua(50)
                touche = apply_debug_mode(touche, mode = "telekinesis")
                display_game()
                display_selected_card(teleported_card["top_left"])
                if touche in gs.keys["switch"]:
                    teleported_card = next(movable_cards)
                elif touche == gs.keys["telekinesis"]:
                    break
                elif touche == gs.keys["exit"]:
                    return

            original_card = deepcopy(cards[teleported_card["id"] - 2]) # -2 because the cards start at ID 2
            for _ in range(teleported_card["rotations"]):
                one_quarter_right_rotation(original_card)

            direction = current_board_element[2] # direction in which the elfe is teleporting a card
            off_i, off_j = get_neighbor_top_left_corner_from_explore(direction)


            if original_card["escalator"] is not None: # remove escalator from previous card location
                absolute_escalator = ((original_card["escalator"][0][0] + teleported_card["top_left"][0], original_card["escalator"][0][1] + teleported_card["top_left"][1]), (original_card["escalator"][1][0] + teleported_card["top_left"][0], original_card["escalator"][1][1] + teleported_card["top_left"][1]))

                gs.escalators = list(gs.escalators)
                gs.escalators.remove(absolute_escalator)
                gs.escalators = set(gs.escalators)

            gs.walls = list(gs.walls)
            for wall in original_card["walls"]: # remove walls from previous card location
                absolute_wall = ((wall[0][0] + teleported_card["top_left"][0], wall[0][1] + teleported_card["top_left"][1]), (wall[1][0] + teleported_card["top_left"][0], wall[1][1] + teleported_card["top_left"][1]))

                gs.walls.remove(absolute_wall)
            gs.walls = set(gs.walls)

            original_card = deepcopy(cards[teleported_card["id"] - 2]) # -2 because the cards start at ID 2
            align_card(original_card, direction)
            original_card["top_left"] = [pawn_i + off_i, pawn_j + off_j]

            board[pawn_i][pawn_j] = "."
            for i in range(4):
                for j in range(4):
                    current_i = pawn_i + i + off_i
                    current_j = pawn_j + j + off_j

                    board[teleported_card["top_left"][0] + i][teleported_card["top_left"][1] + j] = "*"
                    board[current_i][current_j] = original_card["board"][i][j]

            remove_unusable_exploration_cells(direction)
            
            add_walls_to_game(original_card["walls"], original_card["top_left"])
            add_escalator_to_game(original_card["escalator"], original_card["top_left"])
            update_on_board_cards(original_card)

            gs.telekinesis_times_used += 1

def get_movable_cards():
    """
    Return the cards that can be teleported by telekinesis. The rules are :
    - cards with pawns on them can't be teleported
    - if teleporting the card leaves a card without at least one neighbor, this card can't be teleported.
    - the start card can't be teleported.
    """
    movable_cards = []

    directions = ["up", "down", "left", "right"]
    for card in gs.on_board_cards:
        if card["id"] != 1: # teleport the first base card is forbidden
            movable = True
            for dir2 in directions:
                off_i, off_j = get_neightbor_top_left_corner_from_top_left(dir2)
                dircopy = directions.copy()
                dircopy.remove(opposite_direction(dir2))

                if has_neighbors([card["top_left"][0], card["top_left"][1]], {dir2}, ignoreone = True) and not has_neighbors([card["top_left"][0] + off_i, card["top_left"][1] + off_j], set(dircopy)):
                    movable = False
            if movable:
                for pawn in gs.pawns.values():
                    if pawn[0] >= card["top_left"][0] and pawn[0] < card["top_left"][0] + 4 and pawn[1] >= card["top_left"][1] and pawn[1] < card["top_left"][1] + 4:
                        movable = False
                if movable:
                    movable_cards.append(card)
    return movable_cards    

# ------------------------------------------------- neighbors related utilities

def has_neighbors(coords, directions = {"up", "down", "left", "right"}, ignoreone = False):
    """
    Return True if a card is located nearby the given one. (i, j) are the coordinates of the top left corner of the card you want to check the neighbors. The direction parameter is optional and allow to check for a neighbor only in the given. This parameter must be a set containing the directions to check between "up", "left", "down" and "right" (as strings). Defaults to all of them. If ignoreone is set to True, ignore the neightbor of ID 1 (the start card). Defaults to False.
    """
    board = gs.board
    on_board_cards = gs.on_board_cards

    i, j = coords

    for direction in directions:
        neighbor_i, neighbor_j = get_neightbor_top_left_corner_from_top_left(direction)

        for off1 in range(4):
            for off2 in range(4):
                x = i + neighbor_i + off1
                y = j + neighbor_j + off2
                if x >= 0 and x < len(board) and y >= 0 and y < len(board[0]) and board[x][y] != "*":
                    skip = False
                    if ignoreone and get_current_card([x, y], on_board_cards) == 1:
                        skip = True
                    if not skip:
                        return True
    return False

def get_neighbor_top_left_corner_from_explore(direction):
    """
    Return the relative offsets where the top left corner of the neighbor card would be situated, from an exploration cell. Direction must be one of "up", "down", "left", or "right".
    """
    return {"l": (-2, -4), "d": (1, -2), "u": (-4, -1), "r": (-1, 1)}[direction[0]]

def get_neightbor_top_left_corner_from_top_left(direction):
    """
    Return the relative offsets where the top left corner of the neighbor card would be situated, from the top left of a card. Direction must be one of "up", "down", "left", or "right".
    """
    return {"l": (-1, -4), "u": (-4, 1), "d": (4, -1), "r": (1, 4)}[direction[0]]

# ------------------------------------------------- collisions

def map_collision(offsets):
    """
    Return True if the pawn, after moving with the given offsets, will be out of the board, on a non available cell, or have to pass through walls. Otherwise, return False.
    """
    current_pawn, _ = split_pawns()
    empty_cell = False
    board_limit = False

    if (((current_pawn[0]), (current_pawn[1])), ((current_pawn[0] + offsets[0]), (current_pawn[1] + offsets[1]))) in gs.walls or (((current_pawn[0] + offsets[0]), (current_pawn[1] + offsets[1])), ((current_pawn[0]), (current_pawn[1]))) in gs.walls or (offsets == (-1, 0) and not current_pawn[0] > 0) or (offsets == (1, 0) and not current_pawn[0] < len(gs.board) - 1) or (offsets == (0, -1) and not current_pawn[1] > 0) or (offsets == (0, 1) and not current_pawn[1] < len(gs.board[0]) - 1):
        board_limit = True

    if not board_limit:
        empty_cell = gs.board[current_pawn[0] + offsets[0]][current_pawn[1] + offsets[1]] == "*"

    return empty_cell or board_limit

def pawn_collision(offsets):
    """
    Return True if the pawn, after moving with the given offsets, will be on the same cell as another pawn. Otherwise, return False.
    """
    current_pawn, others_pawns = split_pawns()
    for p in others_pawns.values():
        if p == [current_pawn[0] + offsets[0], current_pawn[1] + offsets[1]]:
            return True
    return False

def remove_unusable_exploration_cells(direction):
    """
    Remove the explorations cells that would collide with another card or the board bounds.
    """
    remove_out_of_bounds_exploration_cells_after_exploring(direction)
    remove_colliders_exploration_cells_after_exploring(direction)
    remove_nearby_explorations_cells_after_exploring(direction)

def remove_nearby_explorations_cells_after_exploring(direction):
    """
    Remove the neighbors explorations cells that would collide with the just added card.
    """
    board = gs.board
    i, j = tuple(map(add, (gs.pawns[gs.current_color][0], gs.pawns[gs.current_color][1]), get_neighbor_top_left_corner_from_explore(direction))) # here, (i, j) are the coordinates of a neighbor top left

    for k in range(4):
        for absolute_x, absolute_y in {(i + k, j - 1), (i + k, j + 4), (i - 1, j + k), (i + 4, j + k)}:
            if absolute_y >= 0 and absolute_y < len(board[0]) and absolute_x >= 0 and absolute_x < len(board) and board[absolute_x][absolute_y][0] == "a":
                board[absolute_x][absolute_y] = "."

def remove_colliders_exploration_cells_after_exploring(direction):
    """
    Remove the exploration cells that would collide with another card in the board.
    """
    board = gs.board
    rel_i, rel_j = tuple(map(add, (gs.pawns[gs.current_color][0], gs.pawns[gs.current_color][1]), get_neighbor_top_left_corner_from_explore(direction))) # here, (i, j) are the coordinates of a neighbor top left

    for off_i in range(4):
        for off_j in range(4):
            i, j = rel_i + off_i, rel_j + off_j

            if board[i][j][0] == "a" and board[i][j][1] != "w":      
                direction = board[i][j][2]
                found_something = False

                off1, off2 = {"l": (-2, -4), "u": (-4, -1), "d": (1, -2), "r": (-1, 1)}[direction]

                for k in range(4):
                    for l in range(4):
                        a = i + off1 + k
                        b = j + off2 + l

                        if a >= 0 and a < len(board) and b >= 0 and b < len(board[0]) and board[a][b] != "*":
                            board[i][j] = "."
                            found_something = True
                            break
                    if found_something:
                        break

def remove_out_of_bounds_exploration_cells_after_exploring(direction):
    """
    Remove the exploration cells that would add a new card beyond the board bounds.
    """
    board = gs.board

    rel_i, rel_j = tuple(map(add, (gs.pawns[gs.current_color][0], gs.pawns[gs.current_color][1]), get_neighbor_top_left_corner_from_explore(direction))) # here, (i, j) are the coordinates of a neighbor top left

    for off_i in range(4):
        for off_j in range(4):
            i, j = rel_i + off_i, rel_j + off_j
    
            if board[i][j][0] == "a" and board[i][j][1] != "w":

                bounds_up_collision = board[i][j][-1] == "u" and (i - 4 < 0 or j + 2 >= len(board[0]))
                bounds_down_collision = board[i][j][-1] == "d" and (i + 4 >= len(board) or j - 2 < 0)
                bounds_left_collision = board[i][j][-1] == "l" and (i - 2 < 0 or j - 4 < 0)
                bounds_right_collision = board[i][j][-1] == "r" and (i + 2 >= len(board) or j + 4 >= len(board[0]))

                if bounds_up_collision or bounds_down_collision or bounds_left_collision or bounds_right_collision:
                    board[i][j] = "."

def remove_all_exploration_cells():
    """
    Remove all the exploration cells from the board.
    """
    board = gs.board
    for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j][0] == "a":
                    board[i][j] = "."

# ------------------------------------------------- save

def make_save():
    """
    Dump the game state into a save.json file.
    """
    with open("save.json", "w") as savefile:
        state = {
            "pawns": gs.pawns,
            "pawns_on_objects": gs.pawns_on_objects,
            "pawns_outside": gs.pawns_outside,
            "current_color": gs.current_color,
            "debug_mode": gs.debug_mode,
            "exit_available": gs.exit_available,
            "start_time": gs.start_time,
            "save_time": time(),
            "board": gs.board,
            "walls": list(gs.walls),
            "escalators": list(gs.escalators),
            "stock": gs.stock,
            "on_board_cards": gs.on_board_cards,
            "telekinesis_times_used": gs.telekinesis_times_used,
            "selected_colors": gs.selected_colors
        }
        dump(state, savefile)

def restore_save():
    """
    Restore a save.json file into the game state.
    """
    with open("save.json", "r") as savefile:
        save = load(savefile)
        gs.pawns = save["pawns"]
        gs.pawns_on_objects = save["pawns_on_objects"]
        gs.pawns_outside = save["pawns_outside"]
        gs.current_color = save["current_color"]
        gs.debug_mode = save["debug_mode"]
        gs.exit_available = save["exit_available"]
        adjust_timer(save["start_time"], save["save_time"], offset = 1)
        gs.board = save["board"]
        gs.escalators = set(map(lambda x: tuple(map(lambda y: tuple(y), x)), save["escalators"]))
        gs.walls = set(map(lambda x: tuple(map(lambda y: tuple(y), x)), save["walls"]))
        gs.stock = save["stock"]
        gs.on_board_cards = save["on_board_cards"]
        gs.telekinesis_times_used = save["telekinesis_times_used"]
        gs.selected_colors = save["selected_colors"]

# ------------------------------------------------- miscellaneous

def get_playing_player(players_count, key):
    """
    Return the player ID corresponding to the used key.
    """
    if players_count == 3:
        one = {"a", "z", "q"}
        two = {"o", "p", "m", "l"}
        three = {"x", "c", "v"}
        if key in one:
            return 1
        elif key in two:
            return 2
        elif key in three:
            return 3
    
    elif players_count == 2:
        one = {"a", "z", "q", "e"}
        two = {"p", "o", "i", "m", "l"}
        if key in one:
            return 1
        elif key in two:
            return 2
    return 1

def split_pawns():
    """
    Remove the pawn corresponding to the given color from the dictionary, and return a tuple with the coordinates of the removed pawn and the pawns dictionary without the removed one.
    """
    current_pawn = gs.pawns[gs.current_color]
    others = gs.pawns.copy()
    others.pop(gs.current_color)
    return current_pawn, others

def opposite_direction(direction):
    """
    Return the opposite direction of the given one. The direction must be one of "up", "down", "left" or "right".
    """
    return {"up": "down", "left": "right", "down": "up", "right": "left"}[direction]

def next_color(player):
    """
    Return the color that comes after the current selected one for the given player.
    """
    colors = cycle(gs.pawns.keys())
    for color in colors:
        if gs.current_color == color:
            gs.selected_colors[player - 1] = next(colors)
            gs.current_color = gs.selected_colors[player - 1]
            return

def apply_debug_mode(touche, mode = "normal"):
    """
    If the debug mode is enabled, return a random action key. Otherwise, return the original key. The optional mode parameter can take the values "normal", "vortex" or "telekinesis", and will influence the keys probabilities to be more efficient. Defaults to normal.
    """
    keys = gs.keys
    if gs.debug_mode and (touche is None or touche.lower() != keys["debug"] and touche.lower() != keys["exit"]):
        if mode == "vortex":
            return choices([keys["exit"], keys["vortex"], next(iter(keys["switch"]))], weights = [1, 3, 3])[0]
        elif mode == "telekinesis":
            return choices([keys["exit"], keys["telekinesis"], next(iter(keys["switch"]))], weights = [1, 3, 3])[0]
        else: # normal case
            return choices([next(iter(keys["up"])), next(iter(keys["left"])), next(iter(keys["down"])), next(iter(keys["right"])), keys["escalator"], keys["vortex"], next(iter(keys["switch"])), keys["explore"], keys["telekinesis"]], weights = [10, 10, 10, 10, 3, 2, 7, 3, 1])[0]
    elif touche is not None:
        return touche.lower()
    else:
        return touche

def spawn_reinforcement_guards():
    """
    Add the reinforcements guards in the game.
    """
    pawns = gs.pawns
    on_board_cards = gs.on_board_cards
    board = gs.board

    for card in on_board_cards:
        x, y = card["top_left"]
        for i in range(4):
            for j in range(4):
                if board[x + i][y + j] == "f2":
                    if not [x + i, y + j] in pawns.values():
                        pawns[f"fake_{len(pawns) - 4}"] = [x + i, y + j]
                    else: # if the first guard is on the spawn cell, the reinforcement guard spawn on a random cell between the nearby ones
                        nearby = list(filter(lambda offsets: offsets[0] < 4 and offsets[0] >= 0 and offsets[1] < 4 and offsets[1] >= 0 and board[x + offsets[0]][y + offsets[1]] != "*", [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]))
                        chosen = choice(nearby)
                        pawns[f"fake_{len(pawns) - 4}"] = [x + chosen[0], y + chosen[1]]
                        return