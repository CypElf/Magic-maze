"""
This is the core of the program. It contains the main loop and all the game logic.
"""
from upemtk import *
from random import choice
from time import monotonic
from move import *
from display import *

def main():
	# DO NOT CHANGE THE WIDTH AND HEIGHT, as the entire game is made to render the items to the screen using these values, especially the images
	window_width = 1200
	window_height = 600
	
	game_width = 900
	game_height = 600
	
	cree_fenetre(window_width, window_height)
	display_splash_screen(window_width, window_height)

	board = [
			[".", "e", "*", "*", "*", "*", ".", ".", ".", ".", "*", "*", ".", ".", "."],
			[".", ".", "*", "*", "*", ".", ".", ".", ".", "g", "*", "*", ".", ".", "."],
			["*", ".", ".", ".", ".", ".", ".", ".", "*", "*", "*", "*", ".", ".", "p"],
			["*", "*", ".", ".", ".", ".", ".", ".", "*", "*", ".", "*", ".", "*", "*"],
			["*", "*", "*", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			["*", "*", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			["*", "*", ".", ".", ".", "*", "*", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", "*", "*", ".", "*", "*", ".", ".", "*", "*", "."],
			[".", ".", ".", "*", ".", ".", ".", ".", "*", "*", ".", ".", "*", "y", "."],
			[".", "o", ".", "*", ".", ".", ".", ".", "*", ".", ".", ".", "*", ".", "."],
		]

	pawns = { "purple": [4, 7], "orange": [5, 7], "yellow": [4, 8], "green": [5, 8] }
	pawns_on_objects = { "purple": False, "orange": False, "yellow": False, "green": False }
	pawns_outside = { "purple": False, "orange": False, "yellow": False, "green": False }

	up_keys = ["up", "z"]
	left_keys = ["left", "q"]
	down_keys = ["down", "s"]
	right_keys = ["right", "d"]

	pawn_switch_key = "n"
	debug_key = "b"
	exit_key = "escape"

	purple_keys = ["ampersand", "1", "p"]
	orange_keys = ["eacute", "2", "o"]
	yellow_keys = ["quotedbl", "3", "y"]
	green_keys = ["quoteright", "4", "g"]

	current_color = "purple"
	debug_mode = False
	exit_available = False

	start_time = monotonic()
	print(start_time)

	lost = False
	won = False

	while True:
		touche = attente_touche(50)

		if touche != None or debug_mode:
			if debug_mode and (touche == None or touche.lower() != debug_key and touche.lower() != exit_key):
				current_color = choice(list(pawns.keys()))
				key = choice([up_keys[0], left_keys[0], down_keys[0], right_keys[0]])
			else:
				key = touche.lower()

			if key == exit_key:
				break

			elif key == pawn_switch_key:
				if current_color == "purple":
					current_color = "orange"
				elif current_color == "orange":
					current_color = "yellow"
				elif current_color == "yellow":
					current_color = "green"
				else:
					current_color = "purple"

			elif key == debug_key:
				debug_mode = not debug_mode

			elif key in up_keys:
				move_up(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board)

			elif key in down_keys:
				move_down(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board)
			
			elif key in left_keys:
				move_left(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board)
			
			elif key in right_keys:
				move_right(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board)

			elif key in purple_keys:
				current_color = "purple"

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
		
		if lost or won:
			break
		
		display_game(board, pawns["purple"], pawns["orange"], pawns["yellow"], pawns["green"], current_color, exit_available, start_time, game_width, game_height, window_width, window_height)
		
	if won:
		display_victory(window_width, window_height)
	elif lost: # an elif, not an else, because if the user press escape to close the game while in progress, we don't want to print anything
		display_defeat(window_width, window_height)

	ferme_fenetre()

if __name__ == "__main__":
	main()
