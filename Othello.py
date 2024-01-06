from functions import *


def new_game():
    board=[]
    for q in range(8):
        x=[]
        for o in range(8):
            x.append(int(0))
        board.append(x)
    change_board(33,board,-1)
    change_board(44,board,-1)
    change_board(43,board,1)
    change_board(34,board,1)
    return board




def who_wins(board):
    p1_score=0
    p2_score=0
    for u in range(8):
        for r in range(8):
            if board[u][r]==-1:
                p1_score +=1
            if board[u][r]==1:
                p2_score +=1
    if p1_score == p2_score:
        return "The game ended in a Draw"
    else:
        return "Player 1 wins" if p1_score > p2_score else "Player 2 wins"


#minimax(board,depth,-10^999999,10^999999,PLAYER)

board=new_game()
PLAYER=1



while True:
    POS=0
    POSSIBLE_MOVES = get_possible_moves(board, PLAYER,False)
    #print_board(board,POSSIBLE_MOVES)
    if get_possible_moves(board,-PLAYER,False)==[] and POSSIBLE_MOVES==[]:
        print_board(board,POSSIBLE_MOVES)
        print(who_wins(board))
        input("Press Enter for a new game")
        
        board=new_game()
        PLAYER=1
        
        
    
    
    if POSSIBLE_MOVES!=[]:
        old_board=board
        print_board(board,POSSIBLE_MOVES)
        if PLAYER==1:
            
            print("Possible moves:", POSSIBLE_MOVES)
            print("Player",PLAYER if PLAYER==1 else 2,"turn")
            POS = 99
            while POS==99:
                POS=str(input("Vilken pos 11 till 88 ")) or ' '
                #if len(POS)==2:
                    #POS=str(ord(POS[0:1])-96)+str(POS[1:2])
                if not POS.isdigit():
                    POS=99
                if any(int(POS) == p for p in POSSIBLE_MOVES) == False:
                    POS = 99
            board=is_geting_flipped(int(POS)-11,board,PLAYER)
        if PLAYER ==-1:
            start_time = timeit.default_timer()
            POS = get_best_move(old_board,PLAYER,7)
            end_time = timeit.default_timer()
            print(f"Time taken for get_best_move: {end_time - start_time} seconds")
            board=is_geting_flipped(int(POS),board,PLAYER)
    PLAYER = -PLAYER
     
