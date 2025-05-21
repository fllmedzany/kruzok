import turtle, random

t = turtle.Turtle()
t.shape("circle")
t.shapesize(3)
t.penup()

def move(x, y):
    t.goto(random.randint(-200,200), random.randint(-200,200))

t.onclick(move)
turtle.done()
