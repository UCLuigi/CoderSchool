import math
import random
grid = [["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]]
max_digits = 5

# displays the board (command line version)
def gridify(grid):
	rtn_str = "-"*(len(grid[0])*(max_digits + 2) + 5) + "\n"
	for row in grid:
		rtn_str += "|"
		for num in row:
			digits = len(str(num))
			rtn_str += " " * int((max_digits-digits)/2 + 1) + str(num) + " " * math.ceil((max_digits-digits)/2 + 1) + "|"
		rtn_str += "\n" + "-"*(len(grid[0])*(max_digits + 2) + 5) + "\n"
	return rtn_str


# initializes grid with two randomly placed 2s. Could also use ran_insert twice
def start(grid):
	x1 = 0
	x2 = 0
	y1 = 0
	y2 = 0
	while x1 == x2 and y1 == y2:
		x1 = random.randint(0,3)
		y1 = random.randint(0,3)
		x2 = random.randint(0,3)
		y2 = random.randint(0,3)
	grid[y1][x1] = 2
	grid[y2][x2] = 2

# randomly inserts a tile after movement
def ran_insert (grid):
	free_spots=[]
	for x in range(4):
		for y in range(4):
			if grid[y][x]=="":
				free_spots.append((x,y))

	i=random.randint(0,len(free_spots)-1)
	x,y=free_spots[i]
	random_entry=random.sample([2,2,2,4],1)[0]
	grid[y][x]=random_entry

# moves all tiles left
def left(grid):
	for i in range(4):
		# placements are finalized left to right, tracks which spots have combined to prevent double combinations
		combined=[False]*4
		for j in range(4):
			# skip blanks
			if grid[i][j]=="":
				continue
			# pick up number encountered
			moving=grid[i][j]
			grid[i][j]=""
			# move number to the left until an end case is hit
			for spot in range(j,-2,-1):
				# case 1: ran off edge of row - place number in first spot
				if spot==-1:
					grid[i][0]=moving
					break
				# skip blanks
				if grid[i][spot]=="":
					continue
				# case 2: found same number to combine with
				if grid[i][spot]==moving and not combined[spot]:
					grid[i][spot]*=2
					combined [spot]=True
					break
				# case 3: found different number or number is already combined
				grid[i][spot+1]=moving
				break

# moves all tiles right
def right(grid):
	for i in range(4):
		combined=[False]*4
		for j in range(3,-1,-1):
			if grid[i][j]=="":
				continue
			moving=grid[i][j]
			grid[i][j]=""
			for spot in range(j,5):
				if spot==4:
					grid[i][3]=moving
					break
				if grid[i][spot]=="":
					continue
				if grid[i][spot]==moving and not combined[spot]:
					grid[i][spot]*=2
					combined [spot]=True
					break
				grid[i][spot-1]=moving
				break

# moves all tiles up
def up(grid):
	for j in range(4):
		combined=[False]*4
		for i in range(4):
			if grid[i][j]=="":
				continue
			moving=grid[i][j]
			grid[i][j]=""
			for spot in range(i,-2,-1):
				if spot==-1:
					grid[0][j]=moving
					break
				if grid[spot][j]=="":
					continue
				if grid[spot][j]==moving and not combined[spot]:
					grid[spot][j]*=2
					combined [spot]=True
					break
				grid[spot+1][j]=moving
				break

# moves all tiles down
def down(grid):
	for j in range(4):
		combined=[False]*4
		for i in range(3,-1,-1):
			if grid[i][j]=="":
				continue
			moving=grid[i][j]
			grid[i][j]=""
			for spot in range(i,5):
				if spot==4:
					grid[3][j]=moving
					break
				if grid[spot][j]=="":
					continue
				if grid[spot][j]==moving and not combined[spot]:
					grid[spot][j]*=2
					combined [spot]=True
					break
				grid[spot-1][j]=moving
				break

# get player's input and validate
def player_input(grid):
	valid_response=False
	while not valid_response:
		testgrid=[row.copy() for row in grid]
		r=input('wasd to move\n')
		if r == 'w':
			up(testgrid)
			for i in range(4):
				if grid[i]!=testgrid[i]:
					valid_response=True
					up(grid)
					return
			print("invalid move")
		elif r=='a':
			left(testgrid)
			for i in range(4):
				if grid[i]!=testgrid[i]:
					valid_response=True
					left(grid)
					return
			print("invalid move")
		elif r=='s':
			down(testgrid)
			for i in range(4):
				if grid[i]!=testgrid[i]:
					valid_response=True
					down(grid)
					return
			print("invalid move")
		elif r=='d':
			right(testgrid)
			for i in range(4):
				if grid[i]!=testgrid[i]:
					valid_response=True
					right(grid)
					return
			print("invalid move")
		else:
			print('invalid move')

# check win condition
def is_win(grid):
	for row in grid:
		for number in row:
			if number==2048:
				return True
	return False

# check whether board state is a loss via attempting each movement
def is_lose(grid):
	testgrid=[row.copy() for row in grid]
	right(testgrid)
	for i in range(4):
		if grid[i]!=testgrid[i]:
			return False
	left(testgrid)
	for i in range(4):
		if grid[i]!=testgrid[i]:
			return False
	up(testgrid)
	for i in range(4):
		if grid[i]!=testgrid[i]:
			return False
	down(testgrid)
	for i in range(4):
		if grid[i]!=testgrid[i]:
			return False
	return True

# game loop
start(grid)
print(gridify(grid))
while not is_win(grid) and not is_lose(grid):
	player_input(grid)
	ran_insert(grid)
	print(gridify(grid))
if is_lose(grid):
	print("you lose")
if is_win(grid):
	print("you win")