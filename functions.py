import math
import timeit
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
            temp.append(minimax(is_geting_flipped(each-11,sboard,lplayer),1, -float('inf'), float('inf'), -1,False))
        temp.sort()
        POSSIBLE_MOVES=[]
        for value in temp:
            POSSIBLE_MOVES.append[int(value%100)]"""
    return POSSIBLE_MOVES

def print_board(board, POSSIBLE_MOVES):
    print("   1  2  3  4  5  6  7  8")
    for i in range(8):
        print(i + 1, end=" ")
        for j in range(8):
            if any(int(10*int(j)+int(i)+11) == p for p in POSSIBLE_MOVES):
                print('🟢', end=' ') #🟢🔵
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

def is_geting_flipped(pos,iboard,pplayer):
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
        allow=0
        r=0
        for b in range(t):
            #print("temp",temp,"output",output,"x",x,"y",y,"board",r,"b",b,"direction",direction,"pos",pos,"bef")
            y += j
            x += i
            #if max(x,y)>7 or min(x,y)<0:
            #   break
            if new_board[y][x] == opp:
                temp.append(10*x+y)
            if new_board[y][x]==0 and allow==0:
                allow = 1
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
def evaluate_othello(board, player):
    def piece_count_eval(board, player):
        player_pieces = sum(row.count(player) for row in board)
        opponent_pieces = sum(row.count(-player) for row in board)
        return player_pieces - opponent_pieces

    def mobility_eval(board, player):
        player_legal_moves = len(get_possible_moves(board, player,False))
        opponent_legal_moves = len(get_possible_moves(board, -player,False))
        return player_legal_moves - opponent_legal_moves
    
    # Determine the game stage based on the number of pieces or empty spaces
    total_pieces = sum(row.count(1) + row.count(-1) for row in board)
    

    if total_pieces >= 55:
        # Late game strategy
        score = piece_count_eval(board, player)
    elif total_pieces >= 30:
        # Mid game strategy
        score = piece_count_eval(board, player) + mobility_eval(board, player) #+ evaluate_board(board,player)
    else:
        # Early game strategy
        score = piece_count_eval(board, player) + 2 * mobility_eval(board, player) #+ evaluate_board(board,player)

    return score


def minimax(position, depth, alpha, beta, Player,inMinimax):
    Posible_moves=get_possible_moves(position,Player,inMinimax)
    if depth == 0 or(Posible_moves ==[] and get_possible_moves(position,-Player,False)==[]):
        return evaluate_othello(position,Player) 
    
    
    if Player==-1:
        maxEval = -10**100
        for each in Posible_moves:
            eval = minimax(is_geting_flipped(each-11,position,Player), depth - 1, alpha, beta, -Player, inMinimax)*100+each-11
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval	
    
    else:
        minEval = 10**100
        for each in Posible_moves:
            eval = minimax(is_geting_flipped(each-11,position,Player), depth - 1, alpha, beta, -Player, inMinimax)*100+each-11
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def get_best_move(board,Player,depth):
    best_move=minimax(board, depth, -float('inf'), float('inf'), Player, True)%100
    print(best_move)
    return best_move