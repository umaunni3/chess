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

    def __init__(self, srcFile=None):
        """Initializes the game board according to standard chess rules"""
        if srcFile:
            Board.readFile(srcFile)
            return
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

    def save(self, fileDest):
        """ Takes in a filename and writes the current board state to a csv with 
        that name. """

        with open(fileDest, 'w+') as f:
            # we will write to this file!
            for row in Board.board[::-1]: # look erik i can use ur fancy syntax too
                print(",".join(list(map(str, row))))
                f.write(",".join(list(map(str, row))))
                f.write("\n")


        print("done writing!")





    def readFile(srcFile):
        """ Read in a board state from a csv file and store it in a Board. """
        board = [[] for _ in range(8)]
        with open(srcFile) as f:
            rank = 7
            for line in f:
                print(line)
                # starts with black, which is 7th rank
                if rank < 0:
                    raise ValueError
                    return
                chars = line.split(",")
                this_line = []
                file = 0
                for val in chars:
                    print("   " + str(val))
                    if file > 7:
                        raise ValueError
                        return
                    if val == "XX":
                        this_line.append(val)
                    elif len(val.strip()) == 2: # name in format bP, wQ, etc
                        pieceType = val[1]
                        clr = val[0]
                        if pieceType == "Q":
                            print("adding" + pieceType + " " + clr)
                            piece = Piece.Queen(rank, file, clr)
                        elif pieceType == "K":
                            piece = Piece.King(rank, file, clr)
                            print("adding" + pieceType + " " + clr)
                        elif pieceType == "R":
                            print("adding" + pieceType + " " + clr)
                            piece = Piece.Rook(rank, file, clr)
                        elif pieceType == "N":
                            print("adding" + pieceType + " " + clr)
                            piece = Piece.Knight(rank, file, clr)
                        elif pieceType == "B":
                            print("adding" + pieceType + " " + clr)
                            piece = Piece.Bishop(rank, file, clr)
                        elif pieceType == "p":
                            print("adding" + pieceType + " " + clr)
                            piece = Piece.Pawn(rank, file, clr)
                    else:
                        raise ValueError("unexpected input format! >:( " + str(val))
                    this_line.append(piece)
                    file += 1

                board[rank] = this_line
                rank -= 1

        Board.board = board

    
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

    def validSpot(self, rank, file):
        return int(rank) < Board.width and int(rank) >= 0 and int(file) < Board.width and int(file) >= 0

    def isOpen(self, rank, file):
        """ Return True if the position specified by rank, file is open (not
        occupied by a piece); else, return False. """
        rank, file = int(rank), int(file)
        if not self.validSpot(rank, file): # move is outside of the board rip
            return False
        if self.board[rank][file] == "XX": # no pieces currently in the spot
            return True
        return False

    def putPiece(self, piece, rank, file):
        """ Put the specified piece in the specified position. If this move would
        overwrite an existing piece with a new piece (not an empty space), then
        perhaps do something to indicate that a piece has been captured? """
        rank, file = int(rank), int(file)
        print("PUTPIECE: putting {} on rank {}, file{}".format(piece, rank, file))
        if self.board[rank][file] == "XX" or piece == "XX":
            # moving piece to empty spot, or setting spot to empty
            # after moving the piece that previously occupied it
            self.board[rank][file] = piece
        else:
            if not self.isOpen(rank, file):
                capturedPiece = self.board[rank][file] # piece being captured
                self.captured[capturedPiece.clr].append(self.board[rank][file])
                self.activePieces[capturedPiece.clr].remove(self.board[rank][file])
                capturedPiece.deactivate()

    def setOpen(self, rank, file):
        """ Reset the specified position to open (eg. not containing a piece) """
        self.putPiece("XX", rank, file) # i love being able to pass any datatype into functions
        

    def contents(self, rank, file, rankConverted=False):
        """ Return whatever piece is in the spot specified, or "XX" if there is no piece. """ 
        # switch i, j coords in this code because input pos has format (x,y) with horiz. coord first
        # OH ALSO APPARENTLY SWITCH THE Y COORDINATE BECAUSE NOW THE BOARD PRINTOUT IS A LIE AND WHITE IS AT 0
        # print("CONTENTS!!! rank={}, file={}".format(rank,file))
        
        rank, file = int(rank), int(file)
        if not rankConverted:
            print("CONTENTS!!! rank={}, file={}".format(rank,file))
            file = 7 - file

        print("UPDATED CONTENTS!!! rank={}, file={}".format(rank,file))
        if file > 7 or file < 0 or rank > 7 or rank < 0:
            print("can't move to rank {}, file {}".format(rank, file))
            return
        return self.board[rank][file]