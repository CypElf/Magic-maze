"""
This module contains just one function, display_game, used to display the game in the window.
"""
from upemtk import rectangle, texte, image
from time import monotonic

def display_game(purple, orange, yellow, green, exit_available, board, start_time, width, height):
	"""
	Display the board and the pawns on their positions.
	
	board is supposed to be a valid two dimensional list, with at least 2 rows and 2 columns.
	purple, orange, yellow, green are all supposed to be a list of two elements that describe their position inside the board.

	Exemples :

	>>> display_game([0,0], [0,0], [0,0], [0,0], [], 800, 800)
	Traceback (most recent call last):
		...
	AssertionError: the specified board does not have enough rows

	>>> display_game([0,0], [0,0], [0,0], [0,0], [[],[]], 800, 800)
	Traceback (most recent call last):
		...
	AssertionError: the specified board does not have enough columns

	>>> display_game([0,1], [1,0], [2,-2], [1,1], [[".","."],[".","."]], 800, 800)
	Traceback (most recent call last):
		...
	AssertionError: yellow position is out of range
	"""

	rows_count = len(board)
	assert rows_count >= 2, "the specified board does not have enough rows"

	columns_count = len(board[0])
	assert columns_count >= 2, "the specified board does not have enough columns"

	assert purple[0] < rows_count and purple[0] >= -1 and purple[1] < columns_count and purple[1] >= -1, "purple position is out of range"
	assert orange[0] < rows_count and orange[0] >= -1 and orange[1] < columns_count and orange[1] >= -1, "orange position is out of range"
	assert yellow[0] < rows_count and yellow[0] >= -1 and yellow[1] < columns_count and yellow[1] >= -1, "yellow position is out of range"
	assert green[0] < rows_count and green[0] >= -1 and green[1] < columns_count and green[1] >= -1, "green position is out of range"

	cell_width = width / columns_count
	cell_height = height / rows_count

	for i in range(rows_count):
		for j in range(columns_count):
			x = j * cell_width
			y = i * cell_height

			if board[i][j] == "." or board[i][j] == "*" or board[i][j] == "e":
				if board[i][j] == ".":
					color = "white"
					txt = ""
				elif board[i][j] == "*":
					color = "black"
					txt = ""
				else:
					if exit_available:
						color = "green"
					else:
						color = "white"
					txt = "EXIT"

				rectangle(x, y, x + cell_width, y + cell_height, remplissage = color)
				texte(x + cell_width / 2, y + cell_height / 2, txt, ancrage = "center", taille = 19)

			else:
				if board[i][j] == "p":
					image(x, y, "res/img/objects/purple.png", ancrage = "nw")
				elif board[i][j] == "o":
					image(x, y, "res/img/objects/orange.png", ancrage = "nw")
				elif board[i][j] == "y":
					image(x, y, "res/img/objects/yellow.png", ancrage = "nw")
				elif board[i][j] == "g":
					image(x, y, "res/img/objects/green.png", ancrage = "nw")

			if [i, j] == purple:
				image(x, y, "res/img/players/purple.png", ancrage = "nw")
			elif [i, j] == orange:
				image(x, y, "res/img/players/orange.png", ancrage = "nw")
			elif [i, j] == yellow:
				image(x, y, "res/img/players/yellow.png", ancrage = "nw")
			elif [i, j] == green:
				image(x, y, "res/img/players/green.png", ancrage = "nw")

	timer = monotonic()
	texte(width, 0, int((3 * 60 + start_time + 1) - timer), ancrage = "ne")