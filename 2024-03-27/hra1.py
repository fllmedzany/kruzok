import tkinter as tk
import random

class JednoduchaHra:
    def __init__(self, okno):
        self.okno = okno
        self.okno.title("Lietadlo vs Kruhy")

        # Nastavenia hry
        self.sirka = 600
        self.vyska = 400
        self.zivoty = 3
        self.skore = 0

        # Nastavujeme plátno
        self.platno = tk.Canvas(okno, width=self.sirka, height=self.vyska)
        self.platno.pack()

        # Vytvorenie lietadla
        self.lietadlo = self.platno.create_rectangle(275, 350, 325, 370, fill="green")

        # Sledovanie stlačených kláves
        self.stlacene_klavesy = {'Left': False, 'Right': False, 'space': False}

        # Objekty vo hre
        self.kruhy = []
        self.gulicky = []

        self.okno.bind("<KeyPress>", self.pri_stlaceni_klavesu)
        self.okno.bind("<KeyRelease>", self.pri_pusteni_klavesu)

        self.aktualizuj_hru()

    def pri_stlaceni_klavesu(self, udalost):
        self.stlacene_klavesy[udalost.keysym] = True

    def pri_pusteni_klavesu(self, udalost):
        self.stlacene_klavesy[udalost.keysym] = False

    def aktualizuj_hru(self):
        # Pohyb lietadla
        if self.stlacene_klavesy['Left'] and self.platno.coords(self.lietadlo)[0] > 0:
            self.platno.move(self.lietadlo, -10, 0)
        if self.stlacene_klavesy['Right'] and self.platno.coords(self.lietadlo)[2] < self.sirka:
            self.platno.move(self.lietadlo, 10, 0)

        # Streľba
        if self.stlacene_klavesy['space']:
            x1, y1, x2, y2 = self.platno.coords(self.lietadlo)
            stred = (x1 + x2) / 2
            self.gulicky.append(self.platno.create_oval(stred - 5, y1 - 10, stred + 5, y1, fill="red"))
            self.stlacene_klavesy['space'] = False  # Zabráni neustálej streľbe

        # Pohyb guličiek
        for gulicka in self.gulicky[:]:
            self.platno.move(gulicka, 0, -10)
            if self.platno.coords(gulicka)[1] < 0:
                self.platno.delete(gulicka)
                self.gulicky.remove(gulicka)

        # Pridávanie kruhov
        if random.randint(1, 50) == 1:  # Náhodné pridanie kruhu
            x = random.randint(0, self.sirka)
            self.kruhy.append(self.platno.create_oval(x - 20, 0, x + 20, 40, fill="blue"))

        # Pohyb kruhov
        for kruh in self.kruhy[:]:
            self.platno.move(kruh, 
