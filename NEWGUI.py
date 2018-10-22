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

if len(sys.argv) == 3: # we have additional param: file to read in!
    readInFile = sys.argv[2]
    try:
        gameBoard = Board.Board(readInFile)
    except:
        gameBoard = Board.Board(readInFile)
        # print("could not find specified filepath! loading standard board")
        # gameBoard = Board.Board() # just a default board
else:
    gameBoard = Board.Board() # just a default board

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
    """ takes in a position tuple and returns the corresponding rank, file square """
    x, y = pos[0], pos[1]
    x -= edgeBuffer
    y -= edgeBuffer
    numX, marginX = x // squareWidth, x % squareWidth
    numY, marginY = y // squareWidth, y % squareWidth
    # print(numX, numY)
    return numX, 7-numY

def findDirectCoordinates(pos):
    """ Return coordinates in standard pygame coordinates, but centered on
    whatever square contains pos. Used only for square method testing. """
    pass

def handleClick(pos):
    global gameBoard, selectedPiece, allPieces, highlightSquares
    # print('haii')

    if debug:
        clickPosition = findCoordinates(pos)
        highlightSquare(pos)
        print("c: ", clickPosition)
        print("is there a piece here??")
        highlightSquare(pos)
        print("ooo", gameBoard.contents(clickPosition[1], clickPosition[0], True))
        mouseSprite = MouseSprite(pos)
        collidedPiece = pygame.sprite.spritecollideany(mouseSprite, allPieces)
        if selectedPiece: # we already have a selected piece
            # move that piece here if it's legal; deselect it no matter what
            if (not collidedPiece) or collidedPiece.piece != selectedPiece.piece:
                # either moving onto empty square, or capturing piece which isn't itself! no suicidal chess pieces :c
                selectedPiece.piece.move(gameBoard, clickPosition[1], clickPosition[0], debug, rankConverted=True)
                print("* ", selectedPiece.piece.rank, selectedPiece.piece.file)
            
            selectedPiece = None
            highlightSquares = []

        else:
            # did the mouse collide with a piece? construct sprite for mouse and check for collisions
            
            
            if collidedPiece: # collidedPiece is None if there was no collision
                # set this piece to be the selected piece
                selectedPiece = collidedPiece
                possibleMoves = selectedPiece.piece.legalMoves(gameBoard, debug)
                print("possible moves are!!: ", possibleMoves)
                for move in possibleMoves:
                    highlightSquare(move)
                print(str(collidedPiece) + " is now selected")
            else:
                # highlightSquares = []
                pass # nvm this highlighting stuff honestly

        print("after a click, " + str(selectedPiece) +  " is selected")



def highlightSquare(pos):
    """ Place a semi-transparent highlighting color over the square at the indicated (i,j) coordinate
    to highlight it (to indicate legal moves, probably) """
    global display, highlightSquares
    print("hello! ", pos)
    blitPosition = rankFileToCoords(*pos)
    see_through = pygame.Surface((squareWidth, squareWidth)).convert_alpha()
    see_through.fill(RED_HIGHLIGHT)
    see_through_rect = see_through.get_rect(center=blitPosition)
    highlightSquares.append([see_through, see_through_rect])
    # display.blit(see_through, see_through_rect)

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
RED_HIGHLIGHT = (240, 50, 50, 100)

allPieces = pygame.sprite.Group()

clock = pygame.time.Clock()

x = (displayWidth * 0.45)
y = (displayHeight * 0.5)



# get the board!
# gameBoard = Board.Board()

def readBoard(board):
    """ Go through the gameboard and read in all the pieces """
    for i in range(8):
        for j in range(8):
            if board.board[i][j] != "XX":
                # there is a piece here!
                allPieces.add(board.board[i][j].sprite)

readBoard(gameBoard)
print(gameBoard)

mousePos = None # keep track of mouse position onscreen

selectedPiece = None # keep track of which piece, if any, has been selected by user (clicked)

crashed = False # has game ended? should we halt the game rendering?

highlightSquares = [] # list of squares to be highlighting

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
                elif event.key == 108: # l; print legal moves for selected piece
                    if selectedPiece and hasattr(selectedPiece.piece, "legalMoves"):
                        print(str(selectedPiece) + " legal moves: " + str(selectedPiece.piece.legalMoves(gameBoard, debug)))
                    else:
                        print(str(selectedPiece) + " does not have a legalMoves method implemented :(")

                elif event.key == 100: # d; deactivate/kill the selected piece
                    if selectedPiece:
                        selectedPiece.piece.deactivate()
                    else:
                        print("No selected piece to deactivate :(")

                elif event.key == 118: # v; save board to file
                    gameBoard.save("savefile.csv")

                elif event.key == 104: # h; highlight a square
                    pos = input("type the location to highlight! ") # should be in (x, y) format
                    pos = pos[1:-1] # trim parentheses
                    pos = pos.replace(" ", "") # get rid of spaces so it's in format x,y
                    pos = pos.split(",") # split into [x, y]
                    pos_tuple = tuple(map(int, pos)) # convert to integers
                    highlightSquare(pos_tuple)

                elif event.key == 107: # k; take in rank, file and print board contents
                    r = input("type the rank of the square whose contents you want: ")
                    f = input("type the file of the square whose contents you want: ")
                    r = int(r)
                    f = int(f)
                    print(gameBoard.contents(r, f, True))
            pass

    sqs = []
    display.fill(WHITE)
    renderBoard()
    for sq in highlightSquares:
        display.blit(*sq)
    allPieces.draw(display)
    # see_through = pygame.Surface((100,100)).convert_alpha()
    # see_through.fill(RED_HIGHLIGHT)
    # see_through_rect = see_through.get_rect(bottomleft=display.get_rect().center)
    # sqs.append([see_through, see_through_rect])

    # see_through = pygame.Surface((100,100)).convert_alpha()
    # see_through.fill(RED_HIGHLIGHT)
    # see_through_rect = see_through.get_rect(center=display.get_rect().center)
    # sqs.append([see_through, see_through_rect])

    for pr in sqs:
        display.blit(*pr)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()



