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