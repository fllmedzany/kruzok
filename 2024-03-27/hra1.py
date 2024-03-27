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
            self.platno.move(kruh, 0, 5)
            if self.platno.coords(kruh)[3] > self.vyska:
                self.platno.delete(kruh)
                self.kruhy.remove(kruh)
                self.zivoty -= 1  # Odrátame život, ak kruh dosiahne dolnú hranicu

        # Kontrola kolízií medzi guličkami a kruhmi
        for gulicka in self.gulicky[:]:
            g_x1, g_y1, g_x2, g_y2 = self.platno.coords(gulicka)
            for kruh in self.kruhy[:]:
                k_x1, k_y1, k_x2, k_y2 = self.platno.coords(kruh)
                if k_x1 < g_x2 and k_x2 > g_x1 and k_y1 < g_y2 and k_y2 > g_y1:
                    self.platno.delete(gulicka)
                    self.gulicky.remove(gulicka)
                    self.platno.delete(kruh)
                    self.kruhy.remove(kruh)
                    self.skore += 1
                    break  # Pretože gulička už bola odstránená, skončíme vnorený cyklus

        # Aktualizácia hry
        self.okno.after(50, self.aktualizuj_hru)

        # Kontrola konca hry
        if self.zivoty <= 0:
            self.koniec_hry()

    def koniec_hry(self):
        self.platno.delete("all")  # Vymažeme všetko z plátna
        self.platno.create_text(self.sirka / 2, self.vyska / 2, text="Koniec hry", font=('Arial', 24), fill="red")
        self.platno.create_text(self.sirka / 2, self.vyska / 2 + 30, text=f"Skóre: {self.skore}", font=('Arial', 20), fill="black")

if __name__ == "__main__":
    hlavne_okno = tk.Tk()
    hra = JednoduchaHra(hlavne_okno)
    hlavne_okno.mainloop()

                             
