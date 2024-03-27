import tkinter
import random

canvas = tkinter.Canvas()
canvas.pack()

ids=[]

for i in range(10):
    x = random.randint(0, 380)
    y = random.randint(0, 260)
    id = canvas.create_text(x, y, text='PYTHON')
    ids.append(id)
    



obr = tkinter.PhotoImage(file='pyton.png')
for x in range(80, 380, 120):
    id = canvas.create_image(x, 150, image=obr)
    ids.append(id)

tkinter.mainloop()
