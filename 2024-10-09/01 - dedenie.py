import turtle
import random

# Naša vlastná trieda HviezdnaKorytnacka s menom a metódou na kreslenie hviezd
class HviezdnaKorytnacka(turtle.Turtle):
    def __init__(self, meno, farba):
        super().__init__()  # Volanie konštruktora nadradenej triedy
        self.meno = meno
        self.color(farba)
        self.pozicia = (random.randint(-300, 300), random.randint(-300, 300))  # Náhodná pozícia
    
    # Metóda na kreslenie hviezdy
    def nakresli_hviezdu(self, velkost):
        self.begin_fill()
        for _ in range(5):
            self.forward(velkost)
            self.right(144)
        self.end_fill()
    
    # Metóda na napísanie mena na obrazovku
    def napis_meno_na_obrazovku(self):
        self.penup()
        self.goto(self.pozicia[0], self.pozicia[1] + 50)  # Presunie korytnačku nad miesto hviezdy
        self.pendown()
        self.write(f"Ahoj, volám sa {self.meno}", font=("Arial", 16, "normal"))
        self.penup()
        self.goto(self.pozicia)  # Presunie sa späť na pozíciu pre kreslenie hviezdy
        self.pendown()

# Vytvorenie inštancií triedy HviezdnaKorytnacka s náhodnými pozíciami a anglickými názvami farieb
korytnacka1 = HviezdnaKorytnacka("Janko", "red")
korytnacka2 = HviezdnaKorytnacka("Misko", "green")
korytnacka3 = HviezdnaKorytnacka("Matus", "yellow")

# Každá korytnačka napíše svoje meno na obrazovku a nakreslí hviezdu
korytnacka1.napis_meno_na_obrazovku()
korytnacka1.nakresli_hviezdu(100)

korytnacka2.napis_meno_na_obrazovku()
korytnacka2.nakresli_hviezdu(100)

korytnacka3.napis_meno_na_obrazovku()
korytnacka3.nakresli_hviezdu(100)

turtle.done()
