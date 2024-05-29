def convert_units(meters):
    kilometers = meters / 1000
    centimeters = meters * 100
    millimeters = meters * 1000
    return kilometers, centimeters, millimeters

meters = float(input("Zadaj hodnotu v metroch: "))
km, cm, mm = convert_units(meters)
print(f"{meters} metrov je {km} kilometrov, {cm} centimetrov a {mm} milimetrov.")
