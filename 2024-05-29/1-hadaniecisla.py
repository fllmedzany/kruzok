import random

number_to_guess = random.randint(1, 100)
attempts = 0

print("Hádaj číslo medzi 1 a 100")

while True:
    guess = int(input("Tvoj tip: "))
    attempts += 1
    if guess < number_to_guess:
        print("Vyššie!")
    elif guess > number_to_guess:
        print("Nižšie!")
    else:
        print(f"Uhádol si číslo {number_to_guess} za {attempts} pokusov!")
        break
