"""
This module handles all the keys related things.
"""
from random import shuffle
from time import time
from src.timer import adjust_time
from src.display import display_pause
from src.menu import handle_pause_menu_interaction
from src.logic import move, next_color, use_escalator, use_vortex, explore, use_telekinesis

def get_keys(players_count):
	"""
	Return the right keys according to the players count.
	"""
	if players_count == 1:
		return {
			"up": {"up", "z"},
			"left": {"left", "q"},
			"down": {"down", "s"},
			"right": {"right", "d"},
			"switch": {"n"},
			"debug": "b",
			"escalator": "e",
			"explore": "x",
			"vortex": "v",
			"exit": "escape",
			"telekinesis": "g"
		}

	elif players_count == 2:
		keys = {
			"switch": {"q", "m"},
			"debug": "b",
			"exit": "escape"
		}
	
		directions = ["up", "down", "left", "right"]
		shuffle(directions)
		for key, direction in zip({"a", "z", "o", "p"}, directions):
			keys[direction] = key
		remaining_keys = ["e", "i", "l"]
		shuffle(remaining_keys)
		keys["escalator"], keys["vortex"], keys["explore"] = remaining_keys[0], remaining_keys[1], remaining_keys[2]

		return keys
	else:
		keys = {
			"switch": {"q", "m", "v"},
			"debug": "b",
			"exit": "escape"
		}
		directions = ["up", "down", "left", "right"]
		shuffle(directions)
		for key, direction in zip({"a", "c", "p"}, directions):
			keys[direction] = key

		remaining_keys = ["z", "x", "o", "l"]
		shuffle(remaining_keys)
		keys["escalator"], keys["vortex"], keys[directions[3]], keys["explore"] = remaining_keys[0], remaining_keys[1], remaining_keys[2], remaining_keys[3]
			
		return keys

def key_triggered(key, keys, current_color, pawns, pawns_on_objects, pawns_outside, exit_available, start_time, timeout, debug_mode, walls, escalators, stock, on_board_cards, board, game_width, game_height, window_width, window_height):
	"""
	Execute the appropriate action in the game according to the triggered key.
	"""
	current_time = None
	paused = False
	hourglass_returned = False

	for direction in {"up", "down", "left", "right"}:
		if key in keys[direction]:
			hourglass_returned = move(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, walls, on_board_cards, board, direction)
			break

	if key in keys["switch"]:
		current_color = next_color(current_color, pawns)

	if key == keys["explore"]:
		explore(stock, pawns, on_board_cards, current_color, board, walls, escalators)

	elif key == keys["vortex"]:
		use_vortex(keys, current_color, pawns, exit_available, walls, escalators, start_time, timeout, debug_mode, game_width, game_height, window_width, window_height, board)

	elif key == keys["escalator"]:
		use_escalator(current_color, pawns, escalators)

	elif key == keys["telekinesis"]:
		escalators, walls = use_telekinesis(current_color, pawns, board, on_board_cards, escalators, walls, 0)

	elif key == keys["debug"]:
		debug_mode = not debug_mode
	
	elif key == keys["exit"]:
		paused = True
		current_time = time()

		pause_rectangle_coords, pause_rectangle_width, pause_rectangle_height, zones_coords = display_pause(game_width, game_height)
		handle_pause_menu_interaction(pause_rectangle_coords, pause_rectangle_width, pause_rectangle_height, zones_coords, keys["exit"], pawns, pawns_on_objects, pawns_outside, current_color, debug_mode, exit_available, start_time, board, walls, escalators, stock, on_board_cards)

		current_time = adjust_time(start_time, current_time)
	return escalators, walls, current_color, hourglass_returned, debug_mode, (paused, current_time)