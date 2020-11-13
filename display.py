"""
This module contains display functionnalities, used to draw all the user interface to the window.
"""
from upemtk import rectangle, texte, image, mise_a_jour, attente_clic, hauteur_texte, efface_tout
from time import monotonic

def display_game_end(window_width, window_height, victory):
	"""
	Display a victory of defeat message, based on the victory parameter, in the middle of the screen.
	"""
	if victory:
		txt = "gagné"
	else:
		txt = "perdu"
	efface_tout()
	texte(window_width / 2, window_height / 2, f"Vous avez {txt} !", ancrage = "center")
	mise_a_jour()
	attente_clic()

def display_splash_screen(window_width, window_height):
	"""
	Display the game splash screen in the middle of the screen. This splash screen shows the game controls.
	"""
	efface_tout()
	splash_screen_title = "MAGIC MAZE"
	splash_screen_texte = "Mission:\nVous avez 3 minutes pour récupérer tous les objets et vous échapper par la sortie.\n\nContrôles :\n- ZQSD ou ↑←↓→ pour se déplacer\n- POYG ou 1234 pour sélectionner un pion\n- n pour alternativement switcher de pion\n- b pour activer / désactiver le mode debug (actions automatiques aléatoires)\n- échap pour quitter une partie en cours"
	splash_screen_press_to_start = "Cliquez n'importe où pour démarrer le jeu."
	texte(window_width / 2, window_height / 2 - (hauteur_texte() * len(splash_screen_texte.split("\n")) / 1.5), splash_screen_title, ancrage = "center", taille = 26)
	texte(window_width / 2, window_height / 2, splash_screen_texte, ancrage = "center", taille = 16)
	texte(window_width / 2, window_height / 2 + hauteur_texte() * len(splash_screen_texte.split("\n")), splash_screen_press_to_start, ancrage = "center", taille = 12)
	mise_a_jour()
	attente_clic()
	efface_tout()

def display_game(board, pawns, current_color, exit_available, start_time, game_width, game_height, window_width, window_height):
	"""
	Display the board and the pawns on their positions.
	
	board is supposed to be a valid two dimensional list, with at least 2 rows and 2 columns.
	purple, orange, yellow, green are all supposed to be a list of two elements that describe their position inside the board.

	Exemples :

	>>> display_game([], {"purple": [0, 0], "orange": [0, 0], "yellow": [0, 0], "green": [0, 0]}, "purple", True, 300000.0, 900, 600, 1200, 600)
	Traceback (most recent call last):
		...
	AssertionError: the specified board does not have enough rows

	>>> display_game([[], []], {"purple": [0, 0], "orange": [0, 0], "yellow": [0, 0], "green": [0, 0]}, "purple", True, 300000.0, 900, 600, 1200, 600)
	Traceback (most recent call last):
		...
	AssertionError: the specified board does not have enough columns

	>>> display_game([[".", "."], [".", "."]], {"purple": [0, 1], "orange": [1, 0], "yellow": [2,-2], "green": [1, 1]}, "purple", True, 300000.0, 900, 600, 1200, 600)
	Traceback (most recent call last):
		...
	AssertionError: yellow position is out of range
	"""

	rows_count = len(board)
	assert rows_count >= 2, "the specified board does not have enough rows"

	columns_count = len(board[0])
	assert columns_count >= 2, "the specified board does not have enough columns"

	for color in pawns:
		assert pawns[color][0] < rows_count and pawns[color][0] >= -1 and pawns[color][1] < columns_count and pawns[color][1] >= -1, f"{color} position is out of range"

	efface_tout()

	cell_width = game_width / columns_count
	cell_height = game_height / rows_count

	for i in range(rows_count):
		for j in range(columns_count):
			x = j * cell_width
			y = i * cell_height

			if board[i][j] == "." or board[i][j] == "*" or board[i][j] == "e":
				if board[i][j] == ".":
					color = "white"
				elif board[i][j] == "*":
					color = "grey"
				else:
					if exit_available:
						color = "green"
					else:
						color = "white"

				rectangle(x, y, x + cell_width, y + cell_height, remplissage = color)

				if board[i][j] == "e":
					image(x, y, "res/img/misc/exit.png", ancrage = "nw")

			else:
				objects = {"p": "purple", "o": "orange", "y": "yellow", "g": "green"}

				if not exit_available:
					for obj in ["p", "o", "y", "g"]:
						if board[i][j] == obj:
							image(x, y, f"res/img/objects/{objects[obj]}.png", ancrage = "nw")
							break
				
				rectangle(x, y, x + cell_width, y + cell_height)

			for color in ["purple", "orange", "yellow", "green"]:
				if [i, j] == pawns[color]:
					image(x, y, f"res/img/players/{color}.png", ancrage = "nw")
					break

	timer = monotonic()
	texte(window_width - 10, window_height / 20, "temps restant : " + str(int((3 * 60 + start_time + 1) - timer)), ancrage = "ne")

	x_offset = 30

	for i, color in enumerate(["purple", "orange", "yellow", "green"]):
		image(window_width - (window_width - game_width) / 2 + x_offset, window_height / 5 * (i + 1), f"res/img/players/{color}.png", ancrage = "center")

	y_offsets = {"purple": 1, "orange": 2, "yellow": 3, "green": 4}

	image(window_width - (window_width - game_width) / 2 - 1.5 * x_offset, window_height / 5 * y_offsets[current_color], "res/img/misc/arrow.png", ancrage = "center")