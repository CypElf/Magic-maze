"""
This module handles all the keys related things.
"""
from random import shuffle

import src.game_state as gs
from src.menu import pause_game
from src.logic import move, next_color, use_escalator, use_vortex, explore, use_telekinesis, get_playing_player

def get_keys():
	"""
	Return the right keys according to the players count.
	"""
	if gs.players_count == 1:
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

	elif gs.players_count == 2:
		keys = {
			"switch": {"q", "m"},
			"debug": "b",
			"exit": "escape",
			"telekinesis": "g"
		}
	
		directions = ["up", "down", "left", "right"]
		shuffle(directions)
		for key, direction in zip({"a", "z", "o", "p"}, directions): # these 4 keys are always associated with directions
			keys[direction] = key
		remaining_keys = ["e", "i", "l"]
		shuffle(remaining_keys)
		keys["escalator"], keys["vortex"], keys["explore"] = remaining_keys[0], remaining_keys[1], remaining_keys[2]

		return keys
	else:
		keys = {
			"switch": {"q", "m", "v"},
			"debug": "b",
			"exit": "escape",
			"telekinesis": "g"
		}
		directions = ["up", "down", "left", "right"]
		shuffle(directions)
		for key, direction in zip({"a", "c", "p"}, directions): # these 4 keys are always associated with directions
			keys[direction] = key

		remaining_keys = ["z", "x", "o", "l"]
		shuffle(remaining_keys)
		keys["escalator"], keys["vortex"], keys[directions[3]], keys["explore"] = remaining_keys[0], remaining_keys[1], remaining_keys[2], remaining_keys[3]
			
		return keys

def key_triggered(key):
	"""
	Execute the appropriate action in the game according to the triggered key.
	"""
	keys = gs.keys
	for direction in {"up", "down", "left", "right"}:
		if key in keys[direction]:
			move(direction)
			break

	if key in keys["switch"]:
		next_color(get_playing_player(gs.players_count, key))

	if key == keys["explore"]:
		explore()

	elif key == keys["vortex"]:
		use_vortex(keys)

	elif key == keys["escalator"]:
		use_escalator()

	elif key == keys["telekinesis"]:
		use_telekinesis(keys)

	elif key == keys["debug"]:
		gs.debug_mode = not gs.debug_mode
	
	elif key == keys["exit"]:
		pause_game(keys["exit"])