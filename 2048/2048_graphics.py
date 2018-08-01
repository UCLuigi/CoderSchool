import math
import random
import time
import turtle as t

grid=[['']*4,['']*4,['']*4,['']*4]

max_digits = 5
# displays the board via command line for debugging
def gridify(grid):
	rtn_str = "-"*(len(grid[0])*(max_digits + 2) + 5) + "\n"
	for row in grid:
		rtn_str += "|"
		for num in row:
			digits = len(str(num))
			rtn_str += " " * int((max_digits-len(str(num)))/2 + 1) + str(num) + " " * math.ceil((max_digits-len(str(num)))/2 + 1) + "|"
		rtn_str += "\n" + "-"*(len(grid[0])*(max_digits + 2) + 5) + "\n"
	return rtn_str

# insert a new tile at random location
def newtile(grid):
	# FILL IN HERE

	emptyspots=[]
	for i in range(4):
		for j in range(4):
			if grid[i][j]=="":
				emptyspots.append((i,j))
	spot=random.choice(emptyspots)
	grid[spot[0]][spot[1]]=random.choice([2,2,2,2,4])

score=0
# moves all tiles left and increments score as necessary, see 2048_text.py for explanation of steps
def left(grid):
	score=0
	for i in range(4):
		combined=[False]*4
		for j in range(4):
			if grid[i][j]=="":
				continue
			moving=grid[i][j]
			grid[i][j]=""
			for spot in range(j,-2,-1):
				if spot==-1:
					grid[i][0]=moving
					break
				if grid[i][spot]=="":
					continue
				if grid[i][spot]==moving and not combined[spot]:
					grid[i][spot]*=2
					score+=moving*2
					combined [spot]=True
					break
				grid[i][spot+1]=moving
				break
	return score

def right(grid):
	# FILL IN HERE
	score=0
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
					score+=moving*2
					combined [spot]=True
					break
				grid[i][spot-1]=moving
				break
	return score

def up(grid):
	score=0
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
					score+=moving*2
					combined [spot]=True
					break
				grid[spot+1][j]=moving
				break
	return score

def down(grid):
	# FILL IN HERE
	score=0
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
					score+=moving*2
					combined [spot]=True
					break
				grid[spot-1][j]=moving
				break
	return score

# Check whether a particular move is valid (changes the board state)
def valid_move(grid,move):
	grid2=[row.copy() for row in grid]
	move(grid2)
	if grid2 !=grid:
		return True

# Command line user input (for debugging or before graphics implementation)
def user_input(grid):
	while True:
		response=input("Move using W,A,S,D\n").lower()
		if response=="w":
			if valid_move(grid, up):
				return up(grid)
		elif response=="a":
			if valid_move(grid, left):
				return left(grid)
		elif response=="s":
			if valid_move(grid, down):
				return down(grid)
		elif response=="d":
			if valid_move(grid, right):
				return right(grid)
		else:
			print ("Invalid Input Try Again")

# Check for win condition
def is_win(grid):
	# FILL IN HERE
	for row in grid:
		if 2048 in row:
			return True
	return False

# Check for loss condition
def is_lose(grid):
	# FILL IN HERE
	return not valid_move(grid, left) and not valid_move(grid, right) and not valid_move(grid, up) and not valid_move(grid, down)

# Graphics helper to draw a square
def draw_square(size,position,color1,color2):
	# FILL IN HERE
	t.pu()
	t.goto(position)
	t.pd()
	t.color(color1,color2)
	t.begin_fill()
	for i in range(4):
		t.forward(size)
		t.right(90)
	t.end_fill()

# Color scheme choices
bgcolor="#CAA877"
gridcolor="#CAA877"
tilecolor="#CAA877"

# Draw background grid
def drawgrid():
	draw_square(640,(-320,320),bgcolor,bgcolor)
	for i in range(4):
		for j in range(4):
			draw_square(140,(-320+16+156*j,320-16-156*i),gridcolor,gridcolor)

def tile_color(number, new_color):
	if number == 2:
		new_color = "#33FFAF"
	elif number == 4:
		new_color = "#3F33FF"
	elif number == 8:
		new_color = "#B533FF"
	elif number == 16:
		new_color = "#FF3333"
	elif number == 32:
		new_color = "#FFF033"
	elif number == 64:
		new_color ="#B2FF33"
	elif number == 128:
		new_color = "#25764B"
	elif number == 256:
		new_color = "#255F76"
	elif number == 512:
		new_color = "#76256C"
	elif number == 1024:
		new_color = "#80A866"
	else:
		new_color = "#A88C66"
	return new_color

# Helper to draw a tile with a number
def draw_tile(number,position):
	# FILL IN HERE
	new_color = None
	new_color = tile_color(number, new_color)
	draw_square(140,position,new_color,new_color)
	t.color("black","blue")
	t.pu()
	t.goto((position[0]+70,position[1]-107))
	t.pd()
	t.write(number,align="center",font=("Ubuntu",48,"normal"))

# Can_move prevents the user from spamming buttons before the graphics have finished updating
can_move=True

# Render the grid on the background
def render():
	t.clear()
	drawgrid()
	for i in range(4):
		for j in range(4):
			if grid[i][j]!="":
				draw_tile(grid[i][j],(-320+16+156*j,320-16-156*i))
	global can_move
	t.penup()
	t.goto((320,320))
	t.pendown()
	t.write("Score:"+str(score),align="right",font=("Ubuntu",60,"normal"))
	can_move=True
	t.update()

# Event handlers for the different directions
def handle_left():
	global can_move
	if can_move and valid_move(grid,left):
		can_move=False
		global score
		score+=left(grid)
		newtile(grid)
		render()
		if is_win (grid):
			t.goto((0,0))
			t.write("You Win!",align="center",font=("Ubuntu",60,"normal"))
			time.sleep(10)
			t.bye()
		if is_lose (grid):
			t.write("You lose!",align="center",font=("Ubuntu",60,"normal"))
			t.update()
			time.sleep(10)
			t.bye()

def handle_right():
	global can_move
	if can_move and valid_move(grid,right):
		can_move=False
		global score
		score+=right(grid)
		newtile(grid)
		render()
		if is_win (grid):
			t.goto((0,0))
			t.write("You Win!",align="center",font=("Ubuntu",60,"normal"))
			time.sleep(10)
			t.bye()
		if is_lose (grid):
			t.write("You lose!",align="center",font=("Ubuntu",60,"normal"))
			t.update()
			time.sleep(10)
			t.bye()

def handle_up():
	global can_move
	if can_move and valid_move(grid,up):
		can_move=False
		global score
		score+=up(grid)
		newtile(grid)
		render()
		if is_win (grid):
			t.goto((0,0))
			t.write("You Win!",align="center",font=("Ubuntu",60,"normal"))
			time.sleep(10)
			t.bye()
		if is_lose (grid):
			t.write("You lose!",align="center",font=("Ubuntu",60,"normal"))
			t.update()
			time.sleep(10)
			t.bye()

def handle_down():
	global can_move
	if can_move and valid_move(grid,down):
		can_move=False
		global score
		score+=down(grid)
		newtile(grid)
		render()
		if is_win (grid):
			t.goto((0,0))
			t.write("You Win!",align="center",font=("Ubuntu",60,"normal"))
			time.sleep(10)
			t.bye()
		if is_lose (grid):
			t.write("You lose!",align="center",font=("Ubuntu",60,"normal"))
			t.update()
			time.sleep(10)
			t.bye()

# Set up the game
newtile(grid)
newtile(grid)
t.ht()
t.getscreen().delay(0)
t.tracer(0,0)
render()
t.onkey(handle_left,"Left")	
t.onkey(handle_right,"Right")
t.onkey(handle_up,"Up")
t.onkey(handle_down,"Down")
t.listen()
t.mainloop()
