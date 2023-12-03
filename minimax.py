def get_possible_moves(board, lplayer):
    POSSIBLE_MOVES = []

    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                if is_valid_move(board, i, j, lplayer):
                    POSSIBLE_MOVES.append(j*10+i+11)
    POSSIBLE_MOVES.sort()
    return POSSIBLE_MOVES

def is_geting_flipped(pos,board,pplayer):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    output=[pos]
    opp = -pplayer 
    for direction in directions:
        i, j = direction
        y=pos%10
        x=math.floor(pos/10)
        if i == 0 and j == 1:
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
            t = min(7 - x, y)
        temp=[]
        allow=0
        r=0
        for b in range(t):
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
            

            
        if board[y][x] == pplayer:
                output.extend(temp)
                #print(temp)
                temp=[]  
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
    Past_possible_moves=Possible_moves
    Possible_moves=get_possible_moves(position,Player)
    if depth == 0 or (Possible_moves ==0 and Past_possible_moves==0):
        return evaluate_board(position,Player) 
    
    temp=[]
    for move in Possible_moves:
        temp.append(is_geting_flipped(move,position,Player))
    position=temp
    if Player<0:
        maxEval = -10**99999999999
        for each in position:
            eval = minimax(each, depth - 1, alpha, beta, -Player)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval	
    
    else:
        minEval = 10**999999999999
        for each in position:
            eval = minimax(each, depth - 1, alpha, beta, -Player)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval