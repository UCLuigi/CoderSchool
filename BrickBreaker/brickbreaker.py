from processing import *
from math import pi,cos,sin
from random import random
from time import time

W,H = 450,450    #window width,height
radius =15       #ball radius
speed = 10        #ball speed
pwidth = 30      #paddle width
r,g,b = 0,121,184 #ball color
x,y,vx,vy = W/2,300,0.2*speed,0.6*speed

#######
paddle = 175
highscore = 0
curTime = time()
score = 0
bw, bh = 35,10 #brick width, brick height
squarex = [0, 75, 150, 225, 300, 375, 450]
squarey = [50,65,80,95,110,125,140,165]
drawbrick = [
  [1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1],
  [1,1,1,1,1,1,1,1]]


def resetGame(x,y,vx,vy):
  global drawbrick, score
  drawbrick = [[1]*8]*5
  
  x,y = W/2,300
  #random velocity downwards
  angle = pi/4 + pi/2*random()
  vx = speed*cos(angle)
  vy = speed*sin(angle)
  # if score > highscore:
  #   highscore = score
  score = 0
  return x,y,vx,vy,score

#####

def setup():
  frameRate(20)  #frames per second
  size(W,H)      #window size
  strokeWeight(10)  #line thickness
  
def moveBall(W,H,x,y,vx,vy,speed,radius,x1,x2): #add score later
  #move the ball
  x+=vx
  y+=vy
  # see if the ball bounces on the left or right
  if x<radius or x>W-radius:
    vx = -vx
  # see if the ball bounces on the top
  if y < radius:
    vy = -vy
  # see if the ball is moving downwards and hits the paddle
  if vy > 0 and y > (H-radius-7):
    if x >= x1 - 5 and x <= x2+5:
      vy = -vy
  # the paddle completely missed the ball
  if y> H+radius:
    x,y,vx,vy,score = resetGame(x,y,vx,vy)

  return x,y,vx,vy

#######

def ifTouchBrick(sqx,sqy):
  global x,y,score
  if (abs(x-(sqx+bw/2)) < (bw/2 + radius) and abs(y-(sqy+bh/2)) < bh/2+radius):
    score += 1
    return True, score
  return False  

######

def keyPressed():
  global paddle
  if keyboard.keyCode == LEFT:
    paddle = paddle - 20
  elif keyboard.keyCode == RIGHT:
    paddle = paddle + 20
  
def draw():
  global x,y,vx,vy ,score,curTime
  
  #####
  
  newTime = time()
  if (newTime - curTime) < 0.01:
    return
  curTime = newTime
  
  #####
  x1 = mouse.x - pwidth #mouse.x if using mouse / paddle if using key bindings
  x2 = mouse.x + pwidth #mouse.x if using mouse / paddle if using key bindings
  x,y,vx,vy = moveBall(W,H,x,y,vx,vy,speed,radius,x1,x2) #add score later
  background(0)
  
  #####
  #textsize(32)
  text("Score:" + str(score), 10,30)
  text("High:" + str(highscore), 215,30)
  #####
  
  #draw the ball
  fill(r,g,b)
  noStroke()
  ellipse(x,y,2*radius,2*radius)
  
  #draw the paddle
  stroke(255,255,0)
  line(x1,H-5,x2,H-5)
  noStroke()
  
  #####
  
  hitBrick = False
  for i in range(len(drawbrick[0])):
    bx = 20 + i*(bw+15)
    for j in range(len(drawbrick)):
      by = 85 + j*(bh + 15)
      if drawbrick[j][i] == 1:
        hitOneBrick = ifTouchBrick(bx, by)
        if hitOneBrick: 
          hitBrick = True 
          drawbrick[j][i] = 0
      if drawbrick[j][i] == 1:
        rect(bx, by, bw, bh,0)
        fill(r,g,b)
        noStroke()
  if hitBrick: 
    vy = -vy
  return
  
  #####

run()