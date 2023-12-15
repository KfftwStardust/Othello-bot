import math
import timeit
def change_board(pos,jboard,kplayer):
    
    temp = jboard[pos%10]
    temp[math.floor(pos/10)]= kplayer
    jboard[pos%10] = temp
    return jboard

def get_possible_moves(sboard, lplayer):
    POSSIBLE_MOVES = []

    for i in range(8):
        for j in range(8):
            if sboard[i][j] == 0:
                if is_valid_move(sboard, i, j, lplayer):
                    POSSIBLE_MOVES.append(j*10+i+11)
    POSSIBLE_MOVES.sort()
    return POSSIBLE_MOVES

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
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    output=[pos]
    opp = -pplayer 
    new_board = [row[:] for row in iboard]
    for direction in directions:
        i, j = direction
        y=pos%10
        x=math.floor(pos/10)
        temp=[]
        allow=0
        r=0
        for b in range(8):
            #print("temp",temp,"output",output,"x",x,"y",y,"board",r,"b",b,"direction",direction,"pos",pos,"bef")
            y += j
            x += i
            if max(x,y)>7 or min(x,y)<0:
                break
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
        mobilty: titta på hemsidan 'https://www.samsoft.org.uk/reversi/strategy.html', stable disks, frontiers,
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



def minimax(position, depth, alpha, beta, Player):
    Posible_moves=get_possible_moves(position,Player)
    if depth == 0 or(Posible_moves ==[] and get_possible_moves(position,-Player)==[]):
        return evaluate_board(position,Player) 
    
    temp=[]
    for move in Posible_moves:
        temp.append(is_geting_flipped(move-11,position,Player))
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

def get_best_move(board):
    possible_moves = get_possible_moves(board, -1)
    scores = [minimax(is_geting_flipped(int(move) - 11, board, -1), 6, -float('inf'), float('inf'), -1) for move in possible_moves]
    best_move = max(possible_moves, key=lambda move: scores[possible_moves.index(move)])
    return best_move