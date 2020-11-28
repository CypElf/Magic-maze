"""
This is the core of the program. It contains the main loop and all the game logic.
"""
from upemtk import *
from random import choice
from time import time
from display import display_main_menu, display_game, display_game_end
from keys import key_triggered

def main():
	# DO NOT CHANGE THE WIDTH AND HEIGHT, as the entire game is made to render the items to the screen using these values, especially the images
	window_width = 1200
	window_height = 600
	
	game_width = 900
	game_height = 600
	
	cree_fenetre(window_width, window_height)
	keys = display_main_menu(window_width, window_height)

	board = [
			[".", "e", "*", "*", "*", "*", ".", ".", ".", ".", "*", "*", ".", ".", "."],
			[".", ".", "*", "*", "*", ".", ".", ".", ".", "g", "*", "*", "h", ".", "."],
			["*", ".", ".", ".", "h", ".", ".", ".", "*", "*", "*", "*", ".", ".", "p"],
			["*", "*", ".", ".", ".", ".", ".", ".", "*", "*", ".", "*", ".", "*", "*"],
			["*", "*", "*", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			["*", "*", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			["*", "*", ".", ".", ".", "*", "*", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", "*", "*", ".", "*", "*", ".", ".", "*", "*", "."],
			[".", ".", "h", "*", ".", ".", ".", ".", "*", "*", "h", ".", "*", "y", "."],
			[".", "o", ".", "*", ".", ".", ".", ".", "*", ".", ".", ".", "*", ".", "."],
		]

	walls = {frozenset(((3, 5), (4, 5))), frozenset(((3, 6), (4, 6))), frozenset(((3, 7), (4, 7))), frozenset(((8, 1), (9, 1))), frozenset(((8, 2), (9, 2)))}
	pawns = { "purple": [4, 7], "orange": [5, 7], "yellow": [4, 8], "green": [5, 8] }
	pawns_on_objects = { "purple": False, "orange": False, "yellow": False, "green": False }
	pawns_outside = { "purple": False, "orange": False, "yellow": False, "green": False }

	current_color = "purple"
	debug_mode = False
	exit_available = False

	start_time = time()
	timeout = 3 # timeout is in minutes

	lost = False
	won = False

	while True:
		touche = attente_touche(50)

		if touche != None or debug_mode:
			if debug_mode and (touche == None or touche.lower() != keys["debug"] and touche.lower() != keys["exit"]):
				current_color = choice(list(pawns.keys()))
				key = choice([next(iter(keys["up"])), next(iter(keys["left"])), next(iter(keys["down"])), next(iter(keys["right"]))])
			else:
				key = touche.lower()

			current_color, hourglass_returned, debug_mode, (paused, returned_time) = key_triggered(key, keys, current_color, pawns, pawns_on_objects, pawns_outside, exit_available, start_time, debug_mode, walls, board, game_width, game_height)

			if paused:
				start_time = returned_time

			if not exit_available and not False in pawns_on_objects.values():
				exit_available = True

			if hourglass_returned:
				now = time()
				start_time = now - (timeout * 60 + start_time - now) - 1
			
		lost = timeout * 60 + start_time - time() <= 0
		won = False not in pawns_outside.values()
		
		if lost or won:
			break
		
		display_game(board, pawns, current_color, exit_available, walls, start_time, timeout, game_width, game_height, window_width, window_height)
		
	if won or lost:
		display_game_end(window_width, window_height, won)

	ferme_fenetre()

if __name__ == "__main__":
	main()
