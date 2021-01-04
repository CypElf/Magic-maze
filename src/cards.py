"""
This module only contains the different game cards that can be added to the game with an exploration.
"""
# See the MM_PrintPlay.pdf file in the "sujet" folder to see the real game cards
# The ones defined below are a litteral conversion in this game's representation

# p = purple object
# o = orange object
# y = yellow object
# g = green object
# h = hourglass
# µ = used hourglass
# . = empty cell
# * = not visitable empty cell
# e = exit
# axy = arrow of color x to the direction y (x can be p/o/y/g/w (w is white, others are the same as above) and y u/d/l/f (for up/down/left/right)), used to explore
# f = fake pawns (aka guards) starting point
# f2 = fake pawns reinforcement (aka guards reinforcements) starting point
# vx = vortex of color x (x can be p/o/y/g)

start_card = {
    "id": 1,
    "board": [
        ["h", ".", "aou", "vp"],
        ["apl", ".", ".", "vy"],
        ["vo", ".", ".", "agr"],
        ["vg", "ayd", ".", "*"]
    ],
    "escalators": {((11, 15), (10, 16))},
	"walls": {
		((8, 12), (8, 13)), ((7, 13), (8, 13)), ((7, 14), (8, 14)), ((7, 16), (8, 16)), ((8, 16), (8, 17)), ((9, 16), (9, 17)), ((10, 12), (10, 13)), ((8, 12), (11, 13)), ((11, 13), (12, 13)), ((11, 15), (12, 15)), ((9, 16), (9, 17)), ((10, 15), (10, 16)), ((9, 16), (10, 16)), ((8, 13), (9, 13)), ((9, 13), (10, 13)), ((10, 13), (11, 13)), ((11, 12), (11, 13))
	},
}

cards = [
    {
        # card 2
        "id": 2,
        "board": [
            ["*", "*", "f", "."],
            ["aol", "*", "*", "e"],
            [".", ".", "*", "*"],
            ["vg", "awu", "vp", "*"]
        ],
        "walls": [
            ((2, -1), (2, 0)), ((3, -1), (3, 0)), ((3, 0), (4, 0)), ((3, 0), (3, 1)), ((3, 2), (4, 2)), ((-1, 2), (0, 2)), ((-1, 3), (0, 3)), ((0, 3), (0, 4)), ((1, 3), (1, 4))
        ],
        "escalator": ((1, 0), (0, 2))
     },
    {
        # card 3
        "id": 3,
        "board": [
            [".", ".", "vo", "*"],
            ["apl", ".", ".", "vg"],
            ["h", ".", ".", "ayr"],
            ["*", "awu", ".", "*"]
        ],
        "walls": [
            ((0, -1), (0, 0)), ((2, -1), (2, 0)), ((-1, 0), (0, 0)), ((-1, 1), (0, 1)), ((-1, 2), (0, 2)), ((3, 2), (4, 2)), ((1, 0), (2, 0)), ((1, 0), (1, 1)), ((2, 1), (3, 1)), ((0, 1), (0, 2)), ((1, 2), (2, 2)), ((1, 3), (1, 4)), ((1, 3), (2, 3))
        ],
        "escalator": None
    },
    {
        # card 4
        "id": 4,
        "board": [
            ["*", "*", "apu", "vy"],
            ["*", "h", ".", "*"],
            ["vo", ".", ".", "agr"],
            ["*", "awu", "*", "*"]
        ],
        "walls": [
            ((-1, 3), (0, 3)), ((0, 3), (0, 4)), ((2, -1), (2, 0)), ((1, 1), (1, 2))
        ],
        "escalator": None
    },
    {
        # card 5
        "id": 5,
        "board": [
            ["f2", ".", "aou", "."],
            ["ayl", ".", "h", "."],
            ["vp", ".", ".", "agr"],
            ["*", "awu", ".", "*"]
        ],
        "walls": [
            ((-1, 0), (0, 0)), ((-1, 1), (0, 1)), ((-1, 3), (0, 3)), ((0, 2), (1, 2)), ((1, 0), (2, 0)), ((2, 1), (3, 1)), ((3, 2), (4, 2)), ((0, -1), (0, 0)), ((2, -1), (2, 0)), ((1, 0), (1, 1)), ((0, 1), (0, 2)), ((1, 1), (1, 2)), ((1, 2), (1, 3)), ((0, 3), (0, 4)), ((1, 3), (1, 4))
        ],
        "escalator": None
    },
    {
        # card 6
        "id": 6,
        "board": [
            ["*", "y", "*", "*"],
            ["agl", ".", ".", "*"],
            ["*", ".", ".", "aor"],
            ["vp", "awu", "*", "*"]
        ],
        "walls": [
            ((-1, 1), (0, 1)), ((1, 1), (2, 1)), ((3, 0), (4, 0)), ((3, -1), (3, 0))
        ],
        "escalator": None
    },
    {
        # card 7
        "id": 7,
        "board": [
            ["*", "*", "o", "*"],
            ["vg", ".", ".", "."],
            ["*", "*", "*", "apr"],
            ["*", "awu", "*", "vy"]
        ],
        "walls": [
            ((-1, 2), (0, 2)), ((3, 3), (4, 3)), ((1, -1), (1, 0)), ((1, 3), (1, 4)), ((3, 3), (3, 4))
        ],
        "escalator": ((3, 1), (1, 2))
    },
    {
        # card 8
        "id": 8,
        "board": [
            [".", ".", ".", "."],
            ["aol", "*", "vy", "."],
            ["*", "*", "*", "apr"],
            ["g", "awu", ".", "."]
        ],
        "walls": [
            ((-1, 0), (0, 0)), ((-1, 1), (0, 1)), ((-1, 2), (0, 2)), ((-1, 3), (0, 3)), ((3, 0), (4, 0)), ((3, 2), (4, 2)), ((3, 3), (4, 3)), ((0, -1), (0, 0)), ((3, -1), (3, 0)), ((1, 2), (1, 3)), ((0, 3), (0, 4)), ((1, 3), (1, 4)), ((3, 3), (3, 4))
        ],
        "escalator": None
    },
    {
        # card 9
        "id": 9,
        "board": [
            [".", ".", ".", "."],
            [".", "*", "vo", "."],
            [".", ".", "*", "ayr"],
            ["*", "awu", "*", "p"]
        ],
        "walls": [
            ((-1, 0), (0, 0)), ((-1, 1), (0, 1)), ((-1, 2), (0, 2)), ((-1, 3), (0, 3)), ((0, 2), (1, 2)), ((3, 3), (4, 3)), ((0, -1), (0, 0)), ((1, -1), (1, 0)), ((2, -1), (2, 0)), ((0, 3), (0, 4)), ((1, 3), (1, 4)), ((3, 3), (3, 4))
        ],
        "escalator": None
    }
]