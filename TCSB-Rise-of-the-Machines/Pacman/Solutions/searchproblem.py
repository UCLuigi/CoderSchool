from util import *
import sys
import time
class SearchProblem:
	'''
	A wrapper class for defining a generic search problem
	Includes start state, goal test, and successor functions
	'''

	# kwargs indicates that each type of problem will need to be initialized with different keyword arguments
	def __init__(self, **kwargs):
		self.expanded = 0
		self.expandedstates = []
		self.visualizeexpandedstates = False
		self.starttime = time.time()

	def getStartState(self):
		raise NotImplementedError()
	
	def getStartPos(self):
		return self.getPos(self.getStartState())

	def getPos(self, state):
		raise NotImplementedError()

	def getBoard(self):
		raise NotImplementedError()

	def isGoalState(self, state):
		raise NotImplementedError()

	def getSuccessors(self, state):
		self.expanded += 1
		self.expandedstates.append(state)

	def hasWon(self, game):
		raise NotImplementedError()

class BoardSearchProblem(SearchProblem):
	'''
	Any problem involving moving from point A to point B on the board
	State = (i,j) coordinate pair
	Goal = (i,j) coordinate pair
	Child = ((i,j), action, cost) triple
	'''

	def __init__(self, start, goal, board, passable_blocks):
		super(BoardSearchProblem, self).__init__()
		self.start = start
		self.goal = goal
		self.board = board
		self.passable_blocks = passable_blocks

	def getStartState(self):
		return self.start

	def getPos(self, state):
		return state
	
	def getBoard(self):
		return self.board

	def isGoalState(self, state):
		return state == self.goal

	def getSuccessors(self, state):
		super(BoardSearchProblem, self).getSuccessors(state)
		i,j = state
		children = []
		for direction in Direction.ALL_DIRECTIONS:
			newi,newj = direction.apply((i,j))
			if self.board[newi][newj] in self.passable_blocks:
				children.append(((newi,newj),direction,1))
		return children

	def hasWon(self, game):
		state = (game.player.i, game.player.j)
		return self.isGoalState(state)

class NearestFoodProblem(SearchProblem):
	'''
	A helper class for problems about finding the nearest food
	State = (i,j) coordinate pair
	Goal = N/A
	Child = (state, action, cost) triple
	'''

	def __init__(self, start, board):
		super(NearestFoodProblem, self).__init__()
		self.start = start
		self.board = board
		self.passable_blocks = ["spot"]

	def getStartState(self):
		return self.start
	
	def getPos(self, state):
		return state

	def getBoard(self):
		return self.board

	def isGoalState(self, state):
		i,j = state
		return self.board.foodgrid[i][j]

	def getSuccessors(self, state):
		super(NearestFoodProblem, self).getSuccessors(state)
		i,j = state
		children = []
		for direction in Direction.ALL_DIRECTIONS:
			newi,newj = direction.apply((i,j))
			if self.board[newi][newj] in self.passable_blocks:
				children.append(((newi,newj),direction,1))
		return children

	def hasWon(self, game):
		state = (game.player.i, game.player.j)
		return self.isGoalState(state)


class EatAllFoodProblem(SearchProblem):
	'''
	A problem where Pacman must eat all the food pellets on the board
	State = (i,j) coordinate pair, current board
	Goal = N/A
	Child = (state, action, cost) triple
	'''

	def __init__(self, start, board):
		super(EatAllFoodProblem, self).__init__()
		self.start = start
		self.board = board
		self.passable_blocks = ["spot"]

	def getStartState(self):
		return self.start
	
	def getPos(self, state):
		return state[0]

	def getBoard(self):
		return self.board

	def isGoalState(self, state):
		return state[1].isEmpty()

	def getSuccessors(self, state):
		super(EatAllFoodProblem, self).getSuccessors(state)
		i,j = state[0]
		children = []
		for direction in Direction.ALL_DIRECTIONS:
			newi,newj = direction.apply((i,j))
			if self.board[newi][newj] in self.passable_blocks:
				newboard = state[1].copy()
				newboard.foodgrid[newi][newj] = False
				children.append((((newi,newj),newboard),direction,1))
		return children

	def hasWon(self, game):
		return game.board.isEmpty()

class CornersProblem(EatAllFoodProblem):
	'''
	A problem where Pacman must eat all the food pellets on the board
	State = (i,j) coordinate pair, boolean list of 4 corners visited [TopLeft, TopRight, BottomLeft, BottomRight]
	Goal = N/A
	Child = (state, action, cost) triple
	'''

	def __init__(self, start, board):
		super(EatAllFoodProblem, self).__init__()
		self.start = start
		self.board = board
		self.passable_blocks = ["spot"]
		self.corners = [(1,1), (1,board.width-2), (board.height-2,1), (board.height-2,board.width-2)]

	def getStartState(self):
		return self.start
	
	def getPos(self, state):
		return state[0]

	def getBoard(self):
		return self.board

	def isGoalState(self, state):
		return sum(state[1]) == 4

	def getSuccessors(self, state):
		super(EatAllFoodProblem, self).getSuccessors(state)
		i,j = state[0]
		children = []
		oldcorners = state[1]
		for direction in Direction.ALL_DIRECTIONS:
			newi,newj = direction.apply((i,j))
			if self.board[newi][newj] in self.passable_blocks:
				newcorners = list(oldcorners)
				if (newi,newj) in self.corners:
					newcorners[self.corners.index((newi,newj))] = True
				children.append((((newi,newj),tuple(newcorners)),direction,1))
		return children

	def hasWon(self, game):
		return game.board.isEmpty()