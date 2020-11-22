from random import shuffle
from upemtk import ferme_fenetre
from move import move

def key_triggered(key, keys, current_color, pawns, pawns_on_objects, pawns_outside, exit_available, debug_mode, board):
	hourglass_returned = False
	for direction in {"up", "down", "left", "right"}:
		if key in keys[direction]:
			hourglass_returned = move(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board, direction)
			break

	if key == keys["switch"]:
		current_color = next_color(current_color)

	elif key == keys["debug"]:
		debug_mode = not debug_mode
	
	elif key == keys["exit"]:
		ferme_fenetre()
		exit(0)

	return current_color, hourglass_returned, debug_mode

def get_keys(players_count):
	if players_count == 1:
		return {
			"up": {"up", "z"},
			"left": {"left", "q"},
			"down": {"down", "s"},
			"right": {"right", "d"},
			"switch": "v",
			"debug": "b",
			"exit": "escape"
		}

	elif players_count == 2:
		keys = {
			"switch": "v",
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
			"switch": "v",
			"debug": "b",
			"exit": "escape"
		}
		directions = ["up", "down", "left", "right"]
		shuffle(directions)
		for key, direction in zip({"a", "c", "o", "p"}, directions):
			keys[direction] = key
			
		return keys

def next_color(current_color):
	return {"purple": "orange", "orange": "yellow", "yellow": "green", "green": "purple"}[current_color]