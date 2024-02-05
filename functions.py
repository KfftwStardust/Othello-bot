import math
import random
def change_board(pos,jboard,kplayer):
    
    temp = jboard[pos%10]
    temp[math.floor(pos/10)]= kplayer
    jboard[pos%10] = temp
    return jboard

def get_possible_moves(sboard, lplayer,inMinimax):
    POSSIBLE_MOVES = []

    for i in range(8):
        for j in range(8):
            if sboard[i][j] == 0:
                if is_valid_move(sboard, i, j, lplayer):
                    POSSIBLE_MOVES.append(j*10+i+11)
    POSSIBLE_MOVES.sort()
    """if inMinimax:
        temp = []
        for each in POSSIBLE_MOVES:
            temp.append(minimax(is_getting_flipped(each-11,sboard,lplayer),1, -float('inf'), float('inf'), -1,False))
        temp.sort()
        POSSIBLE_MOVES=[]
        for value in temp:
            POSSIBLE_MOVES.append[int(value%100)]"""
    if POSSIBLE_MOVES==[]:
        POSSIBLE_MOVES.append(0)
    return POSSIBLE_MOVES

def print_board(board, POSSIBLE_MOVES,last_computer_move):
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
    pos -=11
    if pos < 0:
        return iboard
    y=pos%10
    x=math.floor(pos/10)
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
        i, j, t, x, y = direction
        temp=[]
        r=0
        for b in range(t):
            #print("temp",temp,"output",output,"x",x,"y",y,"board",r,"b",b,"direction",direction,"pos",pos,"bef")
            y += j
            x += i
            if max(x,y)>7 or min(x,y)<0:
               break
            if new_board[y][x] == opp:
                temp.append(10*x+y)
            if new_board[y][x] == 0:
                temp=[]
                break    
            if new_board[y][x] == pplayer:
                output.extend(temp)
                temp=[]
                break
            r=new_board[y][x]
            """print("temp",temp,"output",output,"x",x,"y",y,"board",r,"b",b,"direction",direction,"pos",pos,"aft")
        if board[y][x] == pplayer:
                output.extend(temp)
                print(temp)
                temp=[]"""  
    for pos in output:
        new_board=change_board(pos,new_board,pplayer)
    return new_board

def evaluate_board(lboard, Player):

    score = 0

    # Define the weights for each position on the board
    weights = [
        [100, -20, 10, 5, 5, 10, -20, 100],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [10, -2, -1, -1, -1, -1, -2, 10],
        [5, -2, -1, -1, -1, -1, -2, 5],
        [5, -2, -1, -1, -1, -1, -2, 5],
        [10, -2, -1, -1, -1, -1, -2, 10],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [100, -20, 10, 5, 5, 10, -20, 100],
    ]

    # Calculate the score based on the player's pieces and the weights
    """ Olika strategier, minsta antalet disks i early game, få motståndaren att ha få drag.
        mobilty: titta på hemsidan 'https://www.samsoft.org.uk/reversi/strategy.htm', stable disks, frontiers,
        parity
        """
    for i in range(8):
        for j in range(8):
            if lboard[i][j] == 1:
                score += weights[i][j]
            elif lboard[i][j] == -1:
                score -= weights[i][j]
    score = score*Player 
    return score 
# Den är nog skit Chatgpt skrev den
def piece_count_eval(board, player):
    player_pieces = sum(row.count(player) for row in board)
    opponent_pieces = sum(row.count(-player) for row in board)
    return player_pieces - opponent_pieces

def mobility_eval(board, player):
    player_legal_moves = len(get_possible_moves(board, player,False))
    opponent_legal_moves = len(get_possible_moves(board, -player,False))
    return player_legal_moves - opponent_legal_moves
def evaluate_othello(board, player, constants):
    
    
    # Determine the game stage based on the number of pieces or empty spaces
    total_pieces = sum(row.count(1) + row.count(-1) for row in board)
    if player==1:
        n=0
    else:
        n=4

    if total_pieces >= 55:
        # Late game strategy
        score = piece_count_eval(board, player)
    elif total_pieces >= 30:
        # Mid game strategy
        score = piece_count_eval(board, player) + constants[n]*mobility_eval(board, player) + constants[n+1]*evaluate_board(board,player)
    else:
        # Early game strategy
        score = piece_count_eval(board, player) + constants[n+2]* mobility_eval(board, player) + constants[n+3]*evaluate_board(board,player)

    return int(score)

def minimax(position, depth, alpha, beta, Player,inMinimax,constants):
    Posible_moves=get_possible_moves(position,Player,inMinimax)
    if depth == 0 or(Posible_moves ==[] and get_possible_moves(position,-Player,False)==[]):
        return evaluate_othello(position,Player,constants) 
    
    
    if Player==-1:
        maxEval = -10**100
        for each in Posible_moves:
            eval = minimax(is_getting_flipped(each,position,Player), depth - 1, alpha, beta, -Player, inMinimax,constants)*100+each
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval	
    
    else:
        minEval = 10**100
        for each in Posible_moves:
            eval = minimax(is_getting_flipped(each,position,Player), depth - 1, alpha, beta, -Player, inMinimax,constants)*100+each
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def get_best_move(board,Player,depth,constants):

    best_move=minimax(board, depth, -float('inf'), float('inf'), Player, True, constants)%100
    #print(best_move+11)
    return best_move

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

def who_wins(board,player):
    score=piece_count_eval(board,player)
    if score == 0:
        return "Player 0 " #"The game ended in a Draw"
    else:
        return "Player 1 wins" if score > 0 else "Player 2 wins"

def constants_change(constant,board):
    constants=constant
    who_won=int(who_wins(board)[7:8])
    
    if who_won == 2:
        constants[4]=constants[0]
        constants[5]=constants[1]
        constants[6]=constants[2]
        constants[7]=constants[3]
        multiplier = 2*random.random()-1
        constants[4] += (2*random.random()-1)/multiplier
        constants[5] += (2*random.random()-1)/multiplier
        constants[6] += (2*random.random()-1)/multiplier
        constants[7] += (2*random.random()-1)/multiplier
    if who_won ==1:
        constants[0]=constants[4]
        constants[1]=constants[5]
        constants[2]=constants[6]
        constants[3]=constants[7]
        multiplier = 2*random.random()-1
        constants[4] += (2*random.random()-1)/multiplier
        constants[5] += (2*random.random()-1)/multiplier
        constants[6] += (2*random.random()-1)/multiplier
        constants[7] += (2*random.random()-1)/multiplier
    return constants