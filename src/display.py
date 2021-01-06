"""
This module contains display functionnalities, used to draw all the user interface to the window.
"""
import src.game_state as gs
from src.upemtk import rectangle, texte, image, mise_a_jour, attente_clic, hauteur_texte, longueur_texte, efface_tout
from src.timer import get_timer

# ------------------------------------------------- start menus

def display_save_loading_menu():
	"""
	Display the menu that allow to choose between starting a new game or loading a previously saved game. Return a list of coordinates as a tuple of 4 elements, corresponding to the coordinates of the clickable areas displayed.
	"""
	efface_tout()
	image(gs.window_width / 2, gs.window_height / 3, "./res/img/misc/magic-maze.png", ancrage = "center")
	zones_coords = []

	for i, txt in enumerate(("Nouvelle partie", "Charger la sauvegarde")):
		x = gs.window_width / 3 * (i + 1)
		y = gs.window_height / 3 * 2.2
		text_width = longueur_texte(txt)
		text_height = hauteur_texte()

		texte(x, y, txt, ancrage = "center")
		zones_coords.append((x - text_width / 2 - 20, y - text_height / 2 - 20, x + text_width / 2 + 20, y + text_height / 2 + 20))
		rectangle(zones_coords[i][0], zones_coords[i][1], zones_coords[i][2], zones_coords[i][3], epaisseur = 2)
	mise_a_jour()
	return zones_coords

def display_loading_save_error():
	"""
	Display an error message that say there is no save available yet.
	"""
	texte(gs.window_width / 2, gs.window_height / 8 * 7, "Vous n'avez pas encore fait de sauvegarde.", ancrage = "center", taille = 16)

def display_players_selection_menu():
	"""
	Display the menu that allow to choose the number of players that will play together. Return a list of coordinates as a tuple of 4 elements, corresponding to the coordinates of the clickable areas displayed.
	"""
	efface_tout()
	image(gs.window_width / 2, gs.window_height / 3, "./res/img/misc/magic-maze.png", ancrage = "center")
	zones_coords = []

	for i in range(1, 4):
		if i > 1:
			text = f"{i} joueurs"
		else:
			text = "solo"
		text_width = longueur_texte(text)
		text_height = hauteur_texte()

		x = gs.window_width / 4 * i
		y = gs.window_height / 3 * 2.2
		texte(x, y, text, ancrage = "center")

		zones_coords.append((x - text_width / 2 - 20, y - text_height / 2 - 20, x + text_width / 2 + 20, y + text_height / 2 + 20))
		rectangle(zones_coords[i - 1][0], zones_coords[i - 1][1], zones_coords[i - 1][2], zones_coords[i - 1][3], epaisseur = 2)
	mise_a_jour()
	return zones_coords

# ------------------------------------------------- controls

def display_controls(player_count, keys):
	"""
	Display the right game controls screen according to the players count.
	"""
	window_width = gs.window_width
	window_height = gs.window_height

	if player_count == 1:
		display_solo_controls()
		click_to_start_y = window_height / 4 * 3
		
	else:
		for j, (txt, font_size) in enumerate([("Contrôles", 26), ("- g : utiliser la télékinésie de l'elfe\n- b : (dés)activer le mode debug\n- échap : mettre en pause", 20)]):
			texte(window_width / 2, window_height / 6 * (j + 1), txt, ancrage = "center", taille = font_size)

		if player_count == 2:
			display_two_players_controls(keys)
		else:
			display_three_players_controls(keys)
		
		click_to_start_y = window_height / 6 * 5

	texte(window_width / 2, click_to_start_y, "Cliquez n'importe où dans la fenêtre pour commencer.", ancrage = "center", taille = 14)
	mise_a_jour()

def display_solo_controls():
	"""
	Display the solo mode controls
	"""
	texte(gs.window_width / 2, gs.window_height / 4, "Contrôles", ancrage = "center", taille = 26)
	texte(gs.window_width / 2, gs.window_height / 4 * 2, "- ZQSD ou ↑←↓→ : se déplacer\n- e : prendre un escalator\n- v : prendre un vortex\n- x : explorer\n- g : utiliser la télékinésie de l'elfe\n- n : switcher de pion\n- b : (dés)activer le mode debug\n- échap : mettre en pause", ancrage = "center", taille = 20)

def display_two_players_controls(keys):
	"""
	Display the 2 players mode controls
	"""
	printables = {action: printable_action for action, printable_action in {("up", "aller en haut"), ("down", "aller en bas"), ("left", "aller à gauche"), ("right", "aller à droite"), ("escalator", "prendre un escalator"), ("vortex", "prendre un vortex"), ("explore", "explorer")}}
	inverted_keys = {v: k for k, v in keys.items() if type(v) is not set}

	for j in {1, 2}:
		texte(gs.window_width / 3 * j, gs.window_height / 6 * 3, f"Joueur {j}", ancrage = "center", taille = 26)
	
	txt_player1 = f"- a : {printables[inverted_keys['a']]}\n- z : {printables[inverted_keys['z']]}\n- e : {printables[inverted_keys['e']]}\n- q"
	txt_player2 = f"- o : {printables[inverted_keys['o']]}\n- p : {printables[inverted_keys['p']]}\n- i : {printables[inverted_keys['i']]}\n- l : {printables[inverted_keys['l']]}\n- m"

	for j, txt in enumerate([txt_player1, txt_player2]):
		texte(gs.window_width / 3 * (j + 1), gs.window_height / 6 * 4, txt + " : switcher de pion", ancrage = "center", taille = 20)

def display_three_players_controls(keys):
	"""
	Display the 3 players mode controls
	"""
	printables = {action: printable_action for action, printable_action in {("up", "aller en haut"), ("down", "aller en bas"), ("left", "aller à gauche"), ("right", "aller à droite"), ("escalator", "prendre un escalator"), ("vortex", "prendre un vortex"), ("explore", "explorer")}}
	inverted_keys = {v: k for k, v in keys.items() if type(v) is not set}

	for j in {1, 2, 3}:
		texte(gs.window_width / 4 * j, gs.window_height / 6 * 3, f"Joueur {j}", ancrage = "center", taille = 26)

	for j, chars in enumerate([["a", "z", "q"], ["x", "c", "v"], ["o", "p", "m", "l"]]):
		txt = f"- {chars[0]} : {printables[inverted_keys[chars[0]]]}\n- {chars[1]} : {printables[inverted_keys[chars[1]]]}\n- {chars[2]} : switcher de pion"
		if j == 2:
			txt += f"\n- {chars[3]} : {printables[inverted_keys[chars[3]]]}"
		texte(gs.window_width / 4 * (j + 1), gs.window_height / 6 * 4, txt, ancrage = "center", taille = 20)

# ------------------------------------------------- pause menus

def display_pause():
	"""
	Display the pause menu
	"""
	game_width = gs.game_width
	game_height = gs.game_height

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

	return pause_rectangle_coords, pause_rectangle_width, pause_rectangle_height, zones_coords

def display_save_success(pause_rectangle_coords, width, height):
	"""
	Display the success save message.
	"""
	texte(pause_rectangle_coords[0] + width / 2, pause_rectangle_coords[1] + height / 8 * 7, "La partie a bien été sauvegardée.", ancrage = "center", taille = 16)

# ------------------------------------------------- game

def display_game():
	"""
	Display the board and the pawns on their positions.
	
	board is supposed to be a valid two dimensional list, with at least 2 rows and 2 columns.
	purple, orange, yellow, green are all supposed to be a list of two elements that describe their position inside the board.
	"""
	board = gs.board
	pawns = gs.pawns
	walls = gs.walls

	rows_count = len(board)
	assert rows_count >= 2, "the specified board does not have enough rows"

	columns_count = len(board[0])
	assert columns_count >= 2, "the specified board does not have enough columns"

	for color in pawns:
		assert pawns[color][0] < rows_count and pawns[color][0] >= -1 and pawns[color][1] < columns_count and pawns[color][1] >= -1, f"{color} position is out of range"

	efface_tout()

	cell_width = gs.cell_width
	cell_height = gs.cell_height

	for i in range(rows_count):
		for j in range(columns_count):
			x = j * cell_width
			y = i * cell_height

			display_cell(i, j, x, y)

			if i > 0 and ((i - 1, j), (i, j)) in walls or ((i, j), (i - 1, j)) in walls:
				rectangle(x, y - 2, x + cell_width, y + 2, remplissage = "grey")
			if j > 0 and ((i, j - 1), (i, j)) in walls or ((i, j), (i, j - 1)) in walls:
				rectangle(x - 2, y, x + 2, y + cell_height, remplissage = "grey")

	display_escalators()
	display_players()
	display_side_panel()
	
	mise_a_jour()

def display_cell(i, j, x, y):
	"""
	Displays the board[i][j] cell to the screen. x and y are the coordinates of the top left of the cell on the screen.
	"""
	board = gs.board

	if board[i][j] == "." or board[i][j] == "*" or board[i][j] == "e" or board[i][j] == "h" or board[i][j] == "µ" or board[i][j][0] == "a":
		if board[i][j] == "." or board[i][j] == "h" or board[i][j] == "µ" or board[i][j][0] == "a":
			color = "white"
		elif board[i][j] == "*":
			color = "grey"
		elif board[i][j] == "e":
			if gs.exit_available:
				color = "lightgreen"
			else:
				color = "white"
		else:
			color = "white"

		rectangle(x, y, x + gs.cell_width, y + gs.cell_height, remplissage = color)

		if board[i][j][0] == "a":
			for color in {"purple", "orange", "yellow", "green"}:
				if color[0] == board[i][j][1]:
					image(x, y, f"./res/img/explore/{color}.png", ancrage = "nw")

	vortex = set()
	if board[i][j][0] == "v":
		if not gs.exit_available:
			vortex = {("vp", "./vortex/purple"), ("vo", "./vortex/orange"), ("vy", "./vortex/yellow"), ("vg", "./vortex/green")}
		else:
			vortex = {(("vp", "vo", "vy", "vg"), "./vortex/grey")}

	for char, img in {("h", "./misc/hourglass"), ("µ", "./misc/used_hourglass"), ("e", "./misc/exit")}.union(vortex):
		if board[i][j] in char:
			image(x, y, f"./res/img/{img}.png", ancrage = "nw")

	else:
		objects = {"purple", "orange", "yellow", "green"}

		if not gs.exit_available:
			for obj in objects:
				if board[i][j] == obj[0]:
					image(x, y, f"./res/img/objects/{obj}.png", ancrage = "nw")
					break
		
		rectangle(x, y, x + gs.cell_width, y + gs.cell_height)

def display_escalators():
	"""
	Display the escalators on the board.
	"""
	offset_x, offset_y, ladder = None, None, None

	for (i1, j1), (i2, j2) in gs.escalators:
		# offset_x and offset_y are used to display the escalator in the right position
		for diff1, diff2, off_x, off_y, lad in {(2, 1, 1, -0.5, 1), (1, 2, 1.5, 0, 3), (-2, 1, 1, 1.5, 2), (2, -1, 0, -0.5, 2), (-1, -2, -0.5, 1, 3), (-2, -1, 0, 1.5, 1), (1, -2, -0.5, 0, 4), (-1, 2, 1.5, 1, 4), (1, 1, 1, 0, 0), (1, -1, 0, 0, 5), (-1, -1, 0, 1, 0), (-1, 1, 1, 1, 5)}:
			if i1 - i2 == diff1 and j2 - j1 == diff2:
				offset_x, offset_y, ladder = off_x, off_y, lad
				break

		image((j1 + offset_x) * gs.cell_width, (i1 + offset_y) * gs.cell_height, f"./res/img/ladders/{ladder}.png", ancrage = "center")

def display_players():
	"""
	Display the players pawns and the guards on the board.
	"""
	for color in gs.pawns.keys():
		if color.startswith("fake"):
			img = "guard"
		else:
			img = color
		image(gs.pawns[color][1] * gs.cell_width, gs.pawns[color][0] * gs.cell_height, f"./res/img/players/{img}.png", ancrage = "nw")

def display_side_panel():
	"""
	Display the game side panel.
	"""
	pawns = gs.pawns

	display_timer()
	timer_height = 80 + hauteur_texte()

	for i, color in enumerate(pawns):
		if color.startswith("fake"):
			img = "guard"
		else:
			img = color

		y = timer_height + (i + 0.25) * ((gs.window_height - timer_height) / len(pawns))
		divs = gs.players_count + 2

		image(gs.game_width + ((gs.window_width - gs.game_width) / divs * (divs - 1)), y, f"./res/img/big_players/{img}.png", ancrage = "center")

		for j in range(gs.players_count):
			if gs.selected_colors[j] == color:
				image(gs.game_width + ((gs.window_width - gs.game_width) / divs * (j + 1)), y, f"./res/img/side_panel_selectors/selector{j + 1}.png", ancrage = "center")

def display_timer():
	"""
	Display the game timer at the top right of the window.
	"""
	texte(gs.game_width + ((gs.window_width - gs.game_width) / 2), 40, "temps restant : " + str(int((get_timer() + 1))), ancrage = "center")

# ------------------------------------------------- selectors

def display_selected_vortex(coords):
	"""
	Display a circle at the given position to show a selected case (vortex selection).
	"""
	x = coords[1] * gs.game_width / len(gs.board[0])
	y = coords[0] * gs.game_height / len(gs.board)

	image(x, y, "./res/img/misc/circle.png", ancrage = "nw")

def display_selected_card(top_left):
	"""
	Display a selector border to a card whose top left corner coordinates are passed as a parameter.
	"""
	image(top_left[1] * gs.cell_width, top_left[0] * gs.cell_height, "./res/img/misc/border.png", ancrage = "nw")

# ------------------------------------------------- miscellaneous

def display_game_end(victory):
	"""
	Display a victory message in the middle of the screen if the victory parameter is set to True, otherwise if it is set to False, a defeat message is displayed.
	"""
	if victory:
		game_state = "gagné"
	else:
		game_state = "perdu"
	efface_tout()
	texte(gs.window_width / 2, gs.window_height / 2, f"Vous avez {game_state} !", ancrage = "center")
	mise_a_jour()
	attente_clic()