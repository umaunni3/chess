# from Exception.py import * 
import pygame
# from main import * #displayHeight, displayWidth, edgeBuffer, squareWidth
import main
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
        # self.imageFile = ""
        self.sprite = PieceSprite(self)


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
    def move(self, board, rank, file, debug=False, rankConverted=False):
        # self.rank += 1 # just move one forward for now lol
        if 0 <= rank < 8 and 0 <= file < 8:
            # convert input rank, file (with top left (0,0)) to board rank, file (with bottom left (0,0))
            if not rankConverted:
                rank = 7 - rank # only do this if hasn't already been done before being passed in
            prevRank, prevFile = self.rank, self.file
            self.rank, self.file = int(rank), int(file)
            self.sprite.updatePosition(rank, file)
            print("move pos is ", rank, file)
            Piece.updateBoard(self, board, prevRank, prevFile)
            if isinstance(self, Pawn):
                # set hasMoved attribute to true
                self.hasMoved = True
            return
        else:
            print("you can't move here!")

    def legalMoves(self, board, debug=False):
        """ Placeholder method so that code doesn't error on pieces which do not yet
        have a legalMoves method implemented """
        return []

    def updateBoard(piece, board, prevRank, prevFile):
        """ Method for all Piece objects to call after executing their Move method;
        this method updates the Board object to reflect the positions of the pieces. Takes in
        a Board object, the piece's previous rank, and the piece's previous file. """
        print("UPDATEBOARD METHOD")
        print("prev: ", prevRank, prevFile)
        print("new: ", piece.rank, piece.file)
        board.putPiece(piece, piece.rank, piece.file) # put piece in its current position
        board.setOpen(prevRank, prevFile)


    def deactivate(self):
        """ To be called when a piece is captured; set it to inactive, and stop it from 
        rendering onscreen (remove its sprite) """
        self.active = False
        self.sprite.kill()

    def isAttacking(self, board, other_piece):
        """ Return True if this piece can legally capture other_piece """
        return (other_piece.rank, other_piece.file) in self.legalMoves()



    

class Knight(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = True)
        if self.clr == "w":
            self.imageFile = "assets/w_knight.png"
        elif self.clr == "b":
            self.imageFile = "assets/b_knight.png"

        self.sprite.setImageFile(self.imageFile)

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

    def legalMoves(self, board, debug=False):
        """ Return a list of the (rank, file) positions to which this piece
        can legally move (not yet considering whether a move would reveal check
        on this piece's king). Output in form of [(i0, j0), (i1, j1), ... ] """
        # TODO: check if moving anywhere at all would reveal check
        moves = [[1, 2], [1, -2], [2, 1], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]
        valid = []
        for m in moves:
            newPos = (self.rank+m[0], self.file+m[1])
            print(newPos)
            if board.validSpot(*newPos):# ensure it isn't out of bounds
                otherPiece = board.contents(*newPos, rankConverted=True)
                if otherPiece == "XX" or otherPiece.clr != self.clr: # if capturing another piece, ensure it isn't on our team
                    valid.append(newPos)

        return valid


    def move(self, board, rank, file, debug=False, rankConverted=False):
        rank, file = int(rank), int(file)
        if not rankConverted:
            rank = 7 - rank
        if not board.validSpot(rank, file):
            # dont do that smh
            return
        possibleMoves = self.legalMoves(board, debug)
        if (rank, file) in possibleMoves:
            Piece.move(self, board, rank, file, debug, rankConverted=True)
        else:
            print("Knight cannot move to ({}, {})".format(rank, file))






class Bishop(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
        if self.clr == "w":
            self.imageFile = "assets/w_bishop.png"
        elif self.clr == "b":
            self.imageFile = "assets/b_bishop.png"

        self.sprite.setImageFile(self.imageFile)

    def __str__(self):
        return self.clr + "B"

    def legalMoves(self, board, debug=False):
        """ Return a list of the (rank, file) positions to which this bishop
        could legally move. Output in form of [(i0, j0), (i1, j2), ... ] """
        valid = []
        # check along files for each direction
        directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        print("EVALUATING BISHOP MOVES")
        for d in directions:
            print(d)
            # check along the file until you hit another piece; if that piece
            # is on our team, don't include it in list of moves, otherwise, include it
            pos = (self.rank+d[0], self.file+d[1])
            print("   ", pos)
            while board.validSpot(*pos) and board.isOpen(*pos):
                print("hai", pos)
                valid.append(pos)
                pos = (pos[0]+d[0], pos[1]+d[1])
            print("oh")
            if board.validSpot(*pos) and board.contents(*pos, rankConverted=True).clr != self.clr:
                # it's an enemy piece! capturing it is a legal move!
                valid.append(pos)

        return valid


    def move(self, board, rank, file, debug=False, rankConverted=False):
        rank, file = int(rank), int(file)
        if not rankConverted:
            rank = 7 - rank
        if not board.validSpot(rank, file):
            # dont do that smh
            return
        possibleMoves = self.legalMoves(board, debug)
        if (rank, file) in possibleMoves:
            Piece.move(self, board, rank, file, debug, rankConverted=True)
        else:
            print("Bishop cannot move to ({}, {})".format(rank, file))


class Rook(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
        if self.clr == "w":
            self.imageFile = "assets/w_rook.png"
        elif self.clr == "b":
            self.imageFile = "assets/b_rook.png"

        self.sprite.setImageFile(self.imageFile)


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

        self.sprite.setImageFile(self.imageFile)

    def __str__(self):
        return self.clr + "Q"

class King(Piece):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
        if self.clr == "w":
            self.imageFile = "assets/w_king.png"
        elif self.clr == "b":
            self.imageFile = "assets/b_king.png"

        self.sprite.setImageFile(self.imageFile)
        
    def __str__(self):
        return self.clr + "K"
    


class Pawn(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, canJump = False)
        if self.clr == "w":
            self.imageFile = "assets/w_pawn.png"
            self.dir = 1 # white pawns only move "up" on board (rank increases)
        elif self.clr == "b":
            self.imageFile = "assets/b_pawn.png"
            self.dir = -1 # black pawns only move "down" on board (rank decreases)
        self.hasMoved = False # use to determine if pawn can move two spaces or one

        self.sprite.setImageFile(self.imageFile)

    def __str__(self):
        return self.clr + "p"

    def legalMoves(self, board, debug=False):
        """ Return a list of the (rank, file) positions to which this pawn
        could legally move. Output in form of [(i0, j0), (i1, j2), ... ] """
        return self.capturingMoves(board, debug) + self.noncapturingMoves(board, debug)

    def capturingMoves(self, board, debug=False):
        """ Return a list of the places this piece can legally move IF
        it is capturing (i.e. a diagonal move). """
        moves = []
        otherPiece = board.contents(self.rank+self.dir, self.file+1, rankConverted=True)

        if not board.isOpen(self.rank+self.dir, self.file+1) and otherPiece.clr != self.clr: # capture diagonally forward, rights
            moves.append((self.rank+self.dir, self.file+1))
        otherPiece = board.contents(self.rank+self.dir, self.file-1, rankConverted=True)
        if not board.isOpen(self.rank+self.dir, self.file-1) and otherPiece.clr != self.clr: # capture diagonally forward, left
            moves.append((self.rank+self.dir, self.file-1))

        return moves

    def noncapturingMoves(self, board, debug=False):
        moves = []
        if not self.hasMoved and board.isOpen(self.rank+2*self.dir, self.file): # double move on first turn
            # print("can move two!")
            moves.append((self.rank+2*self.dir, self.file))
        if board.isOpen(self.rank+self.dir, self.file):
            moves.append((self.rank+self.dir, self.file)) # regular move forward

        return moves


    def canMove(self, board, rank, file, debug=False):
        """ Takes in a position (rank, file) and returns whether 
        this pawn can legally move to that position """
        # if rank 
        # if board.isOpen(rank, file)
        pass

    def move(self, board, rank, file, debug=False, rankConverted=False):
        """ Move this piece to the specified rank and file
        on the provided board if it is a legal move; else,
        raise an error. """
        # TODO: remember to add en passant rules lol but i'm tired now it's 3 AM
        # adjust rank to board coords so we can properly check moves
        if not rankConverted:
            rank = 7 - rank
        if not board.validSpot(rank, file):
            # u can't do that!!
            # raise InvalidMoveException
            return
        elif board.isOpen(rank, file):
            # cool! now lets check if pawns can do this move lol
            # can only do a forwards move if the target space is empty
            if (rank, file) in self.noncapturingMoves(board, debug):
                # we can move here!
                Piece.move(self, board, rank, file, debug, rankConverted=True)
            else:
                print("Pawn cannot move to " + str((rank, file)))

        else:
            # there's a piece here! let's capture it!! but we can only do capturing move diagonally
            # TODO: check if this move reveals check; if so, don't allow the move
            

            if (rank, file) in self.capturingMoves(board, debug):
                Piece.move(self, board, rank, file, debug, rankConverted=True)
            else:
                print("Pawn cannot move to " + str((rank, file)))


def rankFileToCoords(rank, file):
    """ Takes in rank and file values and returns the corresponding (i, j) coordinate (i 
    refers to y axis, j refers to x axis) """ 
    # file = 7 - file
    y = main.displayHeight - main.edgeBuffer - rank*main.squareWidth - 0.5*main.squareWidth
    x = main.edgeBuffer + file*main.squareWidth + 0.5*main.squareWidth
    return (x,y)


            


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, piece):
        pygame.sprite.Sprite.__init__(self)
        self.piece = piece # keep a pointer to the Piece object it corresponds to
        self.image = ":)" # gets set in setImageFile
        self.rect = ":))" # gets set in setImageFile

    def setImageFile(self, file):
        self.image = pygame.image.load(file)
        self.image = pygame.transform.scale(self.image, (int(main.squareWidth*0.7), int(main.squareWidth*0.7)))
        self.rect = self.image.get_rect()
        self.rect.center = rankFileToCoords(self.piece.rank, self.piece.file) #(displayWidth/2, displayHeight/2)
        
    def updatePosition(self, rank, file):
        """ Set this piece's rank and file to the provided values """
        self.rank = rank
        self.file = file
        self.rect.center = rankFileToCoords(self.piece.rank, self.piece.file)

    def update(self):
        self.rect.center = rankFileToCoords(self.piece.rank, self.piece.file)

    def __repr__(self):
        return str(self.piece) + " sprite"

    # @property
    # def image(self):
    #     img = pygame.image.load(self.piece.imageFile)
    #     return pygame.transform.scale(img, (int(main.squareWidth*0.7), int(main.squareWidth*0.7)))


