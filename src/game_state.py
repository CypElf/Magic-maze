from copy import deepcopy

from src.cards import start_card, cards

# Default values

# DO NOT CHANGE THE WIDTH AND HEIGHT, as the entire game is made to render the items to the screen using these values, especially the images	
window_width = 1500
window_height = 800

game_width = 1200
game_height = 800

cell_width = 40
cell_height = 40

board = [["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30] + list(map(lambda row: ["*"] * 13 + row + ["*"] * 13, start_card["board"])) + [["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30, ["*"] * 30] # game start board, only the start card (ID 1) is present at the center

stock = deepcopy(cards) # remaining cards that can be picked to be displayed at the screen
on_board_cards = [{"id": 1, "top_left": (8, 13), "rotations": 0}] # define which cards have been extracted from the stock and added to the game, and their top left cell coordinates

escalators = start_card["escalators"] # present escalators in the game coordinates
walls = start_card["walls"] # present walls in the game coordinates

pawns = { "purple": [9, 14], "orange": [10, 14], "yellow": [9, 15], "green": [10, 15] } # pawns start coordinates
pawns_on_objects = {"purple": False, "orange": False, "yellow": False, "green": False} # define which pawn is on its object or not
pawns_outside = pawns_on_objects.copy() # define which pawn has successfully escaped from the game or not

current_color = "purple"
selected_colors = ["purple", "purple", "purple"]
debug_mode = False
exit_available = False
telekinesis_times_used = 0

timeout = 3 # timeout is in minutes

lost = False
won = False