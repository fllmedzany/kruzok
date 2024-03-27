import tkinter as tk

class MovingObjectApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Moving Object with Arrow Keys")

        # Nastavenie veľkosti plátna
        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.pack()

        # Vytvorenie objektu (napríklad obdĺžnika)
        self.object = self.canvas.create_rectangle(250, 150, 350, 250, fill="blue")

        # Pripojenie udalostí klávesnice
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)

    # Metódy na pohyb objektu
    def move_left(self, event):
        self.canvas.move(self.object, -10, 0)

    def move_right(self, event):
        self.canvas.move(self.object, 10, 0)

    def move_up(self, event):
        self.canvas.move(self.object, 0, -10)

    def move_down(self, event):
        self.canvas.move(self.object, 0, 10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovingObjectApp(root)
    root.mainloop()
