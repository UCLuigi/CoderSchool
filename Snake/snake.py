screen = Screen()
screen.setup(400, 400)

snake = Turtle()
snake.up()
snake.shape('square')
score = 0

def random_pellet():
  pellet = Turtle()
  pellet.hideturtle()
  pellet.shape('circle')
  x = random.randint(-190, 190)
  y = random.randint(-190, 190)
  pellet.up()
  pellet.setpos(x, y)
  pellet.showturtle()
  return pellet

def add_wall():
  wall = Turtle()
  wall.hideturtle()
  wall.shape('square')
  x = random.randint(-190, 190)
  y = random.randint(-190, 190)
  wall.up()
  wall.setpos(x, y)
  pellet.showturtle()
  return wall

def up():
  if not snake.heading() == 270:
    snake.seth(90)
  
def right():
  if not snake.heading() == 180:
    snake.seth(0)
  
def left():
  if not snake.heading() == 0:
    snake.seth(180)
  
def down():
  if not snake.heading() == 90:
    snake.seth(270)

screen.onkey(up,"Up")
screen.onkey(left,"Left")
screen.onkey(right, "Right")
screen.onkey(down, "Down")

pellet = random_pellet()

while True:
  
  snake.forward(1)
  
  if snake.xcor() > pellet.xcor() - 10 and snake.xcor() < pellet.xcor() + 10 \
    and snake.ycor() > pellet.ycor() - 10 and snake.ycor() < pellet.ycor() + 10:
    score += 1
    print("Score: " + str(score))
    pellet.hideturtle()
    pellet = random_pellet()
    add_wall()
    
  if snake.xcor() > 190 or snake.xcor() < -190:
    break
  
  if snake.ycor() > 190 or snake.ycor() < -190:
    break
  
  screen.listen()