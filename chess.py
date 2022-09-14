import chess

pawnTable = [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, -25, -25, 10, 10, 5, 5, -5, -10, 0, 0, -10, -5, 5, 0, 0, 0, 25, 25, 0, 0, 0, 5, 5, 10, 27, 27, 10, 5, 5, 10, 10, 20, 30, 30, 20, 10, 10, 50, 50, 50, 50, 50, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, ]

knightTable = [-50, -40, -30, -30, -30, -30, -40, -50,
		-40, -20, 0, 0, 0, 0, -20, -40,
		-30, 0, 10, 15, 15, 10, 0, -30,
		-30, 5, 15, 20, 20, 15, 5, -30,
		-30, 0, 15, 20, 20, 15, 0, -30,
		-30, 5, 10, 15, 15, 10, 5, -30,
		-40, -20, 0, 5, 5, 0, -20, -40,
		-50, -40, -20, -30, -30, -20, -40, -50, ]
knightTable.reverse()
bishopTable = [-20, -10, -10, -10, -10, -10, -10, -20,
		-10, 0, 0, 0, 0, 0, 0, -10,
		-10, 0, 5, 10, 10, 5, 0, -10,
		-10, 5, 5, 10, 10, 5, 5, -10,
		-10, 0, 10, 10, 10, 10, 0, -10,
		-10, 10, 10, 10, 10, 10, 10, -10,
		-10, 5, 0, 0, 0, 0, 5, -10,
		-20, -10, -40, -10, -10, -40, -10, -20, ]
bishopTable.reverse()
kingTable = [-30, -40, -40, -50, -50, -40, -40, -30,
	-30, -40, -40, -50, -50, -40, -40, -30,
	-30, -40, -40, -50, -50, -40, -40, -30,
	-30, -40, -40, -50, -50, -40, -40, -30,
	-20, -30, -30, -40, -40, -30, -30, -20,
	-10, -20, -20, -20, -20, -20, -20, -10,
	 20, 20, 0, 0, 0, 0, 20, 20,
	 20, 30, 10, 0, 0, 10, 30, 20]
kingTable.reverse()


def material(board, color):
	material = 0
	for piece in board.pieces(1, color):
		material += 10
	for piece in board.pieces(2, color):
		material += 30
	for piece in board.pieces(3, color):
		material += 30
	for piece in board.pieces(4, color):
		material += 50
	for piece in board.pieces(5, color):
		material += 90
	for piece in board.pieces(6, color):
		material += 9999
	return material


def evalPos(board, color):
	if board.is_checkmate():
		return 999999
	if color == True:
		color2 = False
	else:
		color2 = True
	score = material(board, color)
	score -= material(board, color2)
	for i in range(0, 63):
		p = board.piece_at(i)
		if p == None:
			score += 0
		else:
			if p.color == color:
				if(p.piece_type == 1):
					score += pawnTable[i] * .1
				if(p.piece_type == 2):
					score += knightTable[i] * .1
				if(p.piece_type == 3):
					score += bishopTable[i] * .1
				if(p.piece_type == 6):
					score += kingTable[i] * .1
	return score

def minimaxRoot(depth, board, isMax):
	bestVal = -9999
	bestMove = None
	for move in board.legal_moves:
		board.push(move)
		if board.is_checkmate():
			board.pop()
			return move
		value = minimax(depth - 1, board, -10000, 10000, not isMax)
		board.pop()
		if value >= bestVal:
			bestMove = move
			bestVal = value
	return bestMove


def minimax(depth, board, alpha, beta, isMax):
	if depth == 0:
		return evalPos(board, not isMax)
	if isMax:
		bestMove = -9999
		for move in board.legal_moves:
			board.push(move)
			bestMove = max(bestMove, minimax(depth - 1, board, alpha, beta, not isMax))
			board.pop()
			alpha = max(alpha, bestMove)
			if beta <= alpha:
				return bestMove
		return bestMove
	else:
		bestMove = 9999
		for move in board.legal_moves:
			board.push(move)
			bestMove = min(bestMove, minimax(depth - 1, board, alpha, beta, not isMax))
			board.pop()
			beta = min(beta, bestMove)
			if beta <= alpha:
				return bestMove
		return bestMove

fen = input("Input FEN (enter for default board)")
if fen == "":
	mboard = chess.Board()
else:
	mboard = chess.Board(fen)

print(mboard)
while(1):
	pos1 = input("move from: ")
	pos2 = input("move to: ")
	move = chess.Move.from_uci(pos1 + pos2)
	for m in mboard.legal_moves:
		if move == m:
			mboard.push(move)
	print("")
	print(mboard)
	if mboard.is_checkmate():
		print("White wins")
	mboard.push(minimaxRoot(4, mboard, True))
	print("")
	print(mboard)
	if mboard.is_checkmate():
		print("Black wins")
