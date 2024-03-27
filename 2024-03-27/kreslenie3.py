import tkinter as tk

class AplikaciaPohyblivehoObjektu:
    def __init__(self, okno):
        self.okno = okno
        self.okno.title("Pohybujeme objektom šípkami")

        # Nastavujeme veľkosť plátna, kde sa bude objekt pohybovať
        self.platno = tk.Canvas(okno, width=600, height=400)
        self.platno.pack()

        # Vytvárame objekt, ktorý budeme pohybovať (napríklad modrý obdĺžnik)
        self.objekt = self.platno.create_rectangle(250, 150, 350, 250, fill="blue")

        # Sledujeme, ktoré šípky sú práve stlačené
        self.stlacene_sipky = {'Left': False, 'Right': False, 'Up': False, 'Down': False}

        # Zachytávame udalosti stlačenia a pustenia kláves
        self.okno.bind("<KeyPress>", self.pri_stlaceni_klavesu)
        self.okno.bind("<KeyRelease>", self.pri_pusteni_klavesu)

        # Neustále aktualizujeme pozíciu objektu
        self.aktualizuj_poziciu()

    # Funkcia reaguje na stlačenie klávesu
    def pri_stlaceni_klavesu(self, udalost):
        if udalost.keysym in self.stlacene_sipky:
            self.stlacene_sipky[udalost.keysym] = True

    # Funkcia reaguje na pustenie klávesu
    def pri_pusteni_klavesu(self, udalost):
        if udalost.keysym in self.stlacene_sipky:
            self.stlacene_sipky[udalost.keysym] = False

    # Táto funkcia aktualizuje pozíciu objektu na plátne
    def aktualizuj_poziciu(self):
        if self.stlacene_sipky['Left']:
            self.platno.move(self.objekt, -10, 0)
        if self.stlacene_sipky['Right']:
            self.platno.move(self.objekt, 10, 0)
        if self.stlacene_sipky['Up']:
            self.platno.move(self.objekt, 0, -10)
        if self.stlacene_sipky['Down']:
            self.platno.move(self.objekt, 0, 10)

        # Opäť plánujeme aktualizáciu pozície za 50 milisekúnd
        self.okno.after(50, self.aktualizuj_poziciu)

if __name__ == "__main__":
    hlavne_okno = tk.Tk()
    aplikacia = AplikaciaPohyblivehoObjektu(hlavne_okno)
    hlavne_okno.mainloop()
