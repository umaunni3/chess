# while game_not_over:
# 	play_good_move()
from Board import * 

# stuff for GUI and Piece.py
displayWidth = 600
displayHeight = 600

squareWidth = (0.9 * displayWidth) // 8
edgeBuffer = (displayWidth - (8 * squareWidth)) / 2

def main():
	board = Board()
	print("Begin")
	while not board.finished and count < 5:
		print(board)
		board.update()
  
if __name__== "__main__":
	main()
