import * from Exception.py
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
    def move(self, board, rank, file):
        """ Move this piece to the specified rank and file
        on the provided board if it is a legal move; else,
        raise an error. """


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
    def move(self, board, rank, file):
        """ Move this piece to the specified rank and file
        on the provided board if it is a legal move; else,
        raise an error. """
        # TODO: remember to add en passant rules lol but i'm tired now it's 3 AM
        if !board.valid_spot(rank, file):
            # u can't do that!!
            raise InvalidMoveException
            return
        if board.is_open(rank, file):
            # cool! now lets check if pawns can do this move lol
            if (file == self.file && rank == self.rank + 1 
                        && !reveals_check(this, rank, file)): # moving one place forward
                board.set_open(self.rank, self.file)
                self.rank = rank
                # TODO: confirm that moving forward will not put this pawn's king in check!!
            else:
                # y u do dis
                raise InvalidMoveException
        else:
            if (abs(file - self.file) == 1 && rank == self.rank + 1 
                        && !reveals_check(this, rank, file)) # capturing a piece
                board.set_open(self.rank, self.file)
                self.rank = rank
                self.file = file
                # TODO: confirm that moving forward will not put this pawn's king in check!!
            else:
                # stahp
                raise InvalidMoveException

    
            

def reveals_check():
    """ Determine whether moving the specified piece to the specified location will reveal
    an attack on the king (basically, is the piece pinned and can it legally move) """
    
    # TODO: This whole function!!
    pass