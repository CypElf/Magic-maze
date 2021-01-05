"""
This is the core of the program. It contains the main loop and the encapsulating game logic.
"""
import json
from os import path
from time import time
import src.game_state as gs
from src.logic import apply_debug_mode, spawn_reinforcement_guards
from src.upemtk import attente_touche_jusqua, cree_fenetre, ferme_fenetre
from src.timer import adjust_time, get_timer
from src.display import display_save_loading_menu, display_players_selection_menu, display_game, display_game_end, display_loading_save_error
from src.keys import key_triggered
from src.menu import handle_players_selection_menu_interaction, handle_save_loading_menu_interaction

def main():
	cree_fenetre(gs.window_width, gs.window_height)
	zones_coords = display_save_loading_menu()
	
	save_loading = handle_save_loading_menu_interaction(zones_coords)
	
	while save_loading and not path.isfile("save.json"):
		display_loading_save_error()
		save_loading = handle_save_loading_menu_interaction(zones_coords)

	zones_coords = display_players_selection_menu()
	keys = handle_players_selection_menu_interaction(zones_coords)

	if save_loading:
		with open("save.json", "r") as savefile:
			save = json.load(savefile)
			gs.pawns = save["pawns"]
			gs.pawns_on_objects = save["pawns_on_objects"]
			gs.pawns_outside = save["pawns_outside"]
			gs.current_color = save["current_color"]
			gs.debug_mode = save["debug_mode"]
			gs.exit_available = save["exit_available"]
			adjust_time(save["start_time"], save["save_time"], offset = 1)
			gs.board = save["board"]
			gs.escalators = set(map(lambda x: tuple(map(lambda y: tuple(y), x)), save["escalators"]))
			gs.walls = set(map(lambda x: tuple(map(lambda y: tuple(y), x)), save["walls"]))
			gs.stock = save["stock"]
			gs.on_board_cards = save["on_board_cards"]
			gs.telekinesis_times_used = save["telekinesis_times_used"]
	else:
		gs.start_time = time()

	while True:
		touche = attente_touche_jusqua(50)

		if touche is not None or gs.debug_mode:
			key = apply_debug_mode(touche, keys)

			key_triggered(key, keys)

			if not gs.exit_available and not False in gs.pawns_on_objects.values():
				gs.exit_available = True
				spawn_reinforcement_guards()
			
		gs.lost = get_timer() <= 0
		gs.won = False not in gs.pawns_outside.values()
		
		if gs.lost or gs.won:
			break
		
		display_game()
		
	if gs.won or gs.lost:
		display_game_end(gs.won)

	ferme_fenetre()

if __name__ == "__main__":
	main()
