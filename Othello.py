import math
board=[]
PLAYER = 1

for q in range(8):
    x=[]
    for o in range(8):
        x.append(int(0))
    board.append(x)

def print_board(oard):
    for p in oard:
        print(p)
    return

def change_board(pos,board,kplayer):
    temp = board[pos%10]
    temp[math.floor(pos/10)]= kplayer
    board[pos%10] = temp
    return board

def get_possible_moves(sboard, lplayer):
    POSSIBLE_MOVES = []

    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
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
    opponent = 3 - cplayer
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
    opp=2 if pplayer ==1 else 1
    for direction in directions:
        i, j = direction
        y=pos%10
        x=math.floor(pos/10)
        if i == 0 and j == 1:
            t = 8 - y
        elif i == 1 and j == 0:
            t = 8 - x
        elif i == 0 and j == -1:
            t = y
            y += j
            x += i
        elif i == -1 and j == 0:
            t = x
        elif i == 1 and j == 1:
            t = min(8 - x, 8 - y)
        elif i == -1 and j == -1:
            t = min(x, y)
        elif i == -1 and j == 1:
            t = min(x, 8 - y)
        elif i == 1 and j == -1:
            t = min(8 - x, y)
            y += j
            x += i
        temp=[]
        for b in range(t):
            
            if board[y][x] == opp:
                temp.append(10*x+y)
            if board[y][x]==0:
                temp=[]
            if board[y][x] == pplayer:
                output.extend(temp)
                temp=[]
                
            #r=board[y][x]
            #print("temp",temp,"output",output,"x",x,"y",y,"t",t,"board",r,"b",b,"direction",direction,"pos",pos)
            y += j
            x += i
    for pos in output:
        board=change_board(pos,board,pplayer)
    return board

def who_wins(board):
    p1_score=0
    p2_score=0
    for u in range(8):
        for r in range(8):
            if board[u][r]==1:
                p1_score +=1
            if board[u][r]==2:
                p2_score +=1
    winner=max(p1_score,p2_score)
    return winner


change_board(33,board,1)
change_board(44,board,1)
change_board(43,board,2)
change_board(34,board,2)
print_board(board)
POSSIBLE_MOVES=0
while True:
    PAST_POSSIBLE_MOVES=POSSIBLE_MOVES
    POSSIBLE_MOVES = get_possible_moves(board, PLAYER)
    if not PAST_POSSIBLE_MOVES and not POSSIBLE_MOVES:
        print("Player",who_wins(board),"wins")
    print("Possible moves:", POSSIBLE_MOVES)
    print("Player",PLAYER,"turn")
    if POSSIBLE_MOVES!=[]:
        POS = 99
        while POS==99:
            POS=str(input("Vilken pos 11 till 88 ")) or 99
            if any(int(POS) == p for p in POSSIBLE_MOVES) == False:
                POS = 99
        board=is_geting_flipped(int(POS)-11,board,PLAYER)
    print_board(board)
    PLAYER = 3 - PLAYER
     