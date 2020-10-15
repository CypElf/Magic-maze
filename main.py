from upemtk import *
from random import choice
from move import *
from display import display_game

window_width = 800
window_height = 800

class pawn:
	"""
	The class pawn represents a pawn with its coordinates.
	WARNING ! BE CAREFUL as the x coordinate represents the position on the vertical axis and the y on the horizontal axis, as the rows of the board represents the x and the columns the y. 
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def coord(self):
		"""
		Returns the coordinates of the pawn as a tuple (x,y)

		Example :

		>>> p = pawn(5,4)
		>>> p.coord()
		(5, 4)
		"""
		return (self.x, self.y)

def main():
	cree_fenetre(window_width, window_height)

	board = [
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
			[".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
		]

	pawns = { "red": pawn(7, 4), "orange": pawn(7, 5), "yellow": pawn(8, 4), "green": pawn(8, 5) }

	up_keys = ["Up", "z"]
	left_keys = ["Left", "q"]
	down_keys = ["Down", "s"]
	right_keys = ["Right", "d"]
	debug_key = "b"

	current_color = "red"
	debug_mode = False

	display_game(pawns["red"], pawns["orange"], pawns["yellow"], pawns["green"], board, window_width, window_height)
	mise_a_jour()

	while True:
		event = donne_evenement()
		event_type = type_evenement(event)
		mise_a_jour()

		if event_type == "Touche" or debug_mode:
			if event_type == "Touche":
				key = touche(event)
			else:
				key = choice([up_keys[0], left_keys[0], down_keys[0], right_keys[0]])

			if key == "Escape":
				break

			if key == debug_key:
				debug_mode = not debug_mode

			elif key in up_keys:
				move_up(current_color, pawns, board)

			elif key in down_keys:
				move_down(current_color, pawns, board)
			
			elif key in left_keys:
				move_left(current_color, pawns, board)
			
			elif key in right_keys:
				move_right(current_color, pawns, board)

		display_game(pawns["red"], pawns["orange"], pawns["yellow"], pawns["green"], board, window_width, window_height)
		mise_a_jour()

	ferme_fenetre()


if __name__ == "__main__":
	main()