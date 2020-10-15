def move_up(color, pawns, board):
    """
    Move the pawn corresponding to the given color up in the board.
    pawns must be a dictionary where the keys are color strings and values their pawn object.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn = pawns[color]
    collision = False

    others = pawns.copy()
    others.pop(color)
    for _, p in others.items():
        if p.coord() == (current_pawn.x - 1, current_pawn.y):
            collision = True

    if current_pawn.x > 0 and not collision:
        pawns[color].x -= 1

def move_down(color, pawns, board):
    """
    Move the pawn corresponding to the given color down in the board.
    pawns must be a dictionary where the keys are color strings and values their pawn object.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn = pawns[color]
    collision = False

    others = pawns.copy()
    others.pop(color)
    for p in others.values():
        if p.coord() == (current_pawn.x + 1, current_pawn.y):
            collision = True

    if current_pawn.x < len(board) - 1 and not collision:
        pawns[color].x += 1

def move_left(color, pawns, board):
    """
    Move the pawn corresponding to the given color to the left in the board.
    pawns must be a dictionary where the keys are color strings and values their pawn object.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn = pawns[color]
    collision = False

    others = pawns.copy()
    others.pop(color)
    for _, p in others.items():
        if p.coord() == (current_pawn.x, current_pawn.y - 1):
            collision = True

    if current_pawn.y > 0 and not collision:
        pawns[color].y -= 1

def move_right(color, pawns, board):
    """
    Move the pawn corresponding to the given color to the right in the board.
    pawns must be a dictionary where the keys are color strings and values their pawn object.
    color must be a color string usable as a key in pawns.
    board must be a valid 2 dimensional list representing the game.
    """
    current_pawn = pawns[color]
    collision = False

    others = pawns.copy()
    others.pop(color)
    for _, p in others.items():
        if p.coord() == (current_pawn.x, current_pawn.y + 1):
            collision = True

    if current_pawn.y < len(board[0]) - 1 and not collision:
        pawns[color].y += 1