def move_up(color, pawns, board):
    """
    Move the pawn corresponding to the given color up in the board.
    pawns must be a dictionary where the keys are color strings and values their coordinates as a list of 2 elements.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn = pawns[color]
    collision = False

    others = pawns.copy()
    others.pop(color)
    for p in others.values():
        if p == [current_pawn[0] - 1, current_pawn[1]]:
            collision = True

    if current_pawn[0] > 0 and not collision:
        pawns[color][0] -= 1

def move_down(color, pawns, board):
    """
    Move the pawn corresponding to the given color down in the board.
    pawns must be a dictionary where the keys are color strings and values their coordinates as a list of 2 elements.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn = pawns[color]
    collision = False

    others = pawns.copy()
    others.pop(color)
    for p in others.values():
        if p == [current_pawn[0] + 1, current_pawn[1]]:
            collision = True

    if current_pawn[0] < len(board) - 1 and not collision:
        pawns[color][0] += 1

def move_left(color, pawns, board):
    """
    Move the pawn corresponding to the given color to the left in the board.
    pawns must be a dictionary where the keys are color strings and values their coordinates as a list of 2 elements.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn = pawns[color]
    collision = False

    others = pawns.copy()
    others.pop(color)
    for p in others.values():
        if p == [current_pawn[0], current_pawn[1] - 1]:
            collision = True

    if current_pawn[1] > 0 and not collision:
        pawns[color][1] -= 1

def move_right(color, pawns, board):
    """
    Move the pawn corresponding to the given color to the right in the board.
    pawns must be a dictionary where the keys are color strings and values their coordinates as a list of 2 elements.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn = pawns[color]
    collision = False

    others = pawns.copy()
    others.pop(color)
    for p in others.values():
        if p == [current_pawn[0], current_pawn[1] + 1]:
            collision = True

    if current_pawn[1] < len(board[0]) - 1 and not collision:
        pawns[color][1] += 1