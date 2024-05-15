import random
class Zvieratko:
    def __init__(self, meno, zvuk):
        self.meno = meno
        self.zvuk = zvuk

    def urob_zvuk(self):
        print(f"{self.meno} robí zvuk {self.zvuk}")

class Pes(Zvieratko):
    def __init__(self, meno):
        super().__init__(meno, "haf-haf")

class Macka(Zvieratko):
    def __init__(self, meno):
        super().__init__(meno, "mňau-mňau")

    def urob_zvuk(self):
        if (random.randint(0,2)) == 1:
            print(f"{self.meno} sa nechce")
        else:
            super().urob_zvuk()
        

pes = Pes("Buddy")
macka = Macka("Mimi")

pes.urob_zvuk()  # Buddy robí zvuk haf-haf
macka.urob_zvuk()  # Mimi robí zvuk mňau-mňau
macka.urob_zvuk()  # Mimi robí zvuk mňau-mňau
macka.urob_zvuk()  # Mimi robí zvuk mňau-mňau
macka.urob_zvuk()  # Mimi robí zvuk mňau-mňau
macka.urob_zvuk()  # Mimi robí zvuk mňau-mňau
macka.urob_zvuk()  # Mimi robí zvuk mňau-mňau

