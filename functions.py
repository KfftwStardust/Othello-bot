from math import floor
from random import random
def change_board(pos,jboard,kplayer):
    # changes one position to the current players colour
    jboard[int(pos%10)][int(floor(pos/10))]=kplayer
    return jboard

def get_possible_moves(sboard, lplayer):
    # Finds all possible moves by iterating through all board positions
    POSSIBLE_MOVES = []
    for i in range(8):
        for j in range(8):
            if sboard[i][j] == 0:
                if is_valid_move(sboard, i, j, lplayer):
                    POSSIBLE_MOVES.append(j*10+i+11)
    POSSIBLE_MOVES.sort()
    if POSSIBLE_MOVES==[]:
        POSSIBLE_MOVES.append(0)
    return POSSIBLE_MOVES

def print_board(board, POSSIBLE_MOVES,last_computer_move):
    # prints the current board with your current possible moves and the last computer move played
    print("   1  2  3  4  5  6  7  8")
    for i in range(8):
        print(i + 1, end=" ")
        for j in range(8):
            position = int(10*int(j)+int(i)+11)
            if any(position == p for p in POSSIBLE_MOVES):
                print('🟢', end=' ') #🟢🔵
            elif position == last_computer_move:
                print('⬜', end=' ')
            else:                          
                print('⚪' if board[i][j] == -1 else '⚫' if board[i][j] == 1 else '🟩', end=' ')
        print()

def is_valid_move(dboard, row, col, layer):
    if dboard[row][col] != 0:
        return False

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

    for direction in directions:
        if is_valid_direction(dboard, row, col, direction, layer):
            return True

    return False

def is_valid_direction(cboard, row, col, direction, cplayer):
    opponent =  - cplayer
    i, j = direction

    x, y = row + i, col + j
    if not (0 <= x < 8 and 0 <= y < 8) or cboard[x][y] != opponent:
        return False

    x += i
    y += j

    while 0 <= x < 8 and 0 <= y < 8:
        if cboard[x][y] == cplayer:
            return True
        elif cboard[x][y] == 0:
            return False

        x += i
        y += j

    return False

def is_getting_flipped(pos,iboard,pplayer):
    # Decides which pieces are getting flipped when a piece is played
    pos -=11
    
    if pos < 0:
        # Workaround for a special case in the minimax algoritm
        return iboard
    # Decide the starting positions in the array
    y=int(pos%10)
    x=int(floor(pos/10))
    # Decide which direction from the starting piece the function searches for new peices
    # Directions consists of three parts. 
    # The first part is the first two numbers, they decide the direction like a vector
    # The second part is the third value which decides how many times it's supposed to iterate through the 2d array, this is unique for each direction
    # the thrisd part is the last two numbers which is the starting posistion for the operation
    directions = [(0, 1,7-y,x,y), 
                  (1, 0,7-x,x,y), 
                  (0, -1,y,x,y), 
                  (-1, 0,x,x,y), 
                  (1, 1,min(7-x,7-y),x,y), 
                  (-1, -1,min(x,y),x,y), 
                  (-1, 1,min(x,7-y),x,y), 
                  (1, -1,min(7-x,y),x,y)]
    output=[pos]
    opp = -pplayer 
    new_board = [row[:] for row in iboard]
    for direction in directions:
        dx, dy, iteration_amount, x, y = direction
        temp=[]
        
        for b in range(iteration_amount):
            y += dy
            x += dx
            """if max(x,y)>7 or min(x,y)<0:
                # stops it from itarion outside of the board, and generating error messages
                break"""
            if new_board[y][x] == opp:
                # change the opponents tile to yours if it gets itareted over
                temp.append(10*x+y)
            if new_board[y][x] == 0:
                # if it finds an empty tile, wipe the array and restart in anpther direction 
                temp=[]
                break    
            if new_board[y][x] == pplayer:
                # if it finds your own colour tile, move the result to the output array and restart with another direction
                output.extend(temp)
                temp=[]
                break
    for pos in output:
        # change all the positions that were the opponents and the position that was played
        new_board=change_board(pos,new_board,pplayer)
    return new_board

def evaluate_othello(board, player, constants):
    # The main eval funtion that adds up the eval from the children functions below.
    score = 0
    player_front_tiles = 0
    opp_front_tiles = 0
    # Define the weights for each position on the board
    weights = [
        
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
        ]

    dx = [-1, -1, 0, 1, 1, 1, 0, -1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]
    
    # Calculate the score based on the player's pieces and the weights
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                score += weights[i][j]
            elif board[i][j] == -player:
                score -= weights[i][j]
            if board[i][j]==0:
                for k in range(8):
                        x = i + dx[k]
                        y = j + dy[k]
                        if (x >= 0 and x < 8 and y >= 0 and y < 8 and
                                board[x][y] == 0):
                            if board[i][j] == player:
                                player_front_tiles += 1
                            else:
                                opp_front_tiles += 1
                            break
    if player_front_tiles > opp_front_tiles:
        fscore = -100*player_front_tiles / (player_front_tiles+opp_front_tiles)
    elif player_front_tiles < opp_front_tiles:
        fscore = 100*opp_front_tiles / (player_front_tiles+opp_front_tiles)
    else:
        fscore = 0        
     
    
    return (constants[0] * piece_count_eval(board,player)) + (constants[1] * corner_occupancy_eval(board,player)) + (constants[2] * corner_closeniness_eval(board,player)) + \
               (constants[3] * mobility_eval(board,player)) + (constants[4] * fscore) + (constants[5] * score)

def piece_count_eval(board, player):
    # evaluates according to piece count 
    player_tiles = sum(row.count(player) for row in board)
    opp_tiles = sum(row.count(-player) for row in board)
    if player_tiles > opp_tiles:
        score = 100*player_tiles / (player_tiles+opp_tiles)
    elif player_tiles < opp_tiles:
        score = -100*opp_tiles / (player_tiles+opp_tiles)
    else:
        score = 0
    return score

def corner_occupancy_eval(board,player):
    corners=[[0,0],[0,7],[7,0],[7,7]]
    score = 0
    for each in corners:
        if board[each[0]][each[1]] == player:
            score += 1
        elif board[each[0]][each[1]] == -player:
            score -= 1
    
    return 25*score

def corner_closeniness_eval(board,player):
    corners=[[0,0],[7,0],[0,7],[7,7]]
    d = [[1,1], [1,0], [0,1], [-1,1], [0,1], [-1,0], [1,-1], [0,-1], [1,0], [-1,-1], [-1,0], [0,-1]] 
    score=0
    for c in range(4):
        if board[corners[c][0]][corners[c][1]] == 0:
            for b in range(3):
                if board[corners[c][0]+d[3*c+b][0]][corners[c][1]+d[3*c+b][1]] == player:
                    score +=1
                elif board[corners[c][0]+d[3*c+b][0]][corners[c][1]+d[3*c+b][1]] == -player:
                    score -=1
    
    return -12.5*score

def mobility_eval(board, player):
    # evalutaes according ot mobilty. aka how many possible moves are available, relative to the total amount of moves
    poss_P1 = get_possible_moves(board,player)
    poss_P2 = get_possible_moves(board,-player)
    if poss_P1[0]==0:
        poss_P1=[]
    if poss_P2[0]==0:
        poss_P2=[]
    
    if len(poss_P1)>len(poss_P2):
        score=100*len(poss_P1)/(len(poss_P1)+len(poss_P2))
    elif len(poss_P2)>len(poss_P1):
        score=-100*len(poss_P2)/(len(poss_P1)+len(poss_P2))
    else:
        score = 0
    return score

def minimax(position, depth, alpha, beta, Player,constants):
    
    Posible_moves=get_possible_moves(position,Player)
    if depth == 0 or(Posible_moves ==[] and get_possible_moves(position,-Player)==[]):
        return (evaluate_othello(position,Player,constants),1) if depth == 0 else (who_wins(position), 1)
    best_move=0
    if Player==-1:
        maxEval = -10**100
        for each in Posible_moves:
            eval, _ = minimax(is_getting_flipped(each,position,Player), depth - 1, alpha, beta, -Player,constants)
            if maxEval< eval:
                maxEval=eval
                best_move=each
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return (maxEval, best_move)
    
    else:
        minEval = 10**100
        for each in Posible_moves:
            eval, _ = minimax(is_getting_flipped(each,position,Player), depth - 1, alpha, beta, -Player,constants)
            if minEval> eval:
                minEval=eval
                best_move=each
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return (minEval, best_move)

def get_best_move(board,Player,depth,constants):
    #Finds the best move according to the current version of the minimax algoritm. It's a separate function because we had a plan to add an opening book aswell.
    _ , best_move =minimax(board, depth, -float('inf'), float('inf'), Player, constants)
    #print("best move",best_move)
    return best_move

def new_game():
    #Creates a new board and readies it for a new game
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
    # decides who wins the game
    score=sum(row.count(1) for row in board)-sum(row.count(-1) for row in board)
    if score == 0:
        return 0 #"The game ended in a Draw"
    else:
        return 10**100 if score > 0 else -10**100

def constants_change(constant,board):
    # Changes the constants used in the eval function, is only used when the bot is training. It's supposed to find some good ish values for the eval funtion
    constants=constant
    who_won=int(who_wins(board))
    
    if who_won >0:
        for b in range(6):
            constants[b+6]=constants[b]
            constants[b] += 2*random()
    if who_won <=0:
        for b in range(6):
            constants[b]=constants[b+6]
            constants[b+6] += 2*random()
        
    return constants
