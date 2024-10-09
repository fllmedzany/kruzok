import turtle
import random

pen = turtle.Turtle()
pen.speed(0)

colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

# Function to draw a rotating square
def rotating_square(size, angle):
    for i in range(100):
        pen.color(random.choice(colors))
        for _ in range(4):
            pen.forward(size)
            pen.left(90)
        pen.left(angle)
        size -= 2  # The square becomes smaller with each rotation

rotating_square(200, 10)
turtle.done()
