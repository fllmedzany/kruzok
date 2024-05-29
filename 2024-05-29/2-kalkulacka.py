def calculator():
    print("Zadaj dve čísla a operáciu (+, -, *, /)")
    num1 = float(input("Prvé číslo: "))
    num2 = float(input("Druhé číslo: "))
    operation = input("Operácia: ")

    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Delenie nulou nie je povolené!"
    else:
        result = "Neplatná operácia!"

    print(f"Výsledok: {result}")

calculator()
