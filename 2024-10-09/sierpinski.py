import turtle

pen = turtle.Turtle()
pen.speed(0)

# Function to draw a triangle
def draw_triangle(points, color, pen):
    pen.fillcolor(color)
    pen.up()
    pen.goto(points[0][0], points[0][1])
    pen.down()
    pen.begin_fill()
    pen.goto(points[1][0], points[1][1])
    pen.goto(points[2][0], points[2][1])
    pen.goto(points[0][0], points[0][1])
    pen.end_fill()

# Function to calculate the midpoints
def get_mid(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]

# Recursive function to draw the Sierpinski triangle
def sierpinski(points, degree, pen):
    colors = ['blue', 'red', 'green', 'yellow', 'violet', 'orange']
    draw_triangle(points, colors[degree], pen)
    if degree > 0:
        sierpinski([points[0], get_mid(points[0], points[1]), get_mid(points[0], points[2])], degree - 1, pen)
        sierpinski([points[1], get_mid(points[0], points[1]), get_mid(points[1], points[2])], degree - 1, pen)
        sierpinski([points[2], get_mid(points[2], points[1]), get_mid(points[0], points[2])], degree - 1, pen)

# Set initial points and depth of recursion
points = [[-200, -100], [0, 200], [200, -100]]
degree = 5

sierpinski(points, degree, pen)
turtle.done()
