import tkinter as tk

class AnimovanyObjekt:
    def __init__(self, canvas, x, y, velkost, farba):
        self.canvas = canvas
        self.velkost = velkost
        self.farba = farba
        self.id = canvas.create_oval(x, y, x + velkost, y + velkost, fill=farba)
        self.dx = 2
        self.dy = 2

    def pohni_sa(self):
        coords = self.canvas.coords(self.id)
        if coords[2] >= self.canvas.winfo_width() or coords[0] <= 0:
            self.dx = -self.dx
        if coords[3] >= self.canvas.winfo_height() or coords[1] <= 0:
            self.dy = -self.dy
        self.canvas.move(self.id, self.dx, self.dy)
        self.canvas.after(30, self.pohni_sa)

# Hlavná funkcia na spustenie animácie
def hlavna():
    root = tk.Tk()
    root.title("Animácia s tkinter")

    canvas = tk.Canvas(root, width=500, height=400)
    canvas.pack()

    objekt = AnimovanyObjekt(canvas, 50, 50, 30, "green")
    objekt.pohni_sa()

    root.mainloop()

hlavna()
