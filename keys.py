from move import move

def key_triggered(key, keys, current_color, pawns, pawns_on_objects, pawns_outside, exit_available, debug_mode, board):
	for direction in {"up", "down", "left", "right"}:
		if key in keys[direction]:
			move(current_color, pawns, pawns_on_objects, pawns_outside, exit_available, board, direction)
			break
	
	for color in {"purple", "orange", "yellow", "green"}:
		if key in keys[color]:
			current_color = color
			break

	if key == keys["switch"]:
		current_color = next_color(current_color)

	elif key == keys["debug"]:
		debug_mode = not debug_mode
	
	elif key == keys["exit"]:
		return current_color, True, debug_mode

	return current_color, False, debug_mode

def get_keys():
	return {
		"up": {"up", "z"},
		"left": {"left", "q"},
		"down": {"down", "s"},
		"right": {"right", "d"},
		"switch": "n",
		"debug": "b",
		"exit": "escape",
		"purple": {"ampersand","1", "p"},
		"orange":  {"eacute", "2", "o"},
		"yellow": {"quotedbl", "3", "y"},
		"green": {"quoteright", "4", "g"}
	}

def next_color(current_color):
	return {"purple": "orange", "orange": "yellow", "yellow": "green", "green": "purple"}[current_color]