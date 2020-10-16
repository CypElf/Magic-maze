from upemtk import *
from random import choice
from move import *
from display import display_game
from pawn import *

window_width = 800
window_height = 800

def main():
	cree_fenetre(window_width, window_height)

	board = [
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
		]

	pawns = { "red": pawn(7, 4), "orange": pawn(7, 5), "yellow": pawn(8, 4), "green": pawn(8, 5) }

	up_keys = ["Up", "z"]
	left_keys = ["Left", "q"]
	down_keys = ["Down", "s"]
	right_keys = ["Right", "d"]
	debug_key = "b"

	current_color = "red"
	debug_mode = False

	display_game(pawns["red"], pawns["orange"], pawns["yellow"], pawns["green"], board, window_width, window_height)

	while True:
		touche = attente_touche(200)

		if touche != None or debug_mode:
			if debug_mode and touche != debug_key:
				key = choice([up_keys[0], left_keys[0], down_keys[0], right_keys[0]])
			else:
				key = touche

			if key == "Escape":
				break

			if key == debug_key:
				debug_mode = not debug_mode

			elif key in up_keys:
				move_up(current_color, pawns, board)

			elif key in down_keys:
				move_down(current_color, pawns, board)
			
			elif key in left_keys:
				move_left(current_color, pawns, board)
			
			elif key in right_keys:
				move_right(current_color, pawns, board)

			display_game(pawns["red"], pawns["orange"], pawns["yellow"], pawns["green"], board, window_width, window_height)

	ferme_fenetre()


if __name__ == "__main__":
	main()