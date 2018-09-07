class Piece:
    """
    This is the class for a chesspiece.
    File: a-h, columns of board (Contains both white and black pieces at startup)
    Rank: 1-8, rows of board (First two ranks at start are white)
    """
    def __init__(self, rank, file, clr, canJump):
        """Initializes a piece."""
        self.rank = rank
        self.file = file
        self.clr = clr
        self.canJump = canJump

class Knight(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = True)
    def __str__(self):
        return self.clr + "N"

class Bishop(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
    def __str__(self):
        return self.clr + "B"

class Rook(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
    def __str__(self):
        return self.clr + "R"

class Queen(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
    def __str__(self):
        return self.clr + "Q"

class King(Piece):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
    def __str__(self):
        return self.clr + "K"

class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
    def __str__(self):
        return self.clr + "p"