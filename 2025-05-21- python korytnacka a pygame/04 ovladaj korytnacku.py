import turtle

# Vytvorenie korytnačky
t = turtle.Turtle()
t.shape("turtle")
t.speed(2)

# Globálna premenna pre sledovanie, či je pero dole alebo hore
pero_dole = True

# Funkcie pre ovládanie
def dopredu():
    t.forward(30)
def dozadu():
    t.forward(-30)

def vlavo():
    t.left(90)

def vpravo():
    t.right(90)

def prepni_pero():
    global pero_dole
    if pero_dole:
        t.penup()
        pero_dole = False
    else:
        t.pendown()
        pero_dole = True

# Priradenie funkcií ku klávesám
turtle.listen()
turtle.onkey(dopredu, "Up")
turtle.onkey(dozadu, "Down")
turtle.onkey(vlavo, "Left")
turtle.onkey(vpravo, "Right")
turtle.onkey(prepni_pero, "space")

# Ukončenie programu kliknutím na okno
turtle.done()
