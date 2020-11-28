"""
This module handles all the keys related things.
"""
from random import shuffle
from time import time
from display import display_pause
import logic

def key_triggered(key, keys, current_color, pawns, pawns_on_objects, pawns_outside, exit_available, start_time, debug_mode, walls, board, game_width, game_height):
	"""
	Execute the appropriate action in the game according to the triggered key.
	"""
	current_time = None
	paused = False
	hourglass_returned = False

	for direction in {"up", "down", "left", "right"}:
		if key in keys[direction]:
			hourglass_returned = logic.move(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, walls, board, direction)
			break

	if key in keys["switch"]:
		current_color = logic.next_color(current_color)

	elif key == keys["debug"]:
		debug_mode = not debug_mode
	
	elif key == keys["exit"]:
		paused = True
		current_time = time()

		pause_rectangle_coords, zones_coords = display_pause(game_width, game_height)
		logic.handle_pause_menu_interaction(pause_rectangle_coords, zones_coords, keys["exit"])

		current_time = start_time + (time() - current_time)
	return current_color, hourglass_returned, debug_mode, (paused, current_time)

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
			"exit": "escape"
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

		return keys
	else:
		keys = {
			"switch": {"z", "m", "v"},
			"debug": "b",
			"exit": "escape"
		}
		directions = ["up", "down", "left", "right"]
		shuffle(directions)
		for key, direction in zip({"a", "c", "o", "p"}, directions):
			keys[direction] = key
			
		return keys