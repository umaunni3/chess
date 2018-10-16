# while game_not_over:
# 	play_good_move()
from Board import * 

def main():
	board = Board()
	print("Begin")
	while not board.finished and count < 5:
		print(board)
		board.update()
  
if __name__== "__main__":
	main()
