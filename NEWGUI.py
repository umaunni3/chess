import pygame
from Piece import *
import sys
import Board
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

class MouseSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = pos


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

def findCoordinates(pos):
    """ takes in a position tuple and returns the corresponding i, j square """
    x, y = pos[0], pos[1]
    x -= edgeBuffer
    y -= edgeBuffer
    numX, marginX = x // squareWidth, x % squareWidth
    numY, marginY = y // squareWidth, y % squareWidth
    # print(numX, numY)
    return numX, numY

def handleClick(pos):
    global gameBoard, selectedPiece, allPieces
    # print('haii')

    if debug:
        clickPosition = findCoordinates(pos)
        print(clickPosition)
        if selectedPiece:
            # move that piece here
            selectedPiece.piece.move(gameBoard, clickPosition[1], clickPosition[0], debug)
            print("* ", selectedPiece.piece.rank, selectedPiece.piece.file)
            selectedPiece = None

        else:
            # did we collide with a piece? construct sprite for mouse and check for collisions
            mouseSprite = MouseSprite(pos)
            collidedPiece = pygame.sprite.spritecollideany(mouseSprite, allPieces)
            if collidedPiece: # collidedPiece is None if there was no collision
                # set this piece to be the selected piece
                selectedPiece = collidedPiece
                print(str(collidedPiece) + " is now selected")

        print("after a click, " + str(selectedPiece) +  " is selected")




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

allPieces = pygame.sprite.Group()

clock = pygame.time.Clock()

x = (displayWidth * 0.45)
y = (displayHeight * 0.5)



# get the board!
gameBoard = Board.Board()

def readBoard(board):
    """ Go through the gameboard and read in all the pieces """
    for i in range(8):
        for j in range(8):
            if board.board[i][j] != "XX":
                # there is a piece here!
                allPieces.add(board.board[i][j].sprite)

readBoard(gameBoard)

mousePos = None # keep track of mouse position onscreen

selectedPiece = None # keep track of which piece, if any, has been selected by user (clicked)

crashed = False # has game ended? should we halt the game rendering?

while not crashed:
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # mouse down
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            # mouse up
            handleClick(mousePos)
            pass
        elif event.type == pygame.KEYDOWN:
            # esc key
            if debug: # various testing functionalities to print info to the terminal during execution
                print(event.key)
                if event.key == 99: # c; clear the selectedPiece
                    selectedPiece = None # clear it
                elif event.key == 115: # s; print what the current selectedPiece is
                    print("current selected piece is " + str(selectedPiece))
                elif event.key == 112: # p; print the position of the selectedPiece
                    if selectedPiece:
                        print("selectedPiece position is", + selectedPiece.piece.rank, selectedPiece.piece.file)
                    else:
                        print("no piece currently selected!")
            pass
    display.fill(WHITE)
    renderBoard()
    allPieces.draw(display)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()



