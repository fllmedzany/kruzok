import turtle

pen = turtle.Turtle()
pen.speed(0)

colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

# Recursive function to draw a spiral
def recursive_spiral(size, angle, step, depth):
    if depth == 0:
        return
    pen.color(colors[depth % len(colors)])
    pen.forward(size)
    pen.right(angle)
    recursive_spiral(size + step, angle, step, depth - 1)

recursive_spiral(50, 45, 5, 100)
turtle.done()

