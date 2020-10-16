from upemtk import rectangle

def display_game(red, orange, yellow, green, board, width, height):
	"""
	Display the board and the pawns on their positions.
	
	board is supposed to be a valid two dimensional list, with at least 2 rows and 2 columns.
	red, orange, yellow, green are all supposed to be a list of two elements that describe their position inside the board.

	Exemples :

	>>> display_game([0,0], [0,0], [0,0], [0,0], [], 800, 800)
	Traceback (most recent call last):
		...
	AssertionError: the specified board does not have enough rows

	>>> display_game([0,0], [0,0], [0,0], [0,0], [[],[]], 800, 800)
	Traceback (most recent call last):
		...
	AssertionError: the specified board does not have enough columns

	>>> display_game([0,1], [1,0], [2,0], [1,1], [[".","."],[".","."]], 800, 800)
	Traceback (most recent call last):
		...
	AssertionError: yellow position is out of range
	"""

	rows_count = len(board)
	assert rows_count >= 2, "the specified board does not have enough rows"

	columns_count = len(board[0])
	assert columns_count >= 2, "the specified board does not have enough columns"

	assert red != orange and red != yellow and red != green and orange != yellow and orange != green and yellow != green, "pawns can not be at the same position at the same time"

	assert red[0] < rows_count and red[0] >= 0 and red[1] < columns_count and red[1] >= 0, "red position is out of range"
	assert orange[0] < rows_count and orange[0] >= 0 and orange[1] < columns_count and orange[1] >= 0, "orange position is out of range"
	assert yellow[0] < rows_count and yellow[0] >= 0 and yellow[1] < columns_count and yellow[1] >= 0, "yellow position is out of range"
	assert green[0] < rows_count and green[0] >= 0 and green[1] < columns_count and green[1] >= 0, "green position is out of range"

	case_width = width / columns_count
	case_height = height / rows_count

	for i in range(rows_count):
		for j in range(columns_count):
			x = j * case_width
			y = i * case_height

			color = "white"

			if [i, j] == red:
				color = "red"
			elif [i, j] == orange:
				color = "orange"
			elif [i, j] == yellow:
				color = "yellow"
			elif [i, j] == green:
				color = "green"

			rectangle(x, y, x + case_width, y + case_height, remplissage = color)