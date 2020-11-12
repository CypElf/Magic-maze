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
	keys = get_keys_dico()

	current_color = "purple"
	debug_mode = False
	exit_available = False

	start_time = monotonic()

	lost = False
	won = False

	while True:
		touche = attente_touche(50)

		if touche != None or debug_mode:
			if debug_mode and (touche == None or touche.lower() != keys["debug"] and touche.lower() != keys["exit"]):
				current_color = choice(list(pawns.keys()))
				key = choice([keys["up"][0], keys["left"][0], keys["down"][0], keys["right"][0]])
			else:
				key = touche.lower()

			up = key in keys["up"]
			down = key in keys["down"]
			left = key in keys["left"]
			right = key in keys["right"]

			if up or down or left or right:
				if up:
					direction = "up"
				elif down:
					direction = "down"
				elif left:
					direction = "left"
				elif right:
					direction = "right"

				move(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board, direction)

			elif key == keys["exit"]:
				break

			elif key == keys["switch"]:
				current_color = next_color(current_color)

			elif key == keys["debug"]:
				debug_mode = not debug_mode

			elif key in keys["purple"]:
				current_color = "purple"

			elif key in keys["orange"]:
				current_color = "orange"

			elif key in keys["yellow"]:
				current_color = "yellow"

			elif key in keys["green"]:
				current_color = "green"

			if not exit_available and not False in pawns_on_objects.values():
				exit_available = True
			
		lost = (3 * 60 + start_time) - monotonic() <= 0
		won = False not in pawns_outside.values()
		
		if lost or won:
			break
		
		display_game(board, pawns, current_color, exit_available, start_time, game_width, game_height, window_width, window_height)
		
	if won:
		display_victory(window_width, window_height)
	elif lost: # an elif, not an else, because if the user press escape to close the game while in progress, we don't want to print anything
		display_defeat(window_width, window_height)

	ferme_fenetre()

def get_keys_dico():
	return {"up": ["up", "z"], "left": ["left", "q"], "down": ["down", "s"], "right": ["right", "d"], "switch": "n", "debug": "b", "exit": "escape", "purple": ["ampersand", "1", "p"], "orange":  ["eacute", "2", "o"], "yellow": ["quotedbl", "3", "y"], "green": ["quoteright", "4", "g"]}

def next_color(current_color):
	if current_color == "purple":
		return "orange"
	elif current_color == "orange":
		return "yellow"
	elif current_color == "yellow":
		return "green"
	else:
		return "purple"

if __name__ == "__main__":
	main()
