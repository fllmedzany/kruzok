import tkinter as tk
from tkinter import messagebox
import random

class Hrac:
    def __init__(self, meno, symbol):
        self.meno = meno
        self.symbol = symbol

    def tah(self, board, button_grid):
        pass  # Človek robí ťah interaktívne, takže tu je abstraktné

class PocitacovyHrac(Hrac):
    def __init__(self, meno, symbol):
        super().__init__(meno, symbol)

    def tah(self, board, button_grid):
        # Vyberie náhodné prázdne pole
        prazdne_polia = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
        if prazdne_polia:
            i, j = random.choice(prazdne_polia)
            board[i][j] = self.symbol
            button_grid[i][j].config(text=self.symbol, state="disabled")

class Piskvorky:
    def __init__(self, root):
        self.root = root
        self.root.title("Piškvorky")
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.button_grid = [[None for _ in range(3)] for _ in range(3)]
        self.hrac = Hrac("Človek", "X")
        self.pocitac = PocitacovyHrac("Počítač", "O")
        self.aktualny_hrac = self.hrac
        self.vytvor_hraciu_plochu()

    def vytvor_hraciu_plochu(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text="", width=10, height=3, 
                                   command=lambda i=i, j=j: self.clovek_tah(i, j))
                button.grid(row=i, column=j)
                self.button_grid[i][j] = button

    def clovek_tah(self, i, j):
        if self.board[i][j] == "":
            self.board[i][j] = self.hrac.symbol
            self.button_grid[i][j].config(text=self.hrac.symbol, state="disabled")
            if self.over_vyhru(self.hrac.symbol):
                self.ukonci_hru(f"{self.hrac.meno} vyhral!")
                return
            elif self.plocha_plna():
                self.ukonci_hru("Remíza!")
                return

            self.aktualny_hrac = self.pocitac
            self.root.after(500, self.pocitac_tah)  # Počkaj 500ms a nechaj počítač vykonať ťah

    def pocitac_tah(self):
        self.pocitac.tah(self.board, self.button_grid)
        if self.over_vyhru(self.pocitac.symbol):
            self.ukonci_hru(f"{self.pocitac.meno} vyhral!")
        elif self.plocha_plna():
            self.ukonci_hru("Remíza!")
        else:
            self.aktualny_hrac = self.hrac

    def over_vyhru(self, symbol):
        # Skontroluj riadky, stĺpce a diagonály
        for i in range(3):
            if all(self.board[i][j] == symbol for j in range(3)):
                return True
            if all(self.board[j][i] == symbol for j in range(3)):
                return True
        if all(self.board[i][i] == symbol for i in range(3)) or all(self.board[i][2-i] == symbol for i in range(3)):
            return True
        return False

    def plocha_plna(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def ukonci_hru(self, sprava):
        messagebox.showinfo("Koniec hry", sprava)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    hra = Piskvorky(root)
    root.mainloop()
