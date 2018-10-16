import pygame
from Piece import *
import sys
# from Board import *
# import Piece
# from piece import Piece, Queen, King, Rook, Knight, Pawn, Bishop

# debug mode
if len(sys.argv) > 1 and sys.argv[1] == "--debug":
    debug = True
else:
    debug = False

if debug:
    print("running ChessBot in debug mode")


import Board

def renderBoard():
    # just render the board, not the pieces
    clr = 0
    for i in range(8):
        clr = 1 - clr # toggle the color
        for j in range(8):
            renderSquare(edgeBuffer + i*squareWidth, edgeBuffer + j*squareWidth, squareWidth, clr)
            clr = 1 - clr


def renderSquare(x, y, width, clr):
    if clr == 0:
        clr = BROWN
    else:
        clr = CREAM
    pygame.draw.rect(display, clr, [x, y, width, width], 0)



def renderPiece(fileName, pos):
    img = pygame.image.load(fileName)
    img = pygame.transform.scale(img, tuple(map(lambda x:int(x*0.7), pos)))
    display.blit(img, (x, y))

# give the Piece class a method to generate the sprite
def pieceSprite(self):
    return PieceSprite(self.imageFile, squareToCoords(self.file, self.rank), self)
# Piece.sprite = pieceSprite


pygame.init()

displayWidth = 600
displayHeight = 600

squareWidth = (0.9 * displayWidth) // 8
edgeBuffer = (displayWidth - (8 * squareWidth)) / 2


display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("chess !!!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (178, 129, 66)
CREAM = (232, 219, 204)



    # def update(self):
    #   self.rect.x += 5*self.dir
    #   if self.rect.right > displayWidth or self.rect.left < 0:
    #       self.dir *= -1

class MouseSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = pos

class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, fileName, pos, obj):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50,50))
        self.image = pygame.image.load(fileName)
        self.image = pygame.transform.scale(self.image, (int(squareWidth*0.7), int(squareWidth*0.7)))
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = pos #(displayWidth/2, displayHeight/2)
        self.dir = 1
        self.piece = obj
        self.name = obj.__str__()
    def __repr__(self):
        return self.name
    def update(self):
        self.rect.center = squareToCoords(self.piece.file, self.piece.rank)



def squareToCoords(i, j):
    # return x, y pos of center of desired square
    # (i,j) = (0, 0) is bottom left DESPITE WHAT PYGAME WANTS
    # i flip the x and y coord for u so it may be easier to use

    # flip y coord and x coord
    i, j = pygameToStandardCoords((i, j))
    # i = 7 - i
    # j = 7 - j

    x = edgeBuffer + i*squareWidth + 0.5*squareWidth
    y = edgeBuffer + j*squareWidth + 0.5*squareWidth
    return (x,y)

allPieces = pygame.sprite.Group()
# piece = PieceSprite("assets/b_queen.png", squareToCoords(3,6))
# allPieces.add(piece)



clock = pygame.time.Clock()
crashed = False
img = pygame.image.load("assets/b_queen.png")

def qn(x,y):
    display.blit(img, (x,y))




x = (displayWidth * 0.45)
y = (displayHeight * 0.5)
mouseClicked = False # use to detect a whole click (down and up)


# get the board!
gameBoard = Board.Board("hai")

def pygameToStandardCoords(pos):
    # takes a position tuple and converts it from pygame
    # coords (0, 0 at top left) to standard coords (0, 0 
    # at bottom left)
    return (7-pos[0], pos[1])


def renderPieces(b):
    for i in range(8):
        for j in range(8):
            if b.board[i][j] != "XX" : # there's a piece here!
                piece = b.board[i][j]
                # if piece.clr == "b":
                    # print(piece, type(piece))
                piece.sprite = pieceSprite(piece)
                allPieces.add(piece.sprite)


def findCoordinates(mousePos):
    # takes in a MouseSprite object with a click position
    # and returns the corresponding i, j square
    cent = mousePos.rect.center
    x, y = cent[0], cent[1]
    x -= edgeBuffer
    y -= edgeBuffer
    numX, marginX = x // squareWidth, x % squareWidth
    numY, marginY = y // squareWidth, y % squareWidth
    print(numX, numY)
    return numX, numY

mPos = None # constantly monitor mouse position

def followMouseUpdate(self):
    global mPos
    self.rect.center = mPos.rect.center

selectedPreviousUpdate = None

def specialMouseUpdate(self):
    x, y = self.rect.center[0], self.rect.center[1]
    self.rect.center = (x+1, y+1)
    # self.move(gameBoard, )

def dropPiece():
    global selectedPiece, selectedPreviousUpdate, mPos, gameBoard
    mouseSquare = findCoordinates(mPos)
    mousePosCoords = pygameToStandardCoords(mouseSquare)
    selectedPiece.piece.move(gameBoard, mouseSquare[0], mouseSquare[1], True)
    selectedPiece.update = selectedPreviousUpdate
    selectedPreviousUpdate = None
    selectedPiece = None


selectedPiece = None # piece which was clicked

mPos = None # object for mouse sprite

def handleClick(mPos):
    global selectedPiece, selectedPreviousUpdate

    if debug:
        if selectedPiece:
            print('===')
            print(selectedPiece)
            print(selectedPiece.rank, selectedPiece.file)
            print('===')

    if selectedPiece:
        selectedPiece.piece.move(gameBoard, 5, 5, True)
        return
    collided = pygame.sprite.spritecollideany(mPos, allPieces)
    print("hi" + str(selectedPiece))
    print(findCoordinates(mPos))
    if not selectedPiece and collided:
        # we dont have a previously selected piece, and we just
        # clicked on a new piece. pick it up!
        print(collided)
        selectedPiece = collided
        selectedPreviousUpdate = selectedPiece.update
        selectedPiece.update = followMouseUpdate # have it follow mouse on screen
        print("hiiiiii" + str(type(selectedPiece)))
        print(selectedPiece.update)

        # if debug:
        #     # pause so i dont get spammed a ton with prints
        #     print(collided.rect.center)
        #     collided.piece.move(1, 2, 3, True)
        #     pygame.time.delay(1000)
    elif selectedPiece:
        # set down the selected piece here
        dropPiece()


while not crashed:
    # print(crashed)
    pos = pygame.mouse.get_pos()
    mPos = MouseSprite(pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            handleClick(mPos)
            print(selectedPiece)
        elif event.type == pygame.MOUSEBUTTONUP and mouseClicked:
            # print whatever piece was clicked, if any
            # mouseClicked = False # avoid it spamming the debug output
            # handleClick()
            pass
        elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            dropPiece()
                


    display.fill(WHITE)
    # disp("assets/chessboard.JPG", 0, 0)
    # allPieces.update()
    for s in allPieces:
        # s.update()
        try:
            if s.update is followMouseUpdate or s.update is specialMouseUpdate:
                s.update(s)
            else:
                s.update()
        except TypeError:
            print('yikes', s, type(s))
            print('yikes!!', s.update)
            raise TypeError
    renderBoard()
    renderPieces(gameBoard)
    # qn(x,y)
    allPieces.draw(display)

    # check if mouse is colliding with the piece!
    pos = pygame.mouse.get_pos()
    mPos = MouseSprite(pos)
    # allPieces.add(mPos)
    # mPos = pygame.Rect(pos[0], pos[1], 1, 1)
    # if pygame.sprite.collide_rect(piece, mPos):
    #   print("yooooo!")


    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()



