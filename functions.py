import math
import random
def change_board(pos,jboard,kplayer):
    # changes one position to the current players colour
    jboard[pos%10][math.floor(pos/10)]=kplayer
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
        # Workaround for a pecial case in the minimax algoritm
        return iboard
    # Decide the starting positions in the array
    y=pos%10
    x=math.floor(pos/10)
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
            if max(x,y)>7 or min(x,y)<0:
                # stops it from itarion outside of the board, and generating error messages
                break
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

def evaluate_board(lboard, Player):

    score = 0

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

    
    """ Olika strategier, minsta antalet disks i early game, få motståndaren att ha få drag.
        mobilty: titta på hemsidan 'https://www.samsoft.org.uk/reversi/strategy.htm', stable disks, frontiers,
        parity
        """
    # Calculate the score based on the player's pieces and the weights
    for i in range(8):
        for j in range(8):
            if lboard[i][j] == 1:
                score += weights[i][j]
            elif lboard[i][j] == -1:
                score -= weights[i][j]
    score = score*Player 
    return score 
# Den är nog skit Chatgpt skrev den

def evaluate_othello(board, player, constants):
    # The main eval funtion that adds up the eval from the children functions below.
    
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
def piece_count_eval(board, player):
    # evaluates according to piece count
    player_pieces = sum(row.count(player) for row in board)
    opponent_pieces = sum(row.count(-player) for row in board)
    return player_pieces - opponent_pieces

def mobility_eval(board, player):
    # evalutaes according ot mobilty. aka how many possible moves are available
    player_legal_moves = len(get_possible_moves(board, player,False))
    opponent_legal_moves = len(get_possible_moves(board, -player,False))
    return player_legal_moves - opponent_legal_moves

def minimax(position, depth, alpha, beta, Player,constants):
    
    Posible_moves=get_possible_moves(position,Player)
    if depth == 0 or(Posible_moves ==[] and get_possible_moves(position,-Player)==[]):
        return evaluate_othello(position,Player,constants) 
    
    if Player==-1:
        maxEval = -10**100
        for each in Posible_moves:
            eval = minimax(is_getting_flipped(each,position,Player), depth - 1, alpha, beta, -Player,constants)*100+each
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval	
    
    else:
        minEval = 10**100
        for each in Posible_moves:
            eval = minimax(is_getting_flipped(each,position,Player), depth - 1, alpha, beta, -Player,constants)*100+each
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def get_best_move(board,Player,depth,constants):
    #Finds the best move according to the current version of the minimax algoritm. It's a separate function because we had a plan to add an opening book aswell.
    best_move=minimax(board, depth, -float('inf'), float('inf'), Player, True, constants)%100
    #print(best_move+11)
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

def who_wins(board,player):
    # decides who wins the game
    score=piece_count_eval(board,player)
    if score == 0:
        return "Player 0 " #"The game ended in a Draw"
    else:
        return "Player 1 wins" if score > 0 else "Player 2 wins"

def constants_change(constant,board):
    # Changes the constants used in the eval function, is only used when the bot is training. It's supposed to find some good ish values for the eval funtion
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