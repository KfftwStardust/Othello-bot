from functions import *

board=new_game()
last_computer_move=99
PLAYER=1

constants=[7.95265448247082, 3.3591377304196834, 0.12550102679935993, 6.847242107087103, 12.660532007361532, 11.464745778183207, 3.50764725402987, 13.122139178795013]

while True:
    POSSIBLE_MOVES = get_possible_moves(board, PLAYER,False)
    #print_board(board,POSSIBLE_MOVES)
    if get_possible_moves(board,-PLAYER,False)==[0] and POSSIBLE_MOVES==[0]:
        print_board(board,POSSIBLE_MOVES)
        print(who_wins(board))
        #input("Press Enter for a new game")
        print(constants, file=open('eval_values.txt', 'a'))
        constants=constants_change(constants,board)
        board=new_game()
        last_computer_move=99
        PLAYER=1
        POSSIBLE_MOVES = get_possible_moves(board, PLAYER, False)
    
    elif POSSIBLE_MOVES!=[]:
        #print(POSSIBLE_MOVES)
        old_board=board
        #print_board(board,POSSIBLE_MOVES)
        if PLAYER==1:
            print_board(board,POSSIBLE_MOVES,last_computer_move)
            print("Player",PLAYER if PLAYER==1 else 2,"turn")
            print("Possible moves:", POSSIBLE_MOVES)
            human_move = 99
            while human_move==99:
                human_move=str(input("Choose of the the positions from the list ")) or ' '
                #if len(POS)==2:
                    #POS=str(ord(POS[0:1])-96)+str(POS[1:2])
                if not human_move.isdigit():
                    human_move=99
                if any(int(human_move) == p for p in POSSIBLE_MOVES) == False:
                    human_move = 99
            board=is_getting_flipped(int(human_move),board,PLAYER)
        if PLAYER ==-1:
            #print_board(board,[])
            #start_time = timeit.default_timer()
            computer_move = get_best_move(old_board,PLAYER,3,constants)
            #end_time = timeit.default_timer()
            #print(f"Time taken for get_best_move: {end_time - start_time} seconds")
            board=is_getting_flipped(computer_move,board,PLAYER)
            last_computer_move = computer_move
    PLAYER = -PLAYER
     
