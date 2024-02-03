from functions import *

board=new_game()
PLAYER=1

constants=[7.95265448247082, 3.3591377304196834, 0.12550102679935993, 6.847242107087103, 12.660532007361532, 11.464745778183207, 3.50764725402987, 13.122139178795013]

while True:
    POS=0
    POSSIBLE_MOVES = get_possible_moves(board, PLAYER,False)
    #print_board(board,POSSIBLE_MOVES)
    if get_possible_moves(board,-PLAYER,False)==[0] and POSSIBLE_MOVES==[0]:
        print_board(board,POSSIBLE_MOVES)
        print(who_wins(board))
        #input("Press Enter for a new game")
        print(constants, file=open('eval_values.txt', 'a'))
        constants=constants_change(constants,board)
        board=new_game()
        PLAYER=1
        POSSIBLE_MOVES = get_possible_moves(board, PLAYER, False)
    
    elif POSSIBLE_MOVES!=[]:
        #print(POSSIBLE_MOVES)
        old_board=board
        #print_board(board,POSSIBLE_MOVES)
        if PLAYER==0:
            print_board(board,POSSIBLE_MOVES)
            print("Player",PLAYER if PLAYER==1 else 2,"turn")
            print("Possible moves:", POSSIBLE_MOVES)
            POS = 99
            while POS==99:
                POS=str(input("Choose of the the positions from the list ")) or ' '
                #if len(POS)==2:
                    #POS=str(ord(POS[0:1])-96)+str(POS[1:2])
                if not POS.isdigit():
                    POS=99
                if any(int(POS) == p for p in POSSIBLE_MOVES) == False:
                    POS = 99
            board=is_geting_flipped(int(POS),board,PLAYER)
        if PLAYER !=0:
            #print_board(board,[])
            #start_time = timeit.default_timer()
            POS = get_best_move(old_board,PLAYER,3,constants)
            #end_time = timeit.default_timer()
            #print(f"Time taken for get_best_move: {end_time - start_time} seconds")
            board=is_geting_flipped(POS,board,PLAYER)
    PLAYER = -PLAYER
     
