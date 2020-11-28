"""
This module handles all the keys related things.
"""

from random import shuffle
from upemtk import ferme_fenetre
from move import move

def key_triggered(key, keys, current_color, pawns, pawns_on_objects, pawns_outside, exit_available, debug_mode, walls, board):
	"""
	Execute the appropriate action in the game according to the triggered key.
	"""
	hourglass_returned = False
	for direction in {"up", "down", "left", "right"}:
		if key in keys[direction]:
			hourglass_returned = move(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, walls, board, direction)
			break

	if key in keys["switch"]:
		current_color = next_color(current_color)

	elif key == keys["debug"]:
		debug_mode = not debug_mode
	
	elif key == keys["exit"]:
		ferme_fenetre()
		exit(0)

	return current_color, hourglass_returned, debug_mode

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
	
		directions = {"up", "down", "left", "right"}
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

def next_color(current_color):
	"""
	Return the next color from the given one, in the order "purple", "orange", "yellow", "green".
	"""
	return {"purple": "orange", "orange": "yellow", "yellow": "green", "green": "purple"}[current_color]