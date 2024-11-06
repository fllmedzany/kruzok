'''
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
Pravidlá:

v nekonečnej štvorcovej sieti žijú bunky,
ktoré sa rôzne rozmnožujú, resp. umierajú

v každom políčku siete je buď živá bunka,
alebo je políčko prázdne (budeme označovať ako 1 a 0)

každé políčko má 8 susedov
(vodorovne, zvislo aj po uhlopriečke)

v každej generácii sa s každým jedným políčkom urobí:

ak je na políčku bunka a má práve 2 alebo 3 susedov,
tak táto bunka prežije aj do ďalšej generácie

ak je na políčku bunka a má buď 0 alebo 1 suseda,
alebo viac ako 3 susedov,
tak bunka na tomto políčku do ďalšej generácie neprežije (umiera)

ak má prázdne políčko presne na troch susediacich políčkach živé bunky,
tak sa tu v ďalšej generácii narodí nová bunka

Štvorcovú sieť s 0 a 1 budeme ukladať v dvojrozmernej tabuľke
veľkosti n x n. V tejto tabuľke je momentálna generácia bunkových živočíchov.
Na to, aby sme vyrobili novú generáciu, si pripravíme pomocnú tabuľku
rovnakej veľkosti a do nej budeme postupne zapisovať bunky novej generácie.
Keď už bude celá táto pomocná tabuľka hotová, prekopírujeme ju do pôvodnej tabuľky.
Dvojrozmernú tabuľku budeme vykresľovať do grafickej plochy.

viac na https://python.input.sk/z/13.html#hra-life


'''
import tkinter
import random

def inic(n):
    vysl = [[random.randrange(10) == 1 for j in range(n)] for i in range(n)]
##    vysl[5][2] = vysl[5][3] = vysl[5][4] = vysl[4][4] = vysl[3][3] = 1
##    vysl[6][47] = vysl[6][46] = vysl[6][45] = vysl[5][45] = vysl[4][46] = 1
    return vysl

def kresli(tab, d=8):
    canvas.delete('all')
    for r, riadok in enumerate(tab):
        for s, prvok in enumerate(riadok):
            x, y = s * d + 5, r * d + 5
            farba = ('white', 'black')[prvok]
            canvas.create_rectangle(x, y, x + d, y + d, fill=farba, outline='lightgray')
    canvas.update()

def nova_generacia(p):
    nova = [[0] * len(p[r]) for r in range(len(p))]
    for r in range(1, len(p) - 1):
        for s in range(1, len(p[r])-1):
            ps = (p[r-1][s-1] + p[r-1][s] + p[r-1][s+1] +
                  p[r][s-1]   +             p[r][s+1] +
                  p[r+1][s-1] + p[r+1][s] + p[r+1][s+1])
            if ps == 3 or ps == 2 and p[r][s]:
                nova[r][s] = 1
    return nova

canvas = tkinter.Canvas(width=410, height=410)
canvas.pack()

plocha = inic(50)
kresli(plocha)
for i in range(1000):
    plocha = nova_generacia(plocha)
    kresli(plocha)

tkinter.mainloop()
