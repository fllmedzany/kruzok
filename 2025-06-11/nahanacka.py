import turtle
import threading
import time
import math

# --- Nastavenie okna a korytnačiek ---
screen = turtle.Screen()
screen.title("Korytnačia naháňačka")
screen.setup(width=600, height=600)

zlodej = turtle.Turtle()
zlodej.color("blue")
zlodej.shape("turtle")
zlodej.penup()

policajt = turtle.Turtle()
policajt.color("red")
policajt.shape("turtle")
policajt.penup()
policajt.goto(200, 200)

chyteny = threading.Event()

# --- Ovládanie utečenca klávesmi ---
def vpred():
    zlodej.forward(20)
def vlavo():
    zlodej.left(30)
def vpravo():
    zlodej.right(30)
def vzad():
    zlodej.backward(20)

screen.listen()
screen.onkeypress(vpred, "Up")
screen.onkeypress(vzad, "Down")
screen.onkeypress(vlavo, "Left")
screen.onkeypress(vpravo, "Right")

# --- Funkcia pohybu naháňača vo vlákne ---
def policajt_thread():
    while not chyteny.is_set():
        # Vypočítať smer k utečencovi
        x1, y1 = policajt.position()
        x2, y2 = zlodej.position()
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        policajt.setheading(angle)
        policajt.forward(5)
        # Kontrola vzdialenosti
        if policajt.distance(zlodej) < 20:
            chyteny.set()
            policajt.write("Chytený!", align="center", font=("Arial", 20, "bold"))
            break
        time.sleep(0.015)

# --- Spustiť vlákno pre naháňača ---
t = threading.Thread(target=policajt_thread)
t.daemon = True
t.start()

# --- Hlavná slučka ---
screen.mainloop()
