from util import *
from searchproblem import *
import time

"""
Helper classes to create Nodes that have a State as well as additional Info as you define the problems
"""
class Node:
	def __init__(self, state, info):
		self.state = state
		self.info = info

	def __getitem__(self, item):
		if item == 0 or item == "state":
			return self.state
		if item == 1 or item == "info":
			return self.info
		else:
			raise KeyError("Invalid key. Key can choose from (0,1), (state,info), or more specific keys for types of nodes")

"""
BoardSearchNodes in particular should have a path as their info, so a Node has (state, path)
"""
class BoardSearchNode(Node):
	def __getitem__(self, item):
		if item == "state":
			return self.state
		if item == "path":
			return self.path
		else:
			return super(BoardSearchNode,Node).__getitem__(item)

"""
The function that calls the specific search algorithms.
Do not modify, this simply tracks the number of nodes and time taken to run a search
"""
def search_wrapper(problem, search_fx, heuristic=None, debug=True):
	if heuristic:
		answer = search_fx(problem, heuristic)
	else:
		answer = search_fx(problem)
	if debug:
		print("Expanded " + str(problem.expanded) + " nodes in " + str(int(time.time() - problem.starttime)) + " seconds before terminating.")
		if answer:
			print("Total path length of solution: " + str(len(answer)))
		problem.visualizeexpandedstates = True
	return answer

"""
An optional way to structure the search algorithms since most of the pseudocode is the same for every algorithm
"""
def general_search(problem, fringe):
	fringe.push(Node(problem.getStartState(), []))
	closed = set()
	i = 0
	while True:
		if fringe.isEmpty():
			return None
		node = fringe.pop()
		if problem.isGoalState(node["state"]):
			return node["info"]
		if node["state"] not in closed:
			i+=1
			closed.add(node["state"])
			children = problem.getSuccessors(node["state"])
			for child,action,cost in children:
				fringe.push(Node(child,node["info"] + [action]))

"""
Search a graph by exploring the deepest nodes first
"""
def depth_first_search(problem):
	fringe = Stack()
	return general_search(problem, fringe)

"""
Search a graph by exploring the shallowest nodes first
"""
def breadth_first_search(problem):
	fringe = Queue()
	return general_search(problem, fringe)

"""
Search a graph by exploring the nodes with lowest cost first
"""
def ucs(problem):
	fringe = PriorityQueue(lambda node: len(node["info"]))
	return general_search(problem, fringe)

"""
Search a graph by exploring the nodes with lowest cost + estimated cost to goal first
"""
def Astar(problem, heuristic):
	fringe = PriorityQueue(lambda node: len(node["info"]) + heuristic(node, problem))
	return general_search(problem, fringe)

"""
Search a graph by exploring the nodes with lowest estimated cost to goal first
"""
def greedySearch(problem, heuristic):
	fringe = PriorityQueue(lambda node: heuristic(node, problem))
	return general_search(problem, fringe)

"""
The default heuristic which estimates the distance to goal from every node as 0
"""
def null_heuristic(node, problem):
	return 0

"""
A simple heuristic which uses the manhattan distance to the goal
"""
def manhattan_heuristic(node, problem):
	if isinstance(problem, BoardSearchProblem):
		return manhattan_distance(node["state"], problem.goal[0])
	else:
		return 0

"""
Estimates the cost as the manhattan distance to the nearest corner
"""
def manhattancorner_heuristic(node, problem):
	if isinstance(problem, CornersProblem):
		return min([manhattan_distance(problem.getPos(node["state"]), problem.corners[i]) for i in range(4)])
	else:
		return 0

"""
Estimates the cost as the manhattan distance to the nearest food
"""
def manhattanfood_heuristic(node, problem):
	if isinstance(problem, EatAllFoodProblem):
		problem = NearestFoodProblem(problem.getPos(node["state"]),problem.board)
		food_dists=[manhattan_distance(problem.getStartPos(), (i,j)) for i in range(problem.board.height) for j in range(problem.board.width) if problem.board.foodgrid[i][j]]
		return min(food_dists)
	return 0

"""
Runs BFS to solve the problem and uses the exact solution as the heuristic
Do not actually use this heuristic as it's incredibly slow (you're solving the problem to estimate how to solve the problem).
The point of this is to demonstrate the power of a good heuristic.
"""
def bfs_heuristic(node, problem):
	if isinstance(problem, BoardSearchProblem):
		problem = BoardSearchProblem(node["state"], problem.goal, problem.board, problem.passable_blocks)
		answer = breadth_first_search(problem)
		if answer:
			return len(answer)
	return 0

"""
Runs BFS to the nearest food. Unlike bfs_heuristic this one is usable since you're solving a smaller, simpler problem
"""
def bfsfood_heuristic(node, problem):
	if isinstance(problem, EatAllFoodProblem):
		problem = NearestFoodProblem(problem.getPos(node["state"]), problem.board)
		return len(breadth_first_search(problem))
	else:
		return 0

"""
Estimates the distance to solve the CornersProblem
"""
def corners_heuristic(node, problem):
    corners = problem.corners # These are the corner coordinates
    state = node["state"]
    if problem.isGoalState(state):
        return 0
    visited = state[1]
    cornersToVisit = []

    for i in range(0, 4):
        if not visited[i]:
            cornersToVisit.append(corners[i])
    est = 0
    position = problem.getPos(state)
    while (len(cornersToVisit) > 0):
        cornerDistances = []
        for corner in cornersToVisit:
            cornerDistances.append(manhattan_distance(position, corner))
        mindist = min(cornerDistances)
        mindex = cornerDistances.index(mindist)
        est += mindist
        position = cornersToVisit.pop(mindex)
    return est

"""
Estimates the cost of solving the EatAllFoodProblem
"""
def food_heuristic(node, problem):
	state = node["state"]
	if problem.isGoalState(state):
		return 0

	estimate = 0

	nfp = NearestFoodProblem(problem.getPos(node["state"]), problem.board)
	nfp_path = breadth_first_search(nfp)
	nearestfooddist = len(nfp_path)
	estimate += nearestfooddist

	nfi,nfj = problem.getPos(state)
	for i in range(len(nfp_path)):
		nfi,nfj = nfp_path[i].apply((nfi,nfj))
	secondboard = problem.board.copy()
	secondboard.foodgrid[nfi][nfj] = False
	numfood = sum([sum(row) for row in secondboard.foodgrid])
	if numfood > 0:
		nfp2 = NearestFoodProblem((nfi,nfj), secondboard)
		estimate += len(breadth_first_search(nfp2)) - 1
	return estimate + numfood