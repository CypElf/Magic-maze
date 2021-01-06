"""
This module contains display functionnalities, used to draw all the user interface to the window.
"""
import src.game_state as gs
from src.timer import get_timer
from src.upemtk import rectangle, texte, image, mise_a_jour, attente_clic, hauteur_texte, longueur_texte, efface_tout

# ------------------------------------------------- start menus

def display_save_loading_menu():
	"""
	Display the menu that allow to choose between starting a new game or loading a previously saved game. Return a list of coordinates as tuples that represent the clickable areas of the menu.
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
	Display the menu that allow to choose the number of players that will play together. Return a list of coordinates as tuples that represent the clickable areas of the menu.
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

def display_controls():
	"""
	Display the right game controls screen according to the players count.
	"""
	pc = gs.players_count
	window_width = gs.window_width
	window_height = gs.window_height

	efface_tout()

	printables = get_printables_actions()

	texte(window_width / 2, window_height / 8, "CONTROLES", ancrage = "center", taille = 28)

	common_controls = []
	for char in {"g", "b", "escape"}:
		common_controls.append(f"- {char} : {printables[get_action(char)]}")
	
	texte(window_width / 2, window_height / 8 * 2.5, "\n".join(common_controls), ancrage = "center", taille = 20)

	if pc == 1:
		player_keys = [("e", "v", "x", "n")]
	elif pc == 2:
		player_keys = [("a", "z", "e", "q"), ("o", "p", "i", "l", "m")]
	else:
		player_keys = [("a", "z", "q"), ("x", "c", "v"), ("o", "p", "m", "l")]

	for j in range(1, pc + 1):
		texte(gs.window_width / (pc + 1) * j, gs.window_height / 6 * 3, f"Joueur {j}", ancrage = "center", taille = 26)
	
	players_actions = []

	for chars in player_keys:
		players_actions.append([])
		for char in chars:
			players_actions[-1].append(f"- {char} : {printables[get_action(char)]}")

	for j, actions in enumerate(players_actions):
		txt = "\n".join(actions)
		texte(gs.window_width / (pc + 1) * (j + 1), gs.window_height / 6 * 4, txt, ancrage = "center", taille = 20)

	texte(window_width / 2, window_height / 6 * 5.5, "Cliquez n'importe où dans la fenêtre pour continuer.", ancrage = "center", taille = 14)
	mise_a_jour()

def get_action(key):
	"""
	Return the action that the key is poiting to in the keys.
	"""
	for k, v in gs.keys.items():
		if type(v) is str and key == v or type(v) is set and key in v:
			return k

def get_printables_actions():
	"""
	Return a dictionary whose keys are actions and values are text describing the action that can be displayed to the user.
	"""
	return {
		"move": "se déplacer", # not a real action, but used when playing in solo to display movement controls in one line instead of a separated line for each direction
		"up": "aller en haut",
		"down": "aller en bas",
		"left": "aller à gauche",
		"right": "aller à droite",
		"escalator": "prendre un escalator",
		"vortex": "prendre un vortex",
		"explore": "explorer",
		"telekinesis": "utiliser la télékinésie de l'elfe",
		"switch": "switcher de personnage",
		"debug": "(dés)activer le mode debug",
		"exit": "mettre en pause"
	}

# ------------------------------------------------- pause menu

def display_pause():
	"""
	Display the pause menu. Return a list of coordinates as tuples that represent the clickable areas of the menu.
	"""
	game_width = gs.game_width
	game_height = gs.game_height

	pause_rectangle_width = 720
	pause_rectangle_height = 500

	pause_rectangle_coords = (game_width / 2) - (pause_rectangle_width / 2), (game_height / 2) - (pause_rectangle_height / 2), (game_width / 2) + (pause_rectangle_width / 2), (game_height / 2) + (pause_rectangle_height / 2)

	rectangle(pause_rectangle_coords[0], pause_rectangle_coords[1], pause_rectangle_coords[2], pause_rectangle_coords[3], remplissage = "white", epaisseur = 2)
	texte(pause_rectangle_coords[0] + pause_rectangle_width / 2, pause_rectangle_coords[1] + pause_rectangle_height / 5, "PAUSE", ancrage = "center", taille = 36)

	zones_coords = set()

	option_rectangle_width = 200
	option_rectangle_height = 80

	for offset_x, offset_y, txt in {(1, 2, "sauvegarder"), (2.5, 2, "contrôles"), (3.5 / 2, 2.8, "quitter")}:
		x = pause_rectangle_coords[0] + pause_rectangle_width / 3.5 * offset_x
		y = pause_rectangle_coords[1] + pause_rectangle_height / 4 * offset_y			

		rectangle(x - option_rectangle_width / 2, y - option_rectangle_height / 2, x + option_rectangle_width / 2, y + option_rectangle_height / 2)
		texte(x, y, txt, ancrage = "center")
		zones_coords.add((x - option_rectangle_width / 2, y - option_rectangle_height / 2, x + option_rectangle_width / 2, y + option_rectangle_height / 2, txt))

	return pause_rectangle_coords, zones_coords

def display_save_success(pause_rectangle_coords, width, height):
	"""
	Display a successful save message.
	"""
	texte(pause_rectangle_coords[0] + width / 2, pause_rectangle_coords[1] + height / 8 * 7, "La partie a bien été sauvegardée.", ancrage = "center", taille = 16)

# ------------------------------------------------- game

def display_game(timer = None):
	"""
	Display the whole game to the screen.
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
			display_cell((i, j))

			if i > 0 and ((i - 1, j), (i, j)) in walls or ((i, j), (i - 1, j)) in walls:
				rectangle(j * cell_width, i * cell_height - 2, j * cell_width + cell_width, i * cell_height + 2, remplissage = "grey")
			if j > 0 and ((i, j - 1), (i, j)) in walls or ((i, j), (i, j - 1)) in walls:
				rectangle(j * cell_width - 2, i * cell_height, j * cell_width + 2, i * cell_height + cell_height, remplissage = "grey")

	display_escalators()
	display_players()
	display_side_panel(timer)
	
	mise_a_jour()

def display_cell(coords):
	"""
	Display the cell at the given coordinates to the screen.
	"""
	board = gs.board

	i, j = coords
	x, y = j * gs.cell_width, i * gs.cell_height

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

def display_side_panel(timer = None):
	"""
	Display the game side panel next to the board.
	"""
	pawns = gs.pawns

	display_timer(timer)
	timer_height = 80 + hauteur_texte()
	telekinesis_stock_height = timer_height

	for i, color in enumerate(pawns):
		if color.startswith("fake"):
			img = "guard"
		else:
			img = color

		y = timer_height + (i + 0.5) * (((gs.window_height - telekinesis_stock_height) - timer_height) / len(pawns))
		divs = gs.players_count + 2

		image(gs.game_width + ((gs.window_width - gs.game_width) / divs * (divs - 1)), y, f"./res/img/big_players/{img}.png", ancrage = "center")

		for j in range(gs.players_count):
			if gs.selected_colors[j] == color:
				image(gs.game_width + ((gs.window_width - gs.game_width) / divs * (j + 1)), y, f"./res/img/side_panel_selectors/selector{j + 1}.png", ancrage = "center")

		display_telekinesis_stock()

def display_timer(timer = None):
	"""
	Display the game timer at the top of the side panel. If a timer parameter is specified, display it instead of the game one.
	"""
	if timer is None:
		timer = get_timer() + 1

	texte(gs.game_width + ((gs.window_width - gs.game_width) / 2), 40, "Temps restant : " + str(int(timer)), ancrage = "center")

def display_telekinesis_stock():
	"""
	Display the number of times the telekinesis power can still be used at the bottom of the side panel.
	"""
	texte(gs.game_width + ((gs.window_width - gs.game_width) / 2), gs.window_height - 40, f"Télékinésie : {2 - gs.telekinesis_times_used} / 2", ancrage = "center")

# ------------------------------------------------- selectors

def display_selected_vortex(coords):
	"""
	Display a circle at the given coordinates to show a selected cell.
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
	Display a victory message in the middle of the screen if the victory parameter is set to True. Otherwise, display a defeat message.
	"""
	efface_tout()
	if victory:
		image(0, 0, "./res/img/misc/success_background.png", ancrage = "nw")
		color = "green"
		game_state = "gagné"
	else:
		color = "red"
		game_state = "perdu"
	texte(gs.window_width / 2, gs.window_height / 2, f"Vous avez {game_state} !", ancrage = "center", taille = 34, couleur = color)
	mise_a_jour()
	attente_clic()