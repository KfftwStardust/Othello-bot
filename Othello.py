import math
board=[]
player = 1

for q in range(8):
    x=[]
    for o in range(8):
        x.append(int(0))
    board.append(x)

def printBoard(board):
    for p in board:
        print(p)
    return

def changeBoard(pos,board,player):
    temp = board[pos%10]
    temp[math.floor(pos/10)]= player
    board[pos%10] = temp
    return board

def get_possible_moves(board, player):
    possible_moves = []

    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                if is_valid_move(board, i, j, player):
                    possible_moves.append(j*10+i+11)

    return possible_moves

def is_valid_move(board, row, col, player):
    if board[row][col] != 0:
        return False

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

    for direction in directions:
        if is_valid_direction(board, row, col, direction, player):
            return True

    return False

def is_valid_direction(board, row, col, direction, player):
    opponent = 3 - player
    i, j = direction

    x, y = row + i, col + j
    if not (0 <= x < 8 and 0 <= y < 8) or board[x][y] != opponent:
        return False

    x += i
    y += j

    while 0 <= x < 8 and 0 <= y < 8:
        if board[x][y] == player:
            return True
        elif board[x][y] == 0:
            return False

        x += i
        y += j

    return False

def is_geting_flipped(pos,board,player):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    output=[pos]
    opp=2 if player ==1 else 1
    for direction in directions:
        i, j = direction
        y=pos%10
        x=math.floor(pos/10)
        if i == 0 and j == 1:
            t = 8 - y
        elif i == 1 and j == 0:
            t = 8 - x
        elif i == 0 and j == -1:
            t = y+1
        elif i == -1 and j == 0:
            t = x
        elif i == 1 and j == 1:
            t = min(8 - x, 8 - y)
        elif i == -1 and j == -1:
            t = min(x, y)
        elif i == -1 and j == 1:
            t = min(x, 8 - y)
        elif i == 1 and j == -1:
            t = min(8 - x, y)+1
        temp=[]
        for b in range(t):
            if board[y][x] == player:
                output.extend(temp)
            elif board[y][x] == opp:
                temp.append(10*x+y)
            elif board[y][x]==0:
                temp=[]
                
            r=board[y][x]
            print("temp",temp,"output",output,"x",x,"y",y,"t",t,"board",r,"b",b,"direction",direction,"pos",pos)
            y += j
            x += i
    for k in output:
        board=changeBoard(k,board,player)
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


changeBoard(33,board,1)
changeBoard(44,board,1)
changeBoard(43,board,2)
changeBoard(34,board,2)
printBoard(board)
possible_moves=0
while True:
    past_possible_moves=possible_moves
    possible_moves = get_possible_moves(board, player)
    if past_possible_moves == [] and possible_moves ==[]:
        print("Player",who_wins(board),"wins")
    print("Possible moves:", possible_moves)
    print("Player",player,"turn")
    if possible_moves !=[]:
        pos = 99
        while pos==99:
            pos=str(input("Vilken pos 11 till 88 ")) or 99 
            if any(int(pos) == p for p in possible_moves) is False:
                pos = 99
        board=is_geting_flipped(int(pos)-11,board,player)
        printBoard(board)
    player = 3 - player
    