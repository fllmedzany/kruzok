# Zoznam stromov
stromy = ['zeleny', 'modry', 'zeleny', 'modry', 'zeleny', 'zeleny']


def najdi_trojicu_a_index(stromy):
    # Prechádzame zoznam a skontrolujeme každú možnú trojicu
    for i in range(len(stromy) - 2):
        # Získame trojicu stromov
        trojica = stromy[i:i+3]
        # Počíta, koľko modrých a koľko zelených stromov je v trojici
        pocet_modrych = trojica.count('modry')
        pocet_zelenych = trojica.count('zeleny')
        # Skontrolujeme podmienku
        if pocet_modrych == 1 and pocet_zelenych == 2:
            return i, trojica  # Vráti index a trojicu
    return None  # Vráti None, ak nebol nájdený žiadny taký prípad



# Vyhľadávanie prvej vhodnej trojice a jej indexu
vysledok = najdi_trojicu_a_index(stromy)

if vysledok:
    index, trojica = vysledok
    print(f"Nájdená trojica na indexe {index}: {trojica}")
else:
    print("Nenašla sa žiadna vhodná trojica.")


def kuk ():
    return 1, 'janko'

vysledok = kuk()
a,b = vysledok
print (a)
print(b)
