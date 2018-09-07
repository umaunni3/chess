from Piece import *
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
                    self.board[-1].append(Pawn(rank, file, clr))
                elif rank in [0, 7]:
                    if file == 0 or file == 7:
                        self.board[-1].append(Rook(rank, file, clr))
                    elif file == 1 or file == 6:
                        self.board[-1].append(Knight(rank, file, clr))
                    elif file == 2 or file == 5:
                        self.board[-1].append(Bishop(rank, file, clr))
                    elif file == 3:
                        self.board[-1].append(Queen(rank, file, clr))
                    elif file == 4:
                        self.board[-1].append(King(rank, file, clr))
                else:
                    self.board[-1].append('XX') 
    
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


