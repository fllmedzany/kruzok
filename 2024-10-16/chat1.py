
from openai import OpenAI

# Nastavte váš API kľúč
client = OpenAI(api_key='')

# Funkcia na odoslanie otázky a získanie odpovede
def chat_with_gpt(prompt1):
    completion = client.chat.completions.create(
        
        model="gpt-4o-mini",  # Môžete použiť aj iný model, napr. "gpt-4",
          messages=[
            {"role": "system", "content": "Rozpravaj sa so mnou po slovensky!"},
            {"role": "user", "content": prompt1}
          ]
#        prompt=prompt1
#        messages=[
#            {"role": "system", "content": "You are a helpful assistant."},
#            {"role": "user", "content": prompt}
#        ]
    )
    return completion.choices[0].message.content.strip()


# Príklad použitia funkcie
otazka = "Co vies o meste Ulcin?"
odpoved = chat_with_gpt(otazka)
print("Odpoveď:", odpoved)

