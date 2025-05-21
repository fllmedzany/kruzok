import turtle
import random

screen = turtle.Screen()
screen.title("Had - jednoduchá hra")
screen.bgcolor("lightgreen")
screen.setup(width=500, height=500)
screen.tracer(0)

def start_game():
    global hlava, segments, potrava, skore, skore_turtle, game_over, pridaj_segment_flag, posledna_pozicia

    screen.clear()
    screen.bgcolor("lightgreen")
    screen.title("Had - jednoduchá hra")
    screen.tracer(0)

    # Hadia hlava
    hlava = turtle.Turtle()
    hlava.shape("square")
    hlava.color("darkgreen")
    hlava.penup()
    hlava.goto(0, 0)
    hlava.direction = "stop"
    segments = []
    posledna_pozicia = hlava.position()

    # Potrava
    potrava = turtle.Turtle()
    potrava.shape("circle")
    potrava.color("red")
    potrava.penup()
    potrava.goto(random.randint(-230, 230), random.randint(-230, 230))

    # Skóre
    skore_turtle = turtle.Turtle()
    skore_turtle.hideturtle()
    skore_turtle.penup()
    skore_turtle.goto(-230, 210)
    skore = 0
    skore_turtle.clear()
    skore_turtle.write(f"Skóre: {skore}", font=("Arial", 14, "normal"))

    global game_over, pridaj_segment_flag
    game_over = False
    pridaj_segment_flag = False

    def hore():
        if hlava.direction != "down":
            hlava.direction = "up"
    def dole():
        if hlava.direction != "up":
            hlava.direction = "down"
    def vlavo():
        if hlava.direction != "right":
            hlava.direction = "left"
    def vpravo():
        if hlava.direction != "left":
            hlava.direction = "right"

    screen.listen()
    screen.onkey(hore, "Up")
    screen.onkey(dole, "Down")
    screen.onkey(vlavo, "Left")
    screen.onkey(vpravo, "Right")
    screen.onkey(restart, "r")

    hra()

def pohyb():
    global posledna_pozicia
    posledna_pozicia = hlava.position()
    if hlava.direction == "up":
        y = hlava.ycor()
        hlava.sety(y + 20)
    if hlava.direction == "down":
        y = hlava.ycor()
        hlava.sety(y - 20)
    if hlava.direction == "left":
        x = hlava.xcor()
        hlava.setx(x - 20)
    if hlava.direction == "right":
        x = hlava.xcor()
        hlava.setx(x + 20)

def hra():
    global skore, game_over, pridaj_segment_flag, posledna_pozicia

    if game_over:
        return

    # pohni telo (zozadu dopredu)
    if len(segments) > 0:
        for i in range(len(segments)-1, 0, -1):
            x = segments[i-1].xcor()
            y = segments[i-1].ycor()
            segments[i].goto(x, y)
        segments[0].goto(hlava.xcor(), hlava.ycor())

    pohyb()

    # Ak je potrebné pridať segment (po zjedení potravy)
    if pridaj_segment_flag:
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("green")
        new_segment.penup()
        new_segment.goto(posledna_pozicia)
        segments.append(new_segment)
        pridaj_segment_flag = False

    # Skontroluj kolíziu s potravou
    if hlava.distance(potrava) < 20:
        potrava.goto(random.randint(-230, 230), random.randint(-230, 230))
        pridaj_segment_flag = True   # flag na pridanie segmentu po pohybe
        skore += 1
        skore_turtle.clear()
        skore_turtle.write(f"Skóre: {skore}", font=("Arial", 14, "normal"))

    # Skontroluj náraz do steny
    if (hlava.xcor() > 240 or hlava.xcor() < -240 or
        hlava.ycor() > 240 or hlava.ycor() < -240):
        game_over = True
        skore_turtle.goto(-110, 0)
        skore_turtle.write("Koniec hry! Stlač 'r' pre reštart", font=("Arial", 16, "bold"))
        return

    # Skontroluj náraz do seba
    for segment in segments:
        if segment.distance(hlava) < 20:
            game_over = True
            skore_turtle.goto(-110, 0)
            skore_turtle.write("Koniec hry! Stlač 'r' pre reštart", font=("Arial", 16, "bold"))
            return

    screen.update()
    screen.ontimer(hra, 150)

def restart():
    start_game()

# Prvý štart
start_game()
screen.mainloop()
