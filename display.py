"""
This module contains display functionnalities, used to draw all the user interface to the window.
"""
from upemtk import ferme_fenetre, rectangle, texte, image, mise_a_jour, attente_clic, hauteur_texte, longueur_texte, efface_tout
from time import time
from keys import get_keys

def display_game_end(window_width, window_height, victory):
	"""
	Display a victory of defeat message, based on the victory parameter, in the middle of the screen.
	"""
	if victory:
		game_state = "gagné"
	else:
		game_state = "perdu"
	efface_tout()
	texte(window_width / 2, window_height / 2, f"Vous avez {game_state} !", ancrage = "center")
	mise_a_jour()
	attente_clic()

def display_main_menu(window_width, window_height):
	"""
	Display the game main menu that allow to choose the players count, then shows the according controls.
	Return a keys dictionary that contains the game controls according to the player count.
	"""
	efface_tout()
	
	image(window_width / 2, window_height / 3, "./res/img/misc/magic-maze.png", ancrage = "center")
	zones_coords = []

	for i in range(1, 4):
		if i > 1:
			text = f"{i} joueurs"
		else:
			text = "solo"
		text_width = longueur_texte(text)
		text_height = hauteur_texte()

		x = window_width / 4 * i
		y = window_height / 3 * 2.2
		texte(x, y, text, ancrage = "center")

		zones_coords.append((x - text_width / 2 - 20, y - text_height / 2 - 20, x + text_width / 2 + 20, y + text_height / 2 + 20))
		rectangle(zones_coords[i - 1][0], zones_coords[i - 1][1], zones_coords[i - 1][2], zones_coords[i - 1][3], epaisseur = 2)
	mise_a_jour()

	while True:
		click_x, click_y, _ = attente_clic()
		for i, (x1, y1, x2, y2) in enumerate(zones_coords):
			if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
				efface_tout()

				players_count = i + 1
				keys = get_keys(players_count)

				display_controls(window_width, window_height, players_count, keys)

				return keys

def display_controls(window_width, window_height, player_count, keys):
	"""
	Display the right game controls screen according to the players count.
	"""
	if player_count == 1:
		texte(window_width / 2, window_height / 4, "Contrôles", ancrage = "center", taille = 26)
		texte(window_width / 2, window_height / 4 * 2, "- ZQSD ou ↑←↓→ : se déplacer\n- n : switcher de pion\n- b : (dés)activer le mode debug\n- échap : quitter", ancrage = "center", taille = 20)
		click_to_start_y = window_height / 4 * 3
		
	else:
		for j, (txt, font_size) in enumerate([("Contrôles", 26), ("- b : (dés)activer le mode debug\n- échap : quitter", 20)]):
			texte(window_width / 2, window_height / 6 * (j + 1), txt, ancrage = "center", taille = font_size)

		direction_keys = dict()
		for direction, printable_direction in {("up", "en haut"), ("down", "en bas"), ("left", "à gauche"), ("right", "à droite")}:
			direction_keys[keys[direction]] = printable_direction

		if player_count == 2:
			for j in {1, 2}:
				texte(window_width / 3 * j, window_height / 6 * 3, f"Joueur {j}", ancrage = "center", taille = 26)

			for j, (txt, font_size) in enumerate([(f"- a : aller {direction_keys['a']}\n- z : aller {direction_keys['z']}\n- q : switcher de pion", 20), (f"- o : aller {direction_keys['o']}\n- p : aller {direction_keys['p']}\n- m : switcher de pion", 20)]):
				texte(window_width / 3 * (j + 1), window_height / 6 * 4, txt, ancrage = "center", taille = font_size)
		else:
			for j in {1, 2, 3}:
				texte(window_width / 4 * j, window_height / 6 * 3, f"Joueur {j}", ancrage = "center", taille = 26)

			for j, (txt, font_size) in enumerate([(f"- a : aller {direction_keys['a']}\n- z : switcher de pion", 20), (f"- c : aller {direction_keys['c']}\n- v : switcher de pion", 20), (f"- o : aller {direction_keys['o']}\n- p : aller {direction_keys['p']}\n- m : switcher de pion", 20)]):
				texte(window_width / 4 * (j + 1), window_height / 6 * 4, txt, ancrage = "center", taille = font_size)
		
		click_to_start_y = window_height / 6 * 5

	texte(window_width / 2, click_to_start_y, "Cliquez n'importe où dans la fenêtre pour commencer.", ancrage = "center", taille = 14)
	mise_a_jour()
	attente_clic()

def display_pause(game_width, game_height):
	pause_rectangle_width = game_width / 5 * 4 - game_width / 5
	pause_rectangle_height = game_height / 4 * 3 - game_height / 4
	pause_rectangle_coords = (game_width / 5, game_height / 4, game_width / 5 + pause_rectangle_width, game_height / 4 + pause_rectangle_height)

	rectangle(pause_rectangle_coords[0], pause_rectangle_coords[1], pause_rectangle_coords[2], pause_rectangle_coords[3], remplissage = "white", epaisseur = 2)
	texte(pause_rectangle_coords[0] + pause_rectangle_width / 2, pause_rectangle_coords[1] + pause_rectangle_height / 4, "PAUSE", ancrage = "center", taille = 36)

	zones_coords = set()

	for i, txt in {(1, "sauvegarder"), (2.5, "quitter")}:
		x = pause_rectangle_coords[0] + pause_rectangle_width / 3.5 * i
		y = pause_rectangle_coords[1] + pause_rectangle_height / 4 * 2.5
		rectangle(x - 100, y - 40, x + 100, y + 40)
		texte(x, y, txt, ancrage = "center")
		zones_coords.add((x - 100, y - 40, x + 100, y + 40, txt))

	unpaused = False
	while not unpaused:
		click_x, click_y, _ = attente_clic()
		for i, (x1, y1, x2, y2, txt) in enumerate(zones_coords):
			if click_x >= x1 and click_x <= x2 and click_y >= y1 and click_y <= y2:
				if txt == "quitter":
					ferme_fenetre()
					exit(0)
				else:
					# TODO : save the game state in a file
					pass
			elif not (click_x >= pause_rectangle_coords[0] and click_x <= pause_rectangle_coords[2] and click_y >= pause_rectangle_coords[1] and click_y <= pause_rectangle_coords[3]):
				unpaused = True

def display_game(board, pawns, current_color, exit_available, walls, start_time, timeout, game_width, game_height, window_width, window_height):
	"""
	Display the board and the pawns on their positions.
	
	board is supposed to be a valid two dimensional list, with at least 2 rows and 2 columns.
	purple, orange, yellow, green are all supposed to be a list of two elements that describe their position inside the board.

	Exemples :

	>>> display_game([], {"purple": [0, 0], "orange": [0, 0], "yellow": [0, 0], "green": [0, 0]}, "purple", True, {((0, 0), (0, 1))}, 300000.0, 3, 900, 600, 1200, 600)
	Traceback (most recent call last):
		...
	AssertionError: the specified board does not have enough rows

	>>> display_game([[], []], {"purple": [0, 0], "orange": [0, 0], "yellow": [0, 0], "green": [0, 0]}, "purple", True, {((0, 0), (0, 1))}, 300000.0, 3, 900, 600, 1200, 600)
	Traceback (most recent call last):
		...
	AssertionError: the specified board does not have enough columns

	>>> display_game([[".", "."], [".", "."]], {"purple": [0, 1], "orange": [1, 0], "yellow": [2,-2], "green": [1, 1]}, "purple", True, {((0, 0), (0, 1))}, 300000.0, 3, 900, 600, 1200, 600)
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

			display_cell(board, i, j, x, y, cell_width, cell_height, exit_available)

			for color in {"purple", "orange", "yellow", "green"}:
				if [i, j] == pawns[color]:
					image(x, y, f"res/img/players/{color}.png", ancrage = "nw")
					break

			if i > 0 and {(i - 1, j), (i, j)} in walls:
				rectangle(x, y - 2, x + cell_width, y + 2, remplissage = "grey")

	texte(window_width - 10, window_height / 20, "temps restant : " + str(int((timeout * 60 + start_time + 1) - time())), ancrage = "ne")
	display_side_panel(window_width, window_height, game_width, current_color)

def display_cell(board, i, j, x, y, cell_width, cell_height, exit_available):
	"""
	Displays the board[i][j] cell to the screen. x and y are the coordinates of the top left of the cell on the screen.
	"""
	if board[i][j] == "." or board[i][j] == "*" or board[i][j] == "e" or board[i][j] == "h" or board[i][j] == "µ":
		if board[i][j] == "." or board[i][j] == "h" or board[i][j] == "µ":
			color = "white"
		elif board[i][j] == "*":
			color = "grey"
		else:
			if exit_available:
				color = "lightgreen"
			else:
				color = "white"

		rectangle(x, y, x + cell_width, y + cell_height, remplissage = color)

		for char, img in {("h", "hourglass"), ("µ", "used_hourglass"), ("e", "exit")}:
			if board[i][j] == char:
				image(x, y, f"res/img/misc/{img}.png", ancrage = "nw")

	else:
		objects = {"p": "purple", "o": "orange", "y": "yellow", "g": "green"}

		if not exit_available:
			for obj in {"p", "o", "y", "g"}:
				if board[i][j] == obj:
					image(x, y, f"res/img/objects/{objects[obj]}.png", ancrage = "nw")
					break
		
		rectangle(x, y, x + cell_width, y + cell_height)

def display_side_panel(window_width, window_height, game_width, current_color):
	x_offset = 30

	for i, color in enumerate(["purple", "orange", "yellow", "green"]):
		image(window_width - (window_width - game_width) / 2 + x_offset, window_height / 5 * (i + 1), f"res/img/players/{color}.png", ancrage = "center")

	y_offsets = {"purple": 1, "orange": 2, "yellow": 3, "green": 4}

	image(window_width - (window_width - game_width) / 2 - 1.5 * x_offset, window_height / 5 * y_offsets[current_color], "res/img/misc/arrow.png", ancrage = "center")