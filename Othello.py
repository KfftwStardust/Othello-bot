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

changeBoard(33,board,1)
changeBoard(44,board,1)
changeBoard(43,board,2)
changeBoard(34,board,2)
printBoard(board)
while True:
    pos=int(input("Vilken pos 11 till 88 "))-11
    while pos%10 >7 or pos > 77:
        pos=int(input("Vilken pos 11 till 88 "))-11
    
    
    board=changeBoard(pos,board,currentplayer)
    currentplayer = (currentplayer%2)+1
    printBoard(board)
