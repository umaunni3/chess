# from Exception.py import * 
import pygame
# import GUI
# import GUI.PieceSprite

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
        self.active = True # set to inactive if captured, or for checking possible moves

    def underAttack(self, board):
        """ Return True if this piece is under attack, else False. """
        if self.clr == "w":
            enemyClr = "b"
        else:
            enemyClr = "w"
        enemyPieces = board.activePieces[enemyClr] # list of all enemy pieces
        for piece in enemyPieces: # check each enemy piece to see if it's attacking this piece
            if piece.active and piece is not self and piece.isAttacking(self):
                return True
        return False
    def move(self, board, rank, file, debug=True):
        if debug:
            # self.rank += 1 # just move one forward for now lol
            self.rank = rank
            self.file = file
            return

    

class Knight(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = True)
        if self.clr == "w":
            self.imageFile = "assets/w_knight.png"
        elif self.clr == "b":
            self.imageFile = "assets/b_knight.png"

    def __str__(self):
        return self.clr + "N"

    def canMove(self, board, rank, file):
        """ Return True if this piece can theoretically move
        to the specified location (ignore whether or not there is
        a piece occupying that position). Else return False"""

        if not board.validSpot(rank, file):
            return False
        king = board.kings[self.clr] # get king of this piece's team
        self.active = False
        if king.underAttack(board): # king under attack if this piece is not where it is now
            self.active = True
            return False 
        self.active = True
        # not sure if the logic below works; if not, i'll just hard code the checks lol
        if abs(self.rank - rank) + abs(self.file - file) == 3: # some permuation of L shape
            return True
        return False

    def move(self, board, rank, file, debug=False):
        """ Move this piece to the specified rank and file
        on the provided board if it is a legal move; else,
        raise an error. """
        if debug:
            Piece.move(self, board, rank, file, debug)

            return
        if canMove(board, rank, file):
            board.setOpen(self, self.rank, self.file)
            if not board.isOpen(rank, file): # there's a piece there!
                if isinstance(board.board[rank][file], King):
                    # we're capturing the king! hmmmm should that happen? probably not
                    board.finished = True
                else:
                    board.board[rank][file].active = False # capture it
                    board.captured[self.clr].append(board.board[rank][file]) # add it to captured list
                    if self.clr == "w":
                        enemy = "b"
                    else:
                        enemy = "w"
                    board.activePieces[enemy].remove(board.board[rank][file]) # remove from active list

            board.putPiece(self, rank, file)
            self.rank = rank
            self.file = file
        else:
            # raise InvalidMoveException
            return
        

    def isAttacking(self, board, other_piece):
        """ Return True if this piece can legally capture other_piece """
        # check if after moving this piece the king would be under attack
        return canMove(board, other_piece.rank, other_piece.file)




class Bishop(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
        if self.clr == "w":
            self.imageFile = "assets/w_bishop.png"
        elif self.clr == "b":
            self.imageFile = "assets/b_bishop.png"

    def __str__(self):
        return self.clr + "B"

class Rook(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
        if self.clr == "w":
            self.imageFile = "assets/w_rook.png"
        elif self.clr == "b":
            self.imageFile = "assets/b_rook.png"

    def __str__(self):
        return self.clr + "R"

    def canMove(self, board, rank, file):
        return True
        

class Queen(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
        if self.clr == "w":
            self.imageFile = "assets/w_queen.png"
        elif self.clr == "b":
            self.imageFile = "assets/b_queen.png"

    def __str__(self):
        return self.clr + "Q"

class King(Piece):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
        if self.clr == "w":
            self.imageFile = "assets/w_king.png"
        elif self.clr == "b":
            self.imageFile = "assets/b_king.png"

    def __str__(self):
        return self.clr + "K"
    


class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
        if self.clr == "w":
            self.imageFile = "assets/w_pawn.png"
        elif self.clr == "b":
            self.imageFile = "assets/b_pawn.png"

    def __str__(self):
        return self.clr + "p"

    def move(self, board, rank, file, debug=True):
        """ Move this piece to the specified rank and file
        on the provided board if it is a legal move; else,
        raise an error. """
        # TODO: remember to add en passant rules lol but i'm tired now it's 3 AM
        if debug:
            # self.rank += 1 # just move one forward for now lol
            Piece.move(self, board, rank, file, debug)
            return
        if not board.validSpot(rank, file):
            # u can't do that!!
            # raise InvalidMoveException
            return
        if board.isOpen(rank, file):
            # cool! now lets check if pawns can do this move lol
            if (file == self.file and rank == self.rank + 1 
                        and not revealsCheck(self, rank, file)): # moving one place forward
                board.setOpen(self.rank, self.file)
                self.rank = rank
                # TODO: confirm that moving forward will not put this pawn's king in check!!
            else:
                # y u do dis
                # raise InvalidMoveException
                return
        else:
            if (abs(file - self.file) == 1 and rank == self.rank + 1 
                        and not revealsCheck(self, rank, file)): # capturing a piece
                board.setOpen(self.rank, self.file)
                self.rank = rank
                self.file = file
                # TODO: confirm that moving forward will not put this pawn's king in check!!
            else:
                # stahp
                # raise InvalidMoveException
                return
    
            


# class PieceSprite(pygame.sprite.Sprite):
#     def __init__(self, fileName, pos):
#         pygame.sprite.Sprite.__init__(self)
#         # self.image = pygame.Surface((50,50))
#         self.image = pygame.image.load(fileName)
#         self.image = pygame.transform.scale(self.image, (int(squareWidth*0.7), int(squareWidth*0.7)))
#         # self.image.fill(BLACK)
#         self.rect = self.image.get_rect()
#         self.rect.center = pos #(displayWidth/2, displayHeight/2)
#         self.dir = 1

