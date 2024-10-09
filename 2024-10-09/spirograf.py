import turtle
import math

pen = turtle.Turtle()
pen.speed(0)

# Function to draw a spirograph
def draw_spirograph(radius, step):
    for angle in range(0, 360, step):
        pen.circle(radius)
        pen.left(step)

draw_spirograph(100, 10)
turtle.done()
