import math
def change_board(pos,board,kplayer):
    temp = board[pos%10]
    temp[math.floor(pos/10)]= kplayer
    board[pos%10] = temp
    return board

def get_possible_moves(sboard, lplayer):
    POSSIBLE_MOVES = []

    for i in range(8):
        for j in range(8):
            if sboard[i][j] == 0:
                if is_valid_move(sboard, i, j, lplayer):
                    POSSIBLE_MOVES.append(j*10+i+11)
    POSSIBLE_MOVES.sort()
    return POSSIBLE_MOVES

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

def is_geting_flipped(pos,board,pplayer):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    output=[pos]
    opp = -pplayer 
    for direction in directions:
        i, j = direction
        y=pos%10
        x=math.floor(pos/10)
        temp=[]
        allow=0
        r=0
        """if i == 0 and j == 1:
            t = 7 - y
        elif i == 1 and j == 0:
            t = 7 - x
        elif i == 0 and j == -1:
            t = y
        elif i == -1 and j == 0:
            t = x
        elif i == 1 and j == 1:
            t = min(7 - x, 7 - y)
        elif i == -1 and j == -1:
            t = min(x, y)
        elif i == -1 and j == 1:
            t = min(x, 7 - y)
        elif i == 1 and j == -1:
            t = min(7 - x, y)"""
        for b in range(8):
            #print("temp",temp,"output",output,"x",x,"y",y,"t",t,"board",r,"b",b,"direction",direction,"pos",pos,"bef")
            y += j
            x += i
            if max(x,y)>7 or min(x,y)<0:
                break
            if board[y][x] == opp:
                temp.append(10*x+y)
            if board[y][x]==0 and allow==0:
                allow = 1
                temp=[]
                break    
            if board[y][x] == pplayer:
                output.extend(temp)
                temp=[]
                break
            r=board[y][x]
            #print("temp",temp,"output",output,"x",x,"y",y,"t",t,"board",r,"b",b,"direction",direction,"pos",pos,"aft")
        #if board[y][x] == pplayer:
                #output.extend(temp)
                ##print(temp)
               # temp=[]  
    for pos in output:
        change_board(pos,board,pplayer)
    return board



def evaluate_board(board, Player):

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
    for i in range(8):
        for j in range(8):
            if board[i][j] == Player:
                score += weights[i][j]
            elif board[i][j] == -Player:
                score -= weights[i][j]

    return score
# Den är nog skit Chatgpt skrev den



def minimax(position, depth, alpha, beta, Player):
    Possible_moves=get_possible_moves(position,Player)
    if depth == 0 :
        return evaluate_board(position,Player) 
    
    temp=[]
    for move in Possible_moves:
        temp.append(is_geting_flipped(move,position,Player))
    position=temp
    if Player==-1:
        maxEval = -10**9
        for each in position:
            eval = minimax(each, depth - 1, alpha, beta, 1)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval	
    
    else:
        minEval = 10**9
        for each in position:
            eval = minimax(each, depth - 1, alpha, beta, -1)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def get_best_move(boar,Possible_moves):
    
    te=[]
    for each in Possible_moves:
        te.append(minimax(is_geting_flipped(each-11,boar,-1),5,-10^9,10^9,-1))
    best_move=Possible_moves[te.index(max(te))]
    return best_move