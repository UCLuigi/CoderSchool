from util import Board
from searchproblem import *
from search import *

def maze_generator(pattern):
	def other(spot):
		if spot == "spot":
			return "wall"
		return "spot"

	grid = []
	for row in pattern:
		grid.append([])
		current = row[0]
		for i in range(1,len(row)):
			grid[-1]+=[current]*row[i]
			current = other(current)
		if len(grid[-1]) != len(grid[0]):
			print("Pattern was set with len " + str(len(grid[0])) + ". Generated row " + str(len(grid)) + " with length " + str(len(grid[-1])))
	return grid

tinymazepattern = [
					["wall", 7],
					["wall", 1, 5, 1],
					["wall", 1, 1, 3, 1, 1],
					["wall", 1, 5, 1],
					["wall", 5, 1, 1],
					["wall", 3, 3, 1],
					["wall", 1, 3, 3],
					["wall", 1, 1, 5],
					["wall", 7]
					]


tinymazegrid = maze_generator(tinymazepattern)
tinymaze = Board(maze=tinymazegrid, house=False)
tinymazeproblem = BoardSearchProblem((1,5), (7,1), tinymaze, ["spot"])


tinycornerspattern = [
					["wall",7],
					["wall",1,5,1],
					["wall",1,1,1,1,1,1,1],
					["wall",1,5,1],
					["wall",1,1,1,1,1,1,1],
					["wall",1,5,1],
					["wall",7],
					]
tinycornersgrid = maze_generator(tinycornerspattern)
tinycorners = Board(maze=tinycornersgrid, house=False)
tinycorners.fillcorners()
tinycornerstart = ((3,3),(False, False, False, False))
tinycornersproblem = CornersProblem(tinycornerstart,tinycorners)

mediumcornerspattern = [
						["wall", 31],
						["wall", 1,7,1,1,1,1,1,15,1,1,1],
						["wall", 1,7,1,1,1,1,7,1,7,1,1,1,1],
						["wall", 1,7,1,9,1,5,1,1,1,3,1],
						["wall", 5,1,5,1,3,1,3,1,5,1,1,1,3],
						["wall", 1,3,1,1,1,1,1,1,1,3,1,5,1,5,1,3,1],
						["wall", 1,1,3,1,1,1,1,1,1,1,9,1,3,1,3,1,1],
						["wall", 1,7,1,5,3,5,1,1,1,1,1,3,1],
						["wall", 3,1,1,1,7,1,5,1,3,1,1,1,1,1,1,1,1],
						["wall", 1,1,1,11,3,5,1,5,1,1,1],
						["wall", 1,1,1,1,5,1,1,1,5,1,1,1,3,1,3,1,1,1,1],
						["wall", 1,3,1,5,1,7,1,1,1,3,1,1,3,1,1],
						["wall", 1,3,1,1,5,7,1,1,3,1,1,1,3,1,1],
						["wall", 1,3,1,1,5,7,1,1,3,1,1,5,1],
						["wall", 31],
						]
mediumcornersgrid = maze_generator(mediumcornerspattern)
mediumcorners = Board(maze=mediumcornersgrid, house=False)
mediumcorners.fillcorners()
mediumcornerstart = ((1,2), (False, False, False, False))
mediumcornersproblem = CornersProblem(mediumcornerstart, mediumcorners)

tinyfoodpattern = [
					["wall", 9],
					["wall", 1,7,1],
					["wall", 4,1,2,1,1],
					["wall", 1,7,1],
					["wall", 1,1,2,1,2,1,1],
					["wall", 1,1,1,5,1],
					["wall", 9]
					]
tinyfoodgrid = maze_generator(tinyfoodpattern)
tinyfood = Board(maze=tinyfoodgrid, house=False)
for i,j in [(4,1),(5,1),(5,3)]:
	tinyfood.foodgrid[i][j] = True
tinyfoodproblem = EatAllFoodProblem(((3,4),tinyfood),tinyfood)

trickyfood = Board(maze=tinyfoodgrid, house=False)
# for i,j in [(4,1),(5,1),(5,3),(1,6),(1,7),(4,7),(5,7)]:
for i,j in [(4,1),(5,1),(5,3),(4,7),(5,7)]:
	trickyfood.foodgrid[i][j] = True
trickyfoodproblem = EatAllFoodProblem(((3,4),trickyfood),trickyfood)

heuristictestpattern = [
						["wall", 10],
						["wall", 1,8,1],
						["wall", 10],
						]
heuristictestgrid = maze_generator(heuristictestpattern)
heuristictest = Board(maze=heuristictestgrid, house=False)
heuristictestproblem = BoardSearchProblem((1,4), (1,8), heuristictest, ["spot"])

smallmazepattern = [
					["wall", 13],
					["wall", 1,5,1,5,1],
					["wall", 1,1,3,1,1,1,3,1,1],
					["wall", 1,11,1],
					["wall", 1,1,9,1,1],
					["wall", 1,11,1],
					["wall", 13],
					]
smallmazegrid = maze_generator(smallmazepattern)
smallmaze = Board(maze=smallmazegrid, house=False, filled=True)
smallmaze.foodgrid[5][1] = False
smallmazeproblem = EatAllFoodProblem(((5,1), smallmaze), smallmaze)



regularmazepattern = [
                      ["wall", 20],
                      ["wall", 2, 7, 2, 7, 2],
                      ["wall", 2,1,1,1,3,1,2,1,3,1,1,1,2],
                      ["wall", 2, 16, 2],
                      ["wall", 2,1,1,1,1,1,6,1,1,1,1,1,2],
                      ["wall", 2,3,1,3,2,3,1,3,2],
                      ["wall", 4,1,3,1,2,1,3,1,4],
                      ["wall", 4,1,1,8,1,1,4],
                      #["wall", 4,1,1,1,2,2,2,1,1,1,4],
                      ["wall", 4,3,1,4,1,3,4],
                      #["wall", 4,1,1,1,6,1,1,1,4],
                      ["wall", 4,1,1,8,1,1,4],
                      ["wall", 4,1,1,1,6,1,1,1,4],
                      ["wall", 1,8,2,8,1],
                      ["wall", 1,1,2,1,3,1,2,1,3,1,2,1,1],
                      ["wall", 1,2,1,12,1,2,1],
                      ["wall", 2,1,1,1,1,1,6,1,1,1,1,1,2],
                      ["wall", 1,4,1,3,2,3,1,4,1],
                      ["wall", 1,1,6,1,2,1,6,1,1],
                      ["wall", 1,18,1],
                      ["wall", 20]
                     ]

regularmazegrid = maze_generator(regularmazepattern)
regularmaze = Board(maze=regularmazegrid, filled=True, house=True)
regularmazeproblem = EatAllFoodProblem(((13,9), regularmaze), regularmaze)



hugemazepattern = [
			["wall", 19, 1, 21],
			["wall", 1, 23, 1, 7, 1, 3, 1, 3, 1],
			["wall", 1,1,10,1,10,1,1,1,5,1,3,1,1,1,3],
			["wall", 1,1,1,7,1,5,1,5,1,3,1,3,1,5,1,3,1],
			["wall", 1,1,1,1,5,1,3,1,3,1,3,1,3,1,1,1,1,1,9,1,1],
			["wall", 1,1,1,5,1,5,1,3,1,1,1,5,1,1,1,9,1,1,1],
			["wall", 1,1,13,1,3,1,3,1,3,1,5,1,3,1,1,1,1],
			["wall", 1,3,1,11,1,5,1,1,1,3,1,5,1,1,1,3,1],
			["wall", 3,1,1,1,13,1,3,1,1,1,3,1,5,1,5],
			["wall", 1,3,1,7,1,3,1,3,1,3,1,3,1,7,1,3,1],
			["wall", 1,1,9,1,1,1,3,1,3,1,5,1,5,1,3,1,1,1,1],
			["wall", 1,1,1,5,1,1,1,1,1,9,1,5,1,3,1,3,1,1,1,1,1],
			["wall", 1,1,1,1,3,1,1,1,1,1,9,1,1,1,3,1,3,1,5,1,3],
			["wall", 1,1,1,3,1,5,1,7,1,3,1,3,1,3,1,7,1],
			["wall", 1,1,3,1,9,1,9,1,3,1,5,1,3,1,1],
			["wall", 1,1,1,1,1,9,1,13,1,7,1,1,1,1,1],
			["wall", 1,1,1,1,9,1,1,1,11,1,3,1,5,1,1,1,1],
			["wall", 1,1,1,5,1,1,1,3,1,1,1,5,1,3,1,5,1,5,1,1,1],
			["wall", 1,1,3,1,1,1,1,1,1,1,5,1,1,1,1,1,1,1,7,1,1,1,3,1,1,1,1],
			["wall", 1,5,1,3,1,7,1,1,1,1,1,9,1,3,1,3,1],
			["wall", 19,1,21]
			]
hugemazegrid = maze_generator(hugemazepattern)
hugemaze = Board(maze=hugemazegrid, house=False)
hugemazeproblem = BoardSearchProblem((0,19), (20,19), hugemaze, ["spot"])
