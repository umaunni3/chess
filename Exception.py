class InvalidMoveException(Exception):
	""" Custom exception to be raised when there is a
	request to make an invalid move. """
	print("Not a valid move!")
	pass