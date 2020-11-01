"""
This module handles the pawns travel across the game board.
"""

def update_on_objects(color, pawns, pawns_on_objects, board):
    """
    Update the pawns_on_objects dictionary provided using the new pawns coordinates.
    """
    if board[pawns[color][0]][pawns[color][1]] == color[0:1]:
        pawns_on_objects[color] = True
    else:
        pawns_on_objects[color] = False


def update_on_exit(color, pawns, pawns_outside, exit_available, board):
    """
    Update the pawns_outside dictionary provided using the new pawns coordinates.
    """
    if exit_available and board[pawns[color][0]][pawns[color][1]] == "e":
        pawns_outside[color] = True
        pawns[color] = [-1,-1]

def exclude_pawn(color, pawns):
    """
    This function remove the pawn corresponding to the given color from the dictionary, and returns a tuple with the coordinates of the removed pawn and the dictionary without the element.
    """
    current_pawn = pawns[color]
    others = pawns.copy()
    others.pop(color)
    return current_pawn, others

def move_up(color, pawns, pawns_on_objects, pawns_outside, exit_available, board):
    """
    Move the pawn corresponding to the given color up in the board.
    pawns must be a dictionary where the keys are color strings and values their coordinates as a list of 2 elements.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn, others = exclude_pawn(color, pawns)
    if current_pawn[0] != -1 and current_pawn[1] != -1:
        pawn_collision = False

        for p in others.values():
            if p == [current_pawn[0] - 1, current_pawn[1]]:
                pawn_collision = True

        if current_pawn[0] > 0 and not pawn_collision:
            if not board[current_pawn[0] - 1][current_pawn[1]] == "*":
                pawns[color][0] -= 1
        
        update_on_objects(color, pawns, pawns_on_objects, board)
        update_on_exit(color, pawns, pawns_outside, exit_available, board)

def move_down(color, pawns, pawns_on_objects, pawns_outside, exit_available, board):
    """
    Move the pawn corresponding to the given color down in the board.
    pawns must be a dictionary where the keys are color strings and values their coordinates as a list of 2 elements.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn, others = exclude_pawn(color, pawns)
    if current_pawn[0] != -1 and current_pawn[1] != -1:
        pawn_collision = False

        for p in others.values():
            if p == [current_pawn[0] + 1, current_pawn[1]]:
                pawn_collision = True

        if current_pawn[0] < len(board) - 1 and not pawn_collision:
            if not board[current_pawn[0] + 1][current_pawn[1]] == "*":
                pawns[color][0] += 1

    update_on_objects(color, pawns, pawns_on_objects, board)
    update_on_exit(color, pawns, pawns_outside, exit_available, board)

def move_left(color, pawns, pawns_on_objects, pawns_outside, exit_available, board):
    """
    Move the pawn corresponding to the given color to the left in the board.
    pawns must be a dictionary where the keys are color strings and values their coordinates as a list of 2 elements.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn, others = exclude_pawn(color, pawns)
    if current_pawn[0] != -1 and current_pawn[1] != -1:
        pawn_collision = False

        for p in others.values():
            if p == [current_pawn[0], current_pawn[1] - 1]:
                pawn_collision = True

        if current_pawn[1] > 0 and not pawn_collision:
            if not board[current_pawn[0]][current_pawn[1] - 1] == "*":
                pawns[color][1] -= 1

        update_on_objects(color, pawns, pawns_on_objects, board)
        update_on_exit(color, pawns, pawns_outside, exit_available, board)

def move_right(color, pawns, pawns_on_objects, pawns_outside, exit_available, board):
    """
    Move the pawn corresponding to the given color to the right in the board.
    pawns must be a dictionary where the keys are color strings and values their coordinates as a list of 2 elements.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn, others = exclude_pawn(color, pawns)
    if current_pawn[0] != -1 and current_pawn[1] != -1:
        pawn_collision = False

        for p in others.values():
            if p == [current_pawn[0], current_pawn[1] + 1]:
                pawn_collision = True

        if current_pawn[1] < len(board[0]) - 1 and not pawn_collision:
            if not board[current_pawn[0]][current_pawn[1] + 1] == "*":
                pawns[color][1] += 1

        update_on_objects(color, pawns, pawns_on_objects, board)
        update_on_exit(color, pawns, pawns_outside, exit_available, board)