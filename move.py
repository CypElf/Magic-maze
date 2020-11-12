"""
This module handles the pawns travel across the game board.
"""

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

def exclude_pawn(color, pawns):
    """
    This function remove the pawn corresponding to the given color from the dictionary, and returns a tuple with the coordinates of the removed pawn and the dictionary without the element.
    """
    current_pawn = pawns[color]
    others = pawns.copy()
    others.pop(color)
    return current_pawn, others

def move(color, pawns, pawns_on_objects, pawns_outside, exit_available, board, direction):
    """
    Move the pawn corresponding to the given color up in the board.
    pawns must be a dictionary where the keys are color strings and values their coordinates as a list of 2 elements.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn, others = exclude_pawn(color, pawns)
    
    if current_pawn[0] != -1 and current_pawn[1] != -1:
        pawn_collision = False

        x_change = 0
        y_change = 0
        if direction == "up":
            x_change = -1
            wall_colision = not current_pawn[0] > 0
        elif direction == "down":
            x_change = 1
            wall_colision = not current_pawn[0] < len(board) - 1
        elif direction == "left":
            y_change = -1
            wall_colision = not current_pawn[1] > 0
        else:
            y_change = 1
            wall_colision = not current_pawn[1] < len(board[0]) - 1

        for p in others.values():
            if p == [current_pawn[0] + x_change, current_pawn[1] + y_change]:
                pawn_collision = True

        if not wall_colision and not pawn_collision:
            if not board[current_pawn[0] + x_change][current_pawn[1] + y_change] == "*":
                pawns[color][0] += x_change
                pawns[color][1] += y_change
        
                update_on_objects(color, pawns, pawns_on_objects, board)
                update_on_exit(color, pawns, pawns_outside, exit_available, board)