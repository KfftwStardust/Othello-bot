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


def minimax(position, depth, alpha, beta, Player):
    #if depth == 0 or game over in position
	#	return static evaluation of position
	temp=[]
	for move in get_possible_moves(position,Player):
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