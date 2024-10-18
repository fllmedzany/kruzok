from gtts import gTTS
import pygame
import io

# Inicializácia pygame pre prehrávanie zvuku
pygame.mixer.init()

# Text, ktorý chcete prečítať
text = "Ahoj, toto je príklad hlasovej syntézy v slovenčine."

# Vytvorenie objektu pre slovenčinu s Google Text-to-Speech
tts = gTTS(text=text, lang='sk')

# Uloženie do pamäte namiesto do súboru pomocou BytesIO
mp3_fp = io.BytesIO()
tts.write_to_fp(mp3_fp)

# Presunieme pozíciu na začiatok streamu
mp3_fp.seek(0)

# Načítanie zvuku z pamäte pomocou pygame
pygame.mixer.music.load(mp3_fp, 'mp3')
pygame.mixer.music.play()

# Čakanie na dokončenie prehrávania
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

