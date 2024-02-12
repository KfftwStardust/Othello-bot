from functions import *

board=new_game()
change_board(1,board,1)
change_board(11,board,1)
change_board(10,board,1)
print(corner_closeniness_eval(board,1))