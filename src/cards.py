"""
This module only contains the different game cards that can be added to the game with an exploration.
"""
cards = [
    {
        "board": [
            ["*", "*", ".", "."],
            ["aol", "*", "*", "e"],
            [".", ".", "*", "*"],
            ["vg", "awu", "vp", "*"]
        ],
        "walls": {
            ((2, -1), (2, 0)), ((3, -1), (3, 0)), ((3, 0), (4, 0)), ((3, 0), (3, 1)), ((3, 2), (4, 2)), ((-1, 2), (0, 2)), ((-1, 3), (0, 3)), ((0, 3), (0, 4)), ((1, 3), (1, 4))
        },
        "escalator": ((1, 0), (0, 2))
    }
]