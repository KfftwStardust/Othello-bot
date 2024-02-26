from functions import *
import random
from math import floor


def main():
    human_move=99
    game_string = " "
    num_of_games = 0
    win_amount = 0
    difficulty = " "
    while not difficulty.isdigit():
        difficulty=input("Choose difficulty level 1 or 2 or 3 ")
    difficulty=int(difficulty)
    board=new_game()
    last_computer_move=99
    PLAYER=1
    constants=[1,1,1,1,1,1,
               2,100,40,5,5,2,
               10,801.724,382.026,78.922,74.396,10]
    constants= constants[(difficulty-1)*6:difficulty*6]
    while True:
        POSSIBLE_MOVES = get_possible_moves(board, PLAYER)
        
        if POSSIBLE_MOVES ==[0] and get_possible_moves(board,-PLAYER)==[0]:
            print_board(board,POSSIBLE_MOVES,last_computer_move)
            winner=who_wins(board)
            print( "The game is a draw" if winner ==0 else "You win" if winner >0 else "You lost" )
            num_of_games +=1
            
            if winner > 0:
                win_amount +=1
                print(win_amount/num_of_games, num_of_games, file=open('win_rate.txt', 'a'))
            
            print(constants[0:12], file=open('eval_values.txt', 'a'))
            
            print(game_string, file=open('games.txt','a'))
            game_string = " "
            
            board=new_game()
            last_computer_move=99
            PLAYER=1
            POSSIBLE_MOVES = get_possible_moves(board, PLAYER)
        
        elif POSSIBLE_MOVES!=[0]:
            
            old_board=board
            
            print_board(board,POSSIBLE_MOVES,last_computer_move)
            if PLAYER==1:
                """The human player"""
                print("Player",PLAYER if PLAYER==1 else 2,"turn")
                print("Possible moves:", POSSIBLE_MOVES)
                human_move = " "
                while not human_move.isdigit():
                    # Find the human move in the text input and detect if some other shit is typed in the console
                    human_move=str(input("Choose a position from the list: ")) or " "
                    if any(int(human_move) == p for p in POSSIBLE_MOVES) == False:
                        human_move = " "
                last_computer_move = 99
                board=is_getting_flipped(int(human_move),old_board, PLAYER)
                
                game_string +=chr(96+floor(int(human_move)/10))+str(int(human_move)%10) + " "
                
                
                
            elif PLAYER ==-1:
                """The computer player"""
                
                computer_move = get_best_move(old_board,PLAYER,6,constants)
                
                board=is_getting_flipped(computer_move,board,PLAYER)
                last_computer_move = computer_move
                game_string += chr(96+floor(computer_move/10))+str(computer_move%10) + " "
        PLAYER = -PLAYER
        

if __name__ == "__main__":
    main()