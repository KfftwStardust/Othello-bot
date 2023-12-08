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

def print_board(board, POSSIBLE_MOVES):
    OSSIBLE_MOVES=POSSIBLE_MOVES
    print("   1  2  3  4  5  6  7  8")
    for i in range(8):
        print(i + 1, end=" ")
        for j in range(8):
            if any(int(10*int(j)+int(i)+11) == p for p in OSSIBLE_MOVES):
                print('🟢', end=' ') #🟢🔵
            else:                          
                print('⚪' if board[i][j] == -1 else '⚫' if board[i][j] == 1 else '🟩', end=' ')
        print()


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
    POSSIBLE_MOVES = get_possible_moves(board, PLAYER)
    #print_board(board,POSSIBLE_MOVES)
    if get_possible_moves(board,-PLAYER)==[] and POSSIBLE_MOVES==[]:
        print(who_wins(board))
        input("Press Enter for a new game")
        
        board=new_game()
        PLAYER=1
        
        
    POSSIBLE_MOVES = get_possible_moves(board, PLAYER)
    print_board(board,POSSIBLE_MOVES)
    if POSSIBLE_MOVES!=[]:
        old_board=board
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
            POS=get_best_move(old_board) 
            print(POS)
            input()
            #print_board(board,POSSIBLE_MOVES)   
            board=is_geting_flipped(int(POS)-11,board,PLAYER)
    PLAYER = -PLAYER
     
