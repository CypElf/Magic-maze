from upemtk import *
from random import choice
from move import move_up, move_left, move_down, move_right
from display import display_game

window_width = 800
window_height = 800

def main():
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

	display_game(pawns["red"], pawns["orange"], pawns["yellow"], pawns["green"], exit_available, board, window_width, window_height)

	while True:
		touche = attente_touche(100)

		if touche != None or debug_mode:
			if debug_mode and (touche == None or touche.lower() != debug_key and touche.lower() != escape_key):
				key = choice([up_keys[0], left_keys[0], down_keys[0], right_keys[0]])
			else:
				key = touche.lower()

			if key == escape_key:
				break

			if key == debug_key:
				debug_mode = not debug_mode

			elif key in up_keys:
				move_up(current_color, pawns, pawns_on_objects, board)

			elif key in down_keys:
				move_down(current_color, pawns, pawns_on_objects, board)
			
			elif key in left_keys:
				move_left(current_color, pawns, pawns_on_objects, board)
			
			elif key in right_keys:
				move_right(current_color, pawns, pawns_on_objects, board)

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
			
			efface_tout()
			display_game(pawns["red"], pawns["orange"], pawns["yellow"], pawns["green"], exit_available, board, window_width, window_height)

	ferme_fenetre()


if __name__ == "__main__":
	main()