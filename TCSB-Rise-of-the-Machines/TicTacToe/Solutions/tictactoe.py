import pygame
from pygame.locals import *

pygame.font.init()
titlefont = pygame.font.SysFont('Arial', 60)
menufont = pygame.font.SysFont('Arial', 30)

# Checks whether the given player has 3 pieces in a row on the given board
def is_win(grid, player):
	# Check if won by 3 in a row
	for row in range(3):
		if grid[row] == [player,player,player]:
			return True
	# Check if won by 3 in a column
	for column in range(3):
		threeinarow = True
		for row in range(3):
			if grid[row][column] != player:
				threeinarow = False
		if threeinarow:
			return True
	# Check the diagonals
	if grid[0][0] == player and grid[1][1] == player and grid[2][2] == player:
		return True
	if grid[0][2] == player and grid[1][1] == player and grid[2][0] == player:
		return True
	return False

# Checks whether the grid is a tie due to having no more spaces left
def is_tie(grid):
	for row in range(3):
		for column in range(3):
			if grid[row][column] == "":
				return False
	return True

# Returns all possible grids that could happen after one move from the given player
def get_successors(grid, player):
	successors = []
	for row in range(3):
		for column in range(3):
			# If a spot is empty, it's a potential move, so create a successor for it
			if grid[row][column] == "":
				copy = [row.copy() for row in grid]
				copy[row][column] = player
				successors.append(copy)
	return successors

# Evaluate how good a grid is. 1 = x wins, 0 = o wins, .5 = tie/not over yet
def evaluation_function(grid):
	if is_win(grid, "x"):
		return 1
	if is_win(grid, "o"):
		return 0
	return 0.5

def custom_evaluation_function(grid):
	# With a smarter evaluation function even the non-impossible AI can be nearly unstoppable.
	# Try assigning a score based on custom features like having the middle square or 2 in a row
	raise NotImplementedError()

# Utility function to return the opposing player
def other(player):
	if player == "x":
		return "o"
	else:
		return "x"

# Defines that x wishes to maximize the score while o wishes to minimize it. Optional to use this variable
player_functions = {'x': max, 'o': min}

# Recursively calculates the value of a particular grid
def value(grid, player, depth, maxdepth):
	# Terminal conditions - stop recursing and return a value
	if is_win(grid, player) or is_win(grid, other(player)) or is_tie(grid) or depth >= maxdepth:
		return evaluation_function(grid)
	# Recursively get the value of each child
	children = get_successors(grid, player)
	child_values = []
	for i in range(len(children)):
		child_values.append(value(children[i], other(player), depth+1, maxdepth))
	# Choose the best score for this player
	comparison = player_functions[player]
	return comparison(child_values)

# Uses value() to get the score for each of grid's children then chooses the best child
def minimax(grid, player, maxdepth):
	# Terminal conditions - stop recursing and return a value
	if is_win(grid, player) or is_win(grid, other(player)) or is_tie(grid):
		raise ValueError("Cannot choose next best move when game has terminated")
	# Recursively get the value of each child
	children = get_successors(grid, player)
	child_values = []
	for i in range(len(children)):
		child_values.append(value(children[i], other(player), 0, maxdepth))
	# Choose the best child for this player
	comparison = player_functions[player]
	bestvalue = comparison(child_values)
	return children[child_values.index(bestvalue)]	

# Used to reset the grid after the game ends
def empty_grid():
	return [["","",""],["","",""],["","",""]]

# The main class which runs the game
class App:
	def __init__(self):
		self._running = True
		self.screen = None
		self.size = self.width, self.height = 600, 600
		
		# Variables for the player, AI difficulty, and grid of pieces
		self.grid = empty_grid()
		self.player = "x"
		self.difficulty = 1
		
		# Helper variables for making the menu and game over screens work properly
		self.menu = True
		self.gameover = False
		self.waitcounter = 0
		self.clock = pygame.time.Clock()
		self.message = None

	# Set up the screen
	def on_init(self):
		pygame.init()
		self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self._running = True

	# Whenever a key is pressed or the screen is clicked, handle the event
	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			x,y = pygame.mouse.get_pos()
			# On the menu, handle each of the 4 buttons
			if self.menu:
				if x > 225 and x < 375:
					if y > 100 and y < 175:
						self.menu = False
						if self.player == "o":
							self.grid = minimax(self.grid, other(self.player), self.difficulty)
					if y > 450 and y < 525:
						self._running = False
				if x > 125 and x < 275:
					if y > 250 and y < 325:
						self.difficulty = 1
					if y > 350 and y < 425:
						self.player = "x"
				if x > 325 and x < 475:
					if y > 250 and y < 325:
						self.difficulty = 4
					if y > 250 and y < 425:
						self.player = "o"

			# Outside of the menu, determine where the player clicked and try to move there
			else:
				if not self.gameover:
					x,y = pygame.mouse.get_pos()
					i,j = 0,0
					if x < 200:
						j = 0
					elif x > 400:
						j = 2
					else:
						j = 1
					if y < 200:
						i = 0
					elif y > 400:
						i = 2
					else:
						i = 1
					if self.grid[i][j] == "":
						self.grid[i][j] = self.player
						# Check whether the game should now end due to a win or tie
						if is_win(self.grid, self.player):
							self.message = "You Win!"
							self.gameover=True
							self.grid = empty_grid()
							return
						if is_tie(self.grid):
							self.message = "Cat's game"
							self.gameover=True
							self.grid = empty_grid()
							return
						# Let the AI move if the game isn't over
						self.grid = minimax(self.grid, other(self.player), self.difficulty)
						# Check whether the game should now end due to a loss or tie
						if is_win(self.grid, other(self.player)):
							self.message = "You Lose!"
							self.gameover=True
							self.grid = empty_grid()
							return
						if is_tie(self.grid):
							self.message = "Cat's game"
							self.gameover=True
							self.grid = empty_grid()
							return

	# Counts loops to wait 4 seconds after game over before returning to menu
	def on_loop(self):
		self.clock.tick(60)
		if self.gameover:
			self.waitcounter += 1
			if self.waitcounter == 60 * 4:
				self.waitcounter = 0
				self.gameover = False
				self.menu = True
				self.message = None

	# Draws all graphics
	def on_render(self):
		self.screen.fill((255,255,255))
		# Draws either the current game or the end game message
		if not self.menu:
			if self.message:
				messagesurface = titlefont.render(self.message, False, (0,0,0))
				self.screen.blit(messagesurface, (self.width//2 - messagesurface.get_width()//2, self.height//2 - messagesurface.get_height()//2))
			else:
				pygame.draw.line(self.screen, (0,0,0), (200,0), (200,600))
				pygame.draw.line(self.screen, (0,0,0), (400,0), (400,600))
				pygame.draw.line(self.screen, (0,0,0), (0,200), (600,200))
				pygame.draw.line(self.screen, (0,0,0), (0,400), (600,400))
				for row in range(3):
					for col in range(3):
						if self.grid[row][col] == "o":
							pygame.draw.circle(self.screen, (0,0,0), (col*200+100, row*200+100), 75, 1)
						if self.grid[row][col] == "x":
							pygame.draw.line(self.screen, (0,0,0), (col*200-53+100, row*200-53+100), (col*200+53+100,row*200+53+100))
							pygame.draw.line(self.screen, (0,0,0), (col*200+53+100, row*200-53+100), (col*200-53+100,row*200+53+100))
		# Draws the menu buttons and captions
		else:
			titlesurface = titlefont.render("Tic Tac Toe", False, (0,0,0))
			self.screen.blit(titlesurface, (180, 10))
			# Play button
			pygame.draw.rect(self.screen, (200,200,200), (225, 100, 150, 75))
			textsurface = menufont.render("Play", False, (0,0,0))
			self.screen.blit(textsurface, (280,120))
			# Regular difficulty
			pygame.draw.rect(self.screen, (100,200,100), (125, 250, 150, 75))
			textsurface = menufont.render("Regular", False, (0,0,0))
			self.screen.blit(textsurface, (150,270))
			# Impossible difficulty
			pygame.draw.rect(self.screen, (200,100,100), (325, 250, 150, 75))
			textsurface = menufont.render("Impossible", False, (0,0,0))
			self.screen.blit(textsurface, (350,270))
			# Play as X
			pygame.draw.rect(self.screen, (200,200,200), (125, 350, 150, 75))
			textsurface = menufont.render("Play as X", False, (0,0,0))
			self.screen.blit(textsurface, (150,370))
			# Play as O
			pygame.draw.rect(self.screen, (200,200,200), (325, 350, 150, 75))
			textsurface = menufont.render("Play as O", False, (0,0,0))
			self.screen.blit(textsurface, (350,370))
			# Quit button
			pygame.draw.rect(self.screen, (200,200,200), (225, 450, 150, 75))
			textsurface = menufont.render("Quit", False, (0,0,0))
			self.screen.blit(textsurface, (280,470))
		pygame.display.update()
	
	def on_cleanup(self):
		pygame.quit()
 
 	# Calls the other functions in the correct order and fetches events
	def on_execute(self):
		if self.on_init() == False:
			self._running = False
 
		while( self._running ):
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
		self.on_cleanup()
 
if __name__ == "__main__" :
	theApp = App()
	theApp.on_execute()