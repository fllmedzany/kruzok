import turtle, random

t = turtle.Turtle()
t.speed(0)

for i in range(36):
    t.color(random.choice(["red", "orange", "yellow", "green", "blue", "purple"]))
    t.circle(60)
    t.right(10)
    
