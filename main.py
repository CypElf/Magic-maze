"""
This is the program entry point. It contains the encapsulating code.
"""
from os import path
from time import time

import src.game_state as gs
from src.logic import apply_debug_mode, spawn_reinforcement_guards, restore_save, get_playing_player
from src.upemtk import attente_touche_jusqua, cree_fenetre, ferme_fenetre
from src.timer import get_timer
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
	gs.keys, gs.players_count = handle_players_selection_menu_interaction(zones_coords)

	if save_loading:
		restore_save()
	else:
		# all other default values are already stored in the game state module
		gs.start_time = time()

	# main loop
	while True:
		key = attente_touche_jusqua(50)

		if key is not None or gs.debug_mode:
			key = apply_debug_mode(key)
			gs.current_color = gs.selected_colors[get_playing_player(gs.players_count, key) - 1]
			key_triggered(key)

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
