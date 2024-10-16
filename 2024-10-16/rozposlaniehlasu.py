import speech_recognition as sr
import turtle

"""
instalacia:
    pip install SpeechRecognition
    pip install pyaudio
    pip install setuptools

"""

# Vytvorenie inštancie rozpoznávača
recognizer = sr.Recognizer()

t = turtle.Turtle()
t.pd()
t.speed(30)
# Nastavenie mikrofónu ako zdroja zvuku
with sr.Microphone() as source:
    print("Nastavujem šum okolia... Počkaj chvíľu predtým, ako začneš hovoriť.")
    recognizer.adjust_for_ambient_noise(source, duration=1)  # Prispôsobenie na šum okolia

    while True:    
        print("Povedz niečo...")
        audio = recognizer.listen(source,  timeout=5, phrase_time_limit=2)

        try:
            # Použitie Google Speech Recognition na konverziu
            text = recognizer.recognize_google(audio, language="sk-SK")
            #text = recognizer.recognize_sphinx(audio, language="en-US")
            print("Rozpoznaný text: " + text)
            
            # Rozpoznanie a reakcia na špecifické príkazy
            if text.lower() == "dopredu":
                print("Pohybujem sa dopredu")
                t.fd(50)
            elif text.lower() == "vľavo":
                print("Obraciam sa vľavo")
                t.lt(90)
            elif text.lower() == "vpravo":
                print("Obraciam sa vpravo")
                t.rt(90)
            elif text.lower() == "stoj":
                print("Zastavujem")
            elif text.lower() == "koniec":
                print("Koniec")
                break
            else:
                print("Neznámy príkaz")
        except sr.UnknownValueError:
            print("Google Speech Recognition nerozpoznal zvuk.")
        except sr.RequestError as e:
            print("Nepodarilo sa dostať služby Google Speech Recognition; {0}".format(e))
            

