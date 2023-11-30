import math
board=[]
player = 1

for i in range(8):
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
                    possible_moves.append(j*10+i)

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
    output=[]
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
            t = y
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
        temp=[]
        for b in range(t):
            
            if board[x][y] == player:
                output.extend(temp) 
            if board[x][y] == opp:
                temp.append(10*x+y)
            elif board[x][y]==0:
                temp=[]
            r=board[x][y]
            print("t",t,"temp",temp,"output",output,"b", b,"x",x,"y",y,"player",player,"direction",direction,"board",r)
            y += j
            x += i
            
    for k in output:
        print("f")
        board=changeBoard(k,board,player)
    
    return board


 
changeBoard(33,board,1)
changeBoard(44,board,1)
changeBoard(43,board,2)
changeBoard(34,board,2)
printBoard(board)
while True:
    possible_moves = get_possible_moves(board, player)
    print("Possible moves:", possible_moves)
    pos = 99
    while pos==99:
        pos=int(input("Vilken pos 11 till 88 ")) or 99
        if any(pos == p for p in possible_moves)==False:
            pos = 99

    
    board=changeBoard(pos,board,player)
    board=is_geting_flipped(pos,board,player)
    printBoard(board)
    player = (player%2)+1
    