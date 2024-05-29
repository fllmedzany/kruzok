def count_vowels(text):
    vowels = 'aeiou'
    count = 0
    for char in text:
        if char.lower() in vowels:
            count += 1
    return count

text = input("Zadaj text: ")
vowel_count = count_vowels(text)
print(f"Počet samohlások v texte: {vowel_count}")
