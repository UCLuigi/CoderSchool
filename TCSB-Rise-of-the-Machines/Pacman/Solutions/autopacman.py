import random
from pacman import Pacman
from searchproblem import *
from search import *

class AutoPacman(Pacman):
	'''
	An AI controlled pacman
	The AI interface has any entity with isAI = True call their AI() method once per loop
	'''
	def __init__(self,i,j,game):
		super(AutoPacman, self).__init__(i,j,game)
		self.isAI = True
		self.directions = []
		self.directionIndex = 0

	def AI(self, game):
		if self.directionIndex >= len(self.directions):
			self.direction=None
		else:
			self.direction = self.directions[self.directionIndex]
			self.directionIndex += 1

class GoWestPacman(AutoPacman):
	'''
	The simplest AI which always goes West
	'''
	def __init__(self,i,j,game):
		super(GoWestPacman, self).__init__(i,j,game)
		self.directions = ["West"]


class RandomPacman(AutoPacman):
	'''
	Another simple AI which chooses its moves randomly
	'''
	def __init__(self,i,j,game):
		super(RandomPacman, self).__init__(i,j,game)

	def AI(self, game):
		self.direction = random.choice(Direction.ALL_DIRECTIONS)

class TinyMazePacman(AutoPacman):
	'''
	Contains the hardcoded solution to the tiny maze
	'''
	def __init__(self, i, j, game):
		super(TinyMazePacman, self).__init__(i,j,game)
		self.directions = [Direction(item) for item in ["South", "South", "South", "South", "West", "West", "South", "West", "West", "South"]]
	

class BFSPacman(AutoPacman):
	'''
	Searches for the optimal path to the target
	'''
	def __init__(self, i, j, game):
		super(BFSPacman, self).__init__(i,j,game)
		path_to_target = search_wrapper(game.problem,breadth_first_search)
		if path_to_target:
			self.directions = path_to_target
		else:
			self.directions = []
	

class DFSPacman(AutoPacman):
	'''
	Searches for the deepest path to the target (usually quick but suboptimal)
	'''
	def __init__(self, i, j, game):
		super(DFSPacman, self).__init__(i,j,game)
		path_to_target = search_wrapper(game.problem,depth_first_search)
		if path_to_target:
			self.directions = path_to_target
		else:
			self.directions = []

class UCSPacman(AutoPacman):
	'''
	Searches for the optimal path to the target
	'''
	def __init__(self, i, j, game):
		super(UCSPacman, self).__init__(i,j,game)
		path_to_target = search_wrapper(game.problem, ucs)
		if path_to_target:
			self.directions = path_to_target
		else:
			self.directions = []
	

class AStarPacman(AutoPacman):
	'''
	Searches for the optimal path to the target (quicker than BFS or UCS with a good heuristic)
	'''
	def __init__(self, i, j, game, heuristic=null_heuristic):
		super(AStarPacman, self).__init__(i,j,game)
		startnode = Node((1,1),[])
		path_to_target = search_wrapper(game.problem, Astar, heuristic)
		if path_to_target:
			self.directions = path_to_target
		else:
			self.directions = []

class GreedyPacman(AutoPacman):
	'''
	Greedily follows the heuristic
	'''
	def __init__(self, i, j, game, heuristic=null_heuristic):
		super(GreedyPacman, self).__init__(i,j,game)
		path_to_target = search_wrapper(game.problem, greedySearch, heuristic)
		if path_to_target:
			self.directions = path_to_target
		else:
			self.directions = []

class ClosestDotPacman(AutoPacman):
	'''
	Always moves to the closest dot
	'''
	def __init__(self, i, j, game, heuristic=null_heuristic):
		super(ClosestDotPacman, self).__init__(i,j,game)
		

	def AI(self, game):
		problem = NearestFoodProblem((self.i,self.j), game.board)
		path_to_target = search_wrapper(problem, breadth_first_search, debug=False)
		if path_to_target:
			self.direction = path_to_target[0]

