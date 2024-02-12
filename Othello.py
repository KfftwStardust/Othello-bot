from functions import *

def main():
    difficulty=" "
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
        #print_board(board,POSSIBLE_MOVES)
        if get_possible_moves(board,-PLAYER)==[0] and POSSIBLE_MOVES==[0]:
            print_board(board,POSSIBLE_MOVES,last_computer_move)
            winner=who_wins(board)
            print( "The game is a draw" if winner ==0 else "You win" if winner >0 else "You lost" )
            #input("Press Enter for a new game")
            #print(constants, file=open('eval_values.txt', 'a'))
            #constants=constants_change(constants,board)
            board=new_game()
            last_computer_move=99
            PLAYER=1
            POSSIBLE_MOVES = get_possible_moves(board, PLAYER)
        
        elif POSSIBLE_MOVES!=[0]:
            #print(POSSIBLE_MOVES)
            old_board=board
            #print_board(board,POSSIBLE_MOVES)
            print_board(board,POSSIBLE_MOVES,last_computer_move)
            if PLAYER==1:
                """The human player"""
                print("Player",PLAYER if PLAYER==1 else 2,"turn")
                print("Possible moves:", POSSIBLE_MOVES)
                human_move = 99
                while human_move==99:
                    # Find the human move in the text input and detect if some other shit is typed in the console
                    human_move=str(input("Choose of the the positions from the list ")) or " "#str(POSSIBLE_MOVES[0])
                    #if len(POS)==2:
                        #POS=str(ord(POS[0:1])-96)+str(POS[1:2])
                    if not human_move.isdigit():
                        human_move=99
                    if any(int(human_move) == p for p in POSSIBLE_MOVES) == False:
                        human_move = 99
                board=is_getting_flipped(int(human_move),board,PLAYER)
                PLAYER = -PLAYER
            if PLAYER ==-1:
                """The computer player"""
                #print_board(board,[])
                #start_time = timeit.default_timer()
                computer_move = get_best_move(old_board,PLAYER,2,constants)
                #end_time = timeit.default_timer()
                #print(f"Time taken for get_best_move: {end_time - start_time} seconds")
                board=is_getting_flipped(computer_move,board,PLAYER)
                last_computer_move = computer_move
                PLAYER = -PLAYER
        

if __name__ == "__main__":
    main()