import math
board=[]
currentplayer = 1
for i in range(8):
    x=[]
    for o in range(8):
        x.append(int(0))
    board.append(x)

def printBoard(board):
    for p in board:
        print(p)
    return 

def changeBoard(pos,board,currentplayer):
    pos1 = pos%10
    pos2 = math.floor(pos/10)
    temp = board[pos1]
    temp[pos2]= currentplayer
    board[pos1] = temp
    return board

def get_possible_moves(board, currentplayer):
    possible_moves = []

    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                if is_valid_move(board, i, j, currentplayer):
                    possible_moves.append((i, j))

    return possible_moves

def is_valid_move(board, row, col, currentplayer):
    if board[row][col] != 0:
        return False

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

    for direction in directions:
        if is_valid_direction(board, row, col, direction, currentplayer):
            return True

    return False

def is_valid_direction(board, row, col, direction, currentplayer):
    opponent = 3 - currentplayer
    i, j = direction

    x, y = row + i, col + j
    if not (0 <= x < 8 and 0 <= y < 8) or board[x][y] != opponent:
        return False

    x += i
    y += j

    while 0 <= x < 8 and 0 <= y < 8:
        if board[x][y] == currentplayer:
            return True
        elif board[x][y] == 0:
            return False

        x += i
        y += j

    return False

changeBoard(33,board,1)
changeBoard(44,board,1)
changeBoard(43,board,2)
changeBoard(34,board,2)
printBoard(board)
while True:
    possible_moves = get_possible_moves(board, currentplayer)
    print("Possible moves:", possible_moves)
    pos=int(input("Vilken pos 11 till 88 "))-11
    while pos%10 >7 or pos > 77:
        pos=int(input("Vilken pos 11 till 88 "))-11
    
    
    board=changeBoard(pos,board,currentplayer)
    currentplayer = (currentplayer%2)+1
    printBoard(board)