from upemtk import *
from random import choice
from move import move_up, move_left, move_down, move_right
from display import display_game
from time import monotonic

def main():
	window_width = 800
	window_height = 800
	
	cree_fenetre(window_width, window_height)

	board = [
			[".", "e", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", "g", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", "o", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", "y", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", "r", ".", ".", ".", ".", ".", ".", ".", "."]
		]

	pawns = { "red": [7, 4], "orange": [7, 5], "yellow": [8, 4], "green": [8, 5] }
	pawns_on_objects = { "red": False, "orange": False, "yellow": False, "green": False }
	pawns_outside = { "red": False, "orange": False, "yellow": False, "green": False }

	up_keys = ["up", "z"]
	left_keys = ["left", "q"]
	down_keys = ["down", "s"]
	right_keys = ["right", "d"]

	debug_key = "b"
	escape_key = "escape"

	red_keys = ["ampersand", "1", "r"]
	orange_keys = ["eacute", "2", "o"]
	yellow_keys = ["quotedbl", "3", "y"]
	green_keys = ["quoteright", "4", "g"]

	current_color = "red"
	debug_mode = False
	exit_available = False

	start_time = monotonic()

	lost = False
	won = False

	display_game(pawns["red"], pawns["orange"], pawns["yellow"], pawns["green"], exit_available, board, start_time, window_width, window_height)

	while True:
		touche = attente_touche(50)

		if touche != None or debug_mode:
			if debug_mode and (touche == None or touche.lower() != debug_key and touche.lower() != escape_key):
				current_color = choice(list(pawns.keys()))
				key = choice([up_keys[0], left_keys[0], down_keys[0], right_keys[0]])
			else:
				key = touche.lower()

			if key == escape_key:
				break

			if key == debug_key:
				debug_mode = not debug_mode

			elif key in up_keys:
				move_up(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board)

			elif key in down_keys:
				move_down(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board)
			
			elif key in left_keys:
				move_left(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board)
			
			elif key in right_keys:
				move_right(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board)

			elif key in red_keys:
				current_color = "red"

			elif key in orange_keys:
				current_color = "orange"

			elif key in yellow_keys:
				current_color = "yellow"

			elif key in green_keys:
				current_color = "green"

			if not exit_available and not False in pawns_on_objects.values():
				exit_available = True
			
		lost = (3 * 60 + start_time) - monotonic() <= 0
		won = False not in pawns_outside.values()
		
		efface_tout()

		if lost or won:
			break
		
		display_game(pawns["red"], pawns["orange"], pawns["yellow"], pawns["green"], exit_available, board, start_time, window_width, window_height)
		
	if won:
		texte(window_width / 2, window_height / 2, "You have won!", ancrage = "center")
		mise_a_jour()
		attente_clic()
	
	if lost:
		texte(window_width / 2, window_height / 2, "You have lost!", ancrage = "center")
		mise_a_jour()
		attente_clic()
	
	ferme_fenetre()


if __name__ == "__main__":
	main()