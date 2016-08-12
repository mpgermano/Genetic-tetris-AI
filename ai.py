from pykeyboard import PyKeyboard
from tetris.__Main__ import Main
import time
import copy
from random import randint
from threading import Thread


class AI:
	
	def __init__(self):

		self.keyboard = PyKeyboard()
		self.tetris = Main()

	def quit(self):

		self.keyboard.tap_key('q')
		time.sleep(1)
		self.keyboard.tap_key('y')
	
	def pause(self):
		self.keyboard.tap_key('p')
	
	def runAI(self):

		gameThread = Thread(target=self.runTetris)
		gameThread.start()

		
		time.sleep(1)
		self.keyboard.press_key('s')

		#Game loop
		while not self.tetris.g.gameOver:
			
			#Wait while next piece is loading
			while self.tetris.g.currPiece is None:
				time.sleep(0.05)
			time.sleep(0.05)
				
			moveToExecute = self.calculateMove()
			self.executeMove(moveToExecute)
			self.keyboard.tap_key('Down')
		

		time.sleep(0.5)
		self.keyboard.tap_key('n')
		
	def calculateMove(self):

		#First save game state and copy board and piece
		testingGame = copy.deepcopy(self.tetris.g)
		savedGameState = copy.deepcopy(self.tetris.g)

		possibleMoves = self.getAllPrimaryAndSecondaryMoves(testingGame)
		self.tetris.g = savedGameState

		bestMove = self.calculateBestMove(possibleMoves)
		return bestMove

	def getAllPrimaryAndSecondaryMoves(self, game):
		
		primaryMoves = self.getAllPossibleMoves(game)
		subMoveGame = copy.deepcopy(game)
		for move in primaryMoves:

			# Get all possible moves for the next piece, given the previous move
			subMoveGame = copy.deepcopy(game)
			subMoveGame.board = move['board']
			subMoveGame.newPiece()
			subMoves = self.getAllPossibleMoves(subMoveGame)
			move['subMoves'] = subMoves
		
		# Each Primary move contains a list of submoves
		return primaryMoves

	def getAllPossibleMoves(self, game):
		moves = []
			
		#First Position furthest left possible
		#Then drop from every possible column with every possible rotation
		
		firstRotation = True
		startingRotation = game.currPiece.currRotation
		#For every rotation position
		while game.currPiece.currRotation != startingRotation or firstRotation:
			firstShift = True	
			firstRotation = False
			self.positionFurthestLeft(game)
			oldCol = game.currPiece.topLeft.col		

			#For every col
			while game.currPiece.topLeft.col != oldCol or firstShift:
					
				beforeShift = copy.deepcopy(game)
				firstShift= False
				oldCol = game.currPiece.topLeft.col
				self.dropPiece(game, game.board)
				
				landingStats = {}
			
				#Calculate all board combos with the next piece
				landingStats['rotationIndex'] = game.currPiece.currRotation
				landingStats['topLeftCol'] = game.currPiece.topLeft.col
				landingStats['topLeftRow'] = game.currPiece.topLeft.row
				landingStats['board'] = game.board
				
				moves.append(landingStats)
				game = beforeShift
				game.movePiece(1)
				
			game.rotatePiece()
		return moves

	def positionFurthestLeft(self, game):
		
		for x in range(10):
			game.movePiece(-1)

	def dropPiece(self, game, board):
		
		while not game.fallPiece():
			game.fallPiece()
		game.landPiece(False)
		game.updateBoard()

	def calculateBestMove(self, moves):
		scoreToMove = {}
		for move in moves:
			score = self.calculateMoveScore(move)

			maxSubScore = 0
			for subMove in move['subMoves']:
				subScore = self.calculateMoveScore(move)
				if subScore > maxSubScore:
					maxSubScore = subScore

			#add the score and it's best subScore
			score += maxSubScore
			scoreToMove[score] = move

		maxScore = 0
		for score in scoreToMove:
			if score > maxScore:
				maxScore = score

		selectedMove = scoreToMove[maxScore]
		selectedMove.pop('board')
	
		return selectedMove

	def calculateMoveScore(self, move):
		
		# Arbitrary constants
		# Todo: replace these values with those found from genetic algorithm
		linesClearedMultiplier = 1
		agHeightMultiplier = -0.50
		holesMultiplier = -0.30
		bumpinessMultiplier = -0.15
		
		lines = self.calculateLinesMade(move['board'])
		result = self.calculateAggregateHeightAndBumpiness(move['board'])
		agHeight = result[0]
		bumpiness = result[1]
		holes = self.calculateHoles(move['board'])

		score = (lines * linesClearedMultiplier) + (agHeight * agHeightMultiplier) \
		+ (holes * holesMultiplier) + (bumpiness * bumpinessMultiplier) + 1000
		
		if score < 0:
			score = 0

		return score	

	
	def calculateLinesMade(self, board):
		lines = 0
			
		rows = range(len(board))
		columns = range(len(board[0]))
		for r in rows:
			linePresent = True
			for c in columns:
				if board[r][c] == 0:
					
					linePresent = False
					break
			if linePresent:
				lines = lines + 1
		return lines	
		
	def calculateAggregateHeightAndBumpiness(self, board):

		rows = range(len(board))
		columns = range(len(board[0]))
		aggregateHeight = 0
		columnHeight = 0
		bumpiness = 0
		first = True
		
		for c in reversed(columns):
			previousHeight = columnHeight
			reachedEmpty = False
			columnHeight = 23
			for r in reversed(rows):
				if reachedEmpty and board[r][c] != 0:
					reachedEmpty = False
					
				if board[r][c] == 0 and not reachedEmpty:
					reachedEmpty = True
					columnHeight = 23 - (r+1)
			
			if not first:
				bumpyDelta = abs(previousHeight - columnHeight)
				bumpiness = bumpiness + bumpyDelta
				aggregateHeight = aggregateHeight + columnHeight
			
			if first:
				aggregateHeight = aggregateHeight + columnHeight
				first = False
		result = []
		result.append(aggregateHeight)
		result.append(bumpiness)	
		return result
	
	def calculateHoles(self, board):
		rows = range(len(board))
		columns = range(len(board[0]))
		holes = 0

		for r in reversed(rows):
			empty = True

			for c in reversed(columns):
				if board[r][c] != 0:
					empty = False

				elif board[r][c] == 0:
					for searchRow in reversed(range(0,r)):
						if board[searchRow][c] != 0:
							holes = holes + 1
							break
			
			if empty:
				return holes
		
		return holes
		
	def executeMove(self, move):
		
		if self.tetris.g.level == 10:
			sleepTime = 0.1
		else:
			sleepTime = 0.2
	
		if self.tetris.g.currPiece.topLeft.col < move['topLeftCol']:
			direction = 'Right'
		else:
			direction = 'Left'
		
		while self.tetris.g.currPiece.currRotation != move['rotationIndex']:
			if self.tetris.g.gameOver:
				return
				
			self.keyboard.tap_key('Up')
			time.sleep(sleepTime)

		while self.tetris.g.currPiece.topLeft.col != move['topLeftCol']:
			if self.tetris.g.gameOver:
				return
			self.keyboard.tap_key(direction)
			time.sleep(sleepTime)
	
		
		while self.tetris.g.currPiece.topLeft.row < move['topLeftRow'] - 1:
			if self.tetris.g.gameOver:
				return
			self.keyboard.tap_key('Down')
			time.sleep(sleepTime/2)
	
	def runTetris(self):
		try:
			self.tetris.doWelcome()
			self.tetris.gameLoop()
				
		except ZeroDivisionError as e:
    			pass
		except KeyboardInterrupt as e:
    			pass
		except Exception as e:
    			raise e
		finally:
    			self.tetris.doFinish()
