from upemtk import rectangle

def display_game(red, orange, yellow, green, board, width, height):
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

	case_width = width / columns_count
	case_height = height / rows_count

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