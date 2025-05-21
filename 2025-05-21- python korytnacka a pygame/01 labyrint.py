import turtle, random

t = turtle.Turtle()
t.speed(10)
farby = ["red", "green", "blue", "orange", "purple", "yellow", "black"]

for krok in range(100):
    t.color(random.choice(farby))
    t.fd(20)
    t.lt(random.choice([0, 90, 180, 270]))
