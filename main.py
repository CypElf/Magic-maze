"""
This is the core of the program. It contains the main loop and all the game logic.
"""
import json
from os import path
from time import time
from src.logic import apply_debug_mode
from src.upemtk import attente_touche_jusqua, cree_fenetre, ferme_fenetre
from src.timer import invert_hourglass, adjust_time, get_timer
from src.display import display_save_loading_menu, display_players_selection_menu, display_game, display_game_end, display_loading_save_error
from src.keys import key_triggered
from src.menu import handle_players_selection_menu_interaction, handle_save_loading_menu_interaction
from src.cards import start_card, cards

def main():
	# DO NOT CHANGE THE WIDTH AND HEIGHT, as the entire game is made to render the items to the screen using these values, especially the images	
	window_width = 1500
	window_height = 800

	game_width = 1200
	game_height = 800

	cree_fenetre(window_width, window_height)
	zones_coords = display_save_loading_menu(window_width, window_height)
	
	save_loading = handle_save_loading_menu_interaction(zones_coords)
	
	while save_loading and not path.isfile("save.json"):
		display_loading_save_error(window_width, window_height)
		save_loading = handle_save_loading_menu_interaction(zones_coords)

	zones_coords = display_players_selection_menu(window_width, window_height)
	keys = handle_players_selection_menu_interaction(zones_coords, window_width, window_height)

	if save_loading:
		with open("save.json", "r") as savefile:
			save = json.load(savefile)
			pawns = save["pawns"]
			pawns_on_objects = save["pawns_on_objects"]
			pawns_outside = save["pawns_outside"]
			current_color = save["current_color"]
			debug_mode = save["debug_mode"]
			exit_available = save["exit_available"]
			start_time = adjust_time(save["start_time"], save["save_time"]) + 1
			board = save["board"]
			escalators = set(map(lambda x: tuple(map(lambda y: tuple(y), x)), save["escalators"]))
			walls = set(map(lambda x: tuple(map(lambda y: tuple(y), x)), save["walls"]))
			stock = save["stock"]
	else:
		stock = cards
		escalators = start_card["escalators"]
		walls = start_card["walls"]

		board = [["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30] + list(map(lambda row: ["*"] * 13 + row + ["*"] * 13, start_card["board"])) + [["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30]

		pawns = { "purple": [9, 14], "orange": [10, 14], "yellow": [9, 15], "green": [10, 15] }
		pawns_on_objects = {"purple": False, "orange": False, "yellow": False, "green": False}
		pawns_outside = pawns_on_objects.copy()
		current_color = "purple"
		debug_mode = False
		exit_available = False
		start_time = time()
	timeout = 3 # timeout is in minutes

	lost = False
	won = False

	while True:
		touche = attente_touche_jusqua(50)

		if touche is not None or debug_mode:
			key = apply_debug_mode(touche, keys, debug_mode)

			current_color, hourglass_returned, debug_mode, (paused, returned_time) = key_triggered(key, keys, current_color, pawns, pawns_on_objects, pawns_outside, exit_available, start_time, timeout, debug_mode, walls, escalators, stock, board, game_width, game_height, window_width, window_height)

			if paused:
				start_time = returned_time

			if not exit_available and not False in pawns_on_objects.values():
				exit_available = True

			if hourglass_returned:
				start_time = invert_hourglass(start_time, timeout)
			
		lost = get_timer(start_time, timeout) <= 0
		won = False not in pawns_outside.values()
		
		if lost or won:
			break
		
		display_game(board, pawns, current_color, exit_available, walls, escalators, start_time, timeout, game_width, game_height, window_width, window_height)
		
	if won or lost:
		display_game_end(window_width, window_height, won)

	ferme_fenetre()

if __name__ == "__main__":
	main()
