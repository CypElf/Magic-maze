from upemtk import *

largeurFenetre = 800
hauteurFenetre = 800

def display_game(board, red, orange, yellow, green):
	"""
	Display the board and the pawns on their positions.
	
	board is supposed to be a valid two dimensional list, with at least 2 rows and 2 columns.
	red, orange, yellow, green are all supposed to be a pawn object that describe their position inside the board.

	Exemples :

	>>> display_game([], pawn(0,0), pawn(0,0), pawn(0,0), pawn(0,0))
	Traceback (most recent call last):
		...
	AssertionError: the specified board does not have enough rows

	>>> display_game([[],[]], pawn(0,0), pawn(0,0), pawn(0,0), pawn(0,0))
	Traceback (most recent call last):
		...
	AssertionError: the specified board does not have enough columns

	>>> display_game([[".","."],[".","."]], pawn(0,1), pawn(1,0), pawn(0,2), pawn(1,1))
	Traceback (most recent call last):
		...
	AssertionError: yellow position is out of range
	"""

	rows_count = len(board)
	assert rows_count >= 2, "the specified board does not have enough rows"

	columns_count = len(board[0])
	assert columns_count >= 2, "the specified board does not have enough columns"

	assert red.coord() != orange.coord() and red.coord() != yellow.coord() and red.coord() != green.coord() and orange.coord() != yellow.coord() and orange.coord() != green.coord() and yellow.coord() != green.coord(), "pawns can not be at the same position at the same time"

	assert red.x < rows_count and red.x >= 0 and red.y < columns_count and red.y >= 0, "red position is out of range"
	assert orange.x < rows_count and orange.x >= 0 and orange.y < columns_count and orange.y >= 0, "orange position is out of range"
	assert yellow.x < rows_count and yellow.x >= 0 and yellow.y < columns_count and yellow.y >= 0, "yellow position is out of range"
	assert green.x < rows_count and green.x >= 0 and green.y < columns_count and green.y >= 0, "green position is out of range"

	case_width = largeurFenetre / columns_count
	case_height = hauteurFenetre / rows_count

	for i in range(rows_count):
		for j in range(columns_count):
			x = j * case_width
			y = i * case_height

			color = "white"

			if (i, j) == red.coord():
				color = "red"
			elif (i, j) == orange.coord():
				color = "orange"
			elif (i, j) == yellow.coord():
				color = "yellow"
			elif (i, j) == green.coord():
				color = "green"

			rectangle(x, y, x + case_width, y + case_height, remplissage = color)

class pawn:
	"""
	The class pawn represents a pawn with its coordinates.
	BE CAREFUL as the x coordinate represents the position on the vertical axis and the y on the horizontal axis, as the rows of the board represents the x and the columns the y. 
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
	cree_fenetre(largeurFenetre, hauteurFenetre)

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

	pawns = {"red": pawn(7, 4), "orange": pawn(7, 5), "yellow": pawn(8, 4), "green": pawn(8, 5)}

	up_keys = ["Up", "z"]
	left_keys = ["Left", "q"]
	down_keys = ["Down", "s"]
	right_keys = ["Right", "d"]

	current_color = "red"

	display_game(board, pawns["red"], pawns["orange"], pawns["yellow"], pawns["green"])
	mise_a_jour()

	while True:
		event = donne_evenement()
		event_type = type_evenement(event)
		mise_a_jour()

		if event_type == "Touche":
			key = touche(event)

			if key == "Escape":
				break

			elif key in up_keys:
				current_pawn = pawns[current_color]
				collision = False

				others = pawns.copy()
				others.pop(current_color)
				for _, p in others.items():
					if p.coord() == (current_pawn.x - 1, current_pawn.y):
						collision = True

				if current_pawn.x > 0 and not collision:
					pawns[current_color].x -= 1

			elif key in down_keys:
				current_pawn = pawns[current_color]
				collision = False

				others = pawns.copy()
				others.pop(current_color)
				for _, p in others.items():
					if p.coord() == (current_pawn.x + 1, current_pawn.y):
						collision = True

				if current_pawn.x < len(board) - 1 and not collision:
					pawns[current_color].x += 1
			
			elif key in left_keys:
				current_pawn = pawns[current_color]
				collision = False

				others = pawns.copy()
				others.pop(current_color)
				for _, p in others.items():
					if p.coord() == (current_pawn.x, current_pawn.y - 1):
						collision = True

				if current_pawn.y > 0 and not collision:
					pawns[current_color].y -= 1
			
			elif key in right_keys:
				current_pawn = pawns[current_color]
				collision = False

				others = pawns.copy()
				others.pop(current_color)
				for _, p in others.items():
					if p.coord() == (current_pawn.x, current_pawn.y + 1):
						collision = True

				if current_pawn.y < len(board[0]) - 1 and not collision:
					pawns[current_color].y += 1

			display_game(board, pawns["red"], pawns["orange"], pawns["yellow"], pawns["green"])
		mise_a_jour()

	ferme_fenetre()


if __name__ == "__main__":
	main()