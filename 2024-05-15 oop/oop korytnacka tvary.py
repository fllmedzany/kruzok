import turtle

class Tvar:
    def __init__(self, farba, strana):
        self.farba = farba
        self.strana = strana
        self.turtle = turtle.Turtle()

    def nakresli(self):
        pass

class Stvorec(Tvar):
    def nakresli(self):
        self.turtle.color(self.farba)
        for _ in range(4):
            self.turtle.forward(self.strana)
            self.turtle.right(90)

class Trojuholnik(Tvar):
    def nakresli(self):
        self.turtle.color(self.farba)
        for _ in range(3):
            self.turtle.forward(self.strana)
            self.turtle.right(120)

# Hlavná funkcia na kreslenie tvarov
def hlavna():
    stvorec = Stvorec("red", 100)
    trojuholnik = Trojuholnik("blue", 100)

    stvorec.nakresli()
    trojuholnik.nakresli()

    turtle.done()

hlavna()
