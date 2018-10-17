from Piece import *
import Piece
# from piece import Piece, Queen, King, Rook, Knight, Pawn, Bishop

# print(Piece)

filemap = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
class Board:
    """
    This is the class for the board. Refer to image for standard chessboard notation/initial config.
    File: a-h, columns of board (Contains both white and black pieces at startup)
    Rank: 1-8, rows of board (First two ranks at start are white)
    Currently, "na" means empty square (just to make the printout nice and square)
    """
    width = 8
    board = []
    finished = False
    turn = 0 #0 will be white, 1 black
    activePieces = {"w":[], "b":[]} # map between color and all active pieces of that color on board
    captured = {"w":[], "b":[]} # map between color and pieces of that color that were captured
    kings = {} # {clr : King of that color} (should only have two elements)

    def __init__(self):
        """Initializes the game board according to standard chess rules"""
        for rank in range(Board.width): #populate board
            self.board.append([])
            if rank < 4: 
                clr = "w"
            else:
                clr = "b"
            for file in range(Board.width): 
                if rank in [1, 6]: #pawns
                    piece = Piece.Pawn(rank, file, clr)
                elif rank in [0, 7]:
                    if file == 0 or file == 7:
                        piece = Piece.Rook(rank, file, clr)
                    elif file == 1 or file == 6:
                        piece = Piece.Knight(rank, file, clr)
                    elif file == 2 or file == 5:
                        piece = Piece.Bishop(rank, file, clr)
                    elif file == 3:
                        piece = Piece.Queen(rank, file, clr)
                    elif file == 4:
                        piece = Piece.King(rank, file, clr)
                        Board.kings[clr] = piece
                else:
                    piece = 'XX'
                self.board[-1].append(piece)
                Board.activePieces[clr].append(piece)
    
    def update(self):
        if self.finished == True:
            return "Time to go to bed"
        else:
            move = input("Your move: ")
            tokens = [i for i in move]
            if len(tokens) == 2: #pawn movement
                file, rank = tokens
                file = filemap[file]
                rank = int(rank)
                if self.turn == 0:
                    sgn = -1
                elif self.turn == 1:
                    sgn = 1
                if isinstance(self.board[rank + sgn*1][file], Pawn):
                    self.board[rank][file], self.board[rank + sgn*1][file] = self.board[rank + sgn*1][file], self.board[rank][file] 
                elif isinstance(self.board[rank + sgn*2][file], Pawn):
                    self.board[rank][file], self.board[rank + sgn*2][file] = self.board[rank + sgn*2][file], self.board[rank][file] 
                else:
                    print("invalid move")
                    return
                
                self.turn = 1 - self.turn
                print("Pawn to " + move)
            else:
                print("DONTDOTHATASDG;LKAHSDG;LASKHDFLKASJL;FDJ/M/ZXCVLKASLDGH \n")

    def __str__(self):
        for rank in self.board[::-1]:
            print([str(piece) for piece in rank])
        return ""

    def validSpot(rank, file):
        return rank < Board.width and file < Board.width

    def isOpen(rank, file):
        """ Return True if the position specified by rank, file is open (not
        occupied by a piece); else, return False. """
        if not validSpot(rank, file): # move is outside of the board rip
            return False
        if board[rank][file] == "XX": # no pieces currently in the spot
            return True
        return False

    def putPiece(piece, rank, file):
        """ Put the specified piece in the specified position. If this move would
        overwrite an existing piece with a new piece (not an empty space), then
        perhaps do something to indicate that a piece has been captured? """
        if board[rank][file] == "XX":
            board[rank][file] = piece
        else:
            if not isOpen(rank, file):
                capturedPiece = board[rank][file] # piece being captured
                captured[capturedPiece.clr].append(board[rank][file])
                activePieces[color].remove(board[rank][file])


    def setOpen(rank, file):
        """ Reset the specified position to open (eg. not containing a piece) """
        putPiece("XX", rank, file) # i love being able to pass any datatype into functions
        
