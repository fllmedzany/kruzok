# -*- coding: utf-8 -*-
import random
import re
import sys

# ---------- Nastavenia a frázy ----------

OPENERS = [
    "Ahoj! Čo ťa dnes najviac potešilo?",
    "Zdravím! Mal si dnes niečo zaujímavé?",
    "Môžeme pokecať? O čom chceš?",
    "Začnime zľahka: ako ide deň?",
    "Keby si mal voľný víkend, čo spravíš?",
    "Dnes je ideálny čas na nové nápady. Aké máš?",
    "Dal by si si radšej kávu alebo čaj?",
    "Poďme sa baviť o niečom príjemnom. Návrhy?",
    "Čo ťa naposledy prekvapilo?",
    "Akú hudbu teraz počúvaš najviac?",
    "Máš obľúbený film, ku ktorému sa vraciaš?",
    "Ak by si mohol cestovať kamkoľvek, kam pôjdeš?",
    "Čo bol tvoj malý úspech tohto týždňa?",
    "Čo si sa nedávno nové naučil?",
    "Akú knihu by si odporučil?",
    "Čo ťa vie spoľahlivo rozosmiať?",
    "Máš obľúbený šport alebo aktivitu?",
    "Ako vyzerá tvoj ideálny večer?",
    "Ktoré mesto by si rád spoznal?",
    "Čo ťa dnes najviac unavilo?"
]

QUESTION_REPLIES = [
    "Dobrá otázka!",
    "Prečo sa pýtaš?",
    "Znie to zaujímavo — čo si o tom myslíš ty?",
    "Skúsme na to pozrieť z inej strany.",
    "Môžeme to rozobrať. Čo je na tom pre teba dôležité?",
    "To stojí za diskusiu."
]

EXCLAMATION_REPLIES = [
    "Ou, znieš dosť energicky. Prečo kričíš?",
    "Intenzívne! Čo ťa k tomu viedlo?",
    "Cítim emócie. Povedz mi o tom viac."
]

NEUTRAL_FALLBACKS = [
    "Chápem. Povieš mi o tom trošku viac?",
    "Zaujímavé. Môžeš to rozvinúť?",
    "Jasné. Ako to vnímaš ty?",
    "Rozumiem. Čo by si chcel preskúmať ďalej?"
]

TOPICS = [
    "filmoch", "knihách", "cestovaní", "jedle", "športe",
    "technológiách", "hudbe", "prírode", "histórii", "hrách",
    "zvykoch", "zdraví", "záhradkárčení", "programovaní", "móde"
]

TOPIC_PROMPTS = {
    "filmoch": "Aký film ťa naposledy bavil?",
    "knihách": "Čítaš teraz niečo dobré?",
    "cestovaní": "Kam by si šiel najradšej?",
    "jedle": "Sladké alebo slané? Máš favorit?",
    "športe": "Sleduješ nejaký tím alebo hráča?",
    "technológiách": "Aký gadget by si chcel vyskúšať?",
    "hudbe": "Aká pieseň ti dnes hrá v hlave?",
    "prírode": "Máš obľúbenú túru alebo miesto?",
    "histórii": "Ktoré obdobie ťa fascinuje?",
    "hrách": "Aké hry hrávaš najradšej?",
    "zvykoch": "Máš nejaký ranný rituál?",
    "zdraví": "Ako si dobíjaš energiu?",
    "záhradkárčení": "Pestuješ niečo doma?",
    "programovaní": "Na čom teraz kódiš?",
    "móde": "Aký štýl ti je blízky?"
}

# Kľúčové slová → odpovede (náhodne sa vyberie jedna)
KEYWORD_RULES = {
    r"\bprečo\b": [
        "Výborná otázka. Čo je podľa teba príčina?",
        "Hmm, skúsme nájsť dôvod. Čo tipuješ?"
    ],
    r"\bako\b": [
        "Ako by si to spravil ty?",
        "Skús popísať postup, ktorý ti dáva zmysel."
    ],
    r"\bčo\b": [
        "Myslíš niečo konkrétne? Uveď príklad.",
        "Zúžme to — čo presne máš na mysli?"
    ],
    r"\bkedy\b": [
        "Má tvoja otázka nejaký termín?",
        "Záleží na kontexte. Kedy by sa ti to hodilo?"
    ],
    r"\bkde\b": [
        "Ktoré miesto preferuješ a prečo?",
        "Máš tip na lokalitu?"
    ],
    r"\bkto\b": [
        "Kto by bol podľa teba ideálna voľba?",
        "Koho by si oslovil ako prvého?"
    ],
    r"\bmožno\b|\basi\b": [
        "Znieš neist(o). Čo by ti pomohlo rozhodnúť sa?",
        "Poďme si spraviť plusy a mínusy."
    ],
    r"\b(super|skvel[ée]|\bpar[aá]da\b|\bfajn\b)": [
        "To rád počujem! Čo to spravilo super?",
        "Skvelé! Chceš na to nadviazať?"
    ],
    r"\b(zle|smutn[ýaé]|nuda|frustrovan[ýaé])\b": [
        "Mrzí ma to. Čo by to vedelo trochu zlepšiť?",
        "Chápem. Chceš sa z toho vypísať?"
    ],
    r"\b(díky|dakujem|ďakujem|vdaka|vďaka)\b": [
        "Rado sa stalo. Čím môžem pomôcť ďalej?",
        "Kedykoľvek. Máš ďalšiu tému?"
    ],
    r"\b(haha|lol|xd)\b": [
        "Som rád, že ťa to pobavilo 😄",
        "Humor je základ! Pokračujeme?"
    ]
}

EXIT_WORDS = {"koniec", "exit", "quit", "bye", "q", "dovidenia", "čaute", "cau", "čau"}

# ---------- Pomocné funkcie ----------

def pick(seq):
    return random.choice(seq)

def normalize(s: str) -> str:
    # jednoduchá normalizácia (lower + odstránenie extra medzier)
    return re.sub(r"\s+", " ", s.strip().lower())

def ends_with_question(s: str) -> bool:
    return s.rstrip().endswith("?")

def ends_with_exclaim(s: str) -> bool:
    return s.rstrip().endswith("!")

def match_keywords(s: str):
    for pat, replies in KEYWORD_RULES.items():
        if re.search(pat, s, flags=re.IGNORECASE):
            return pick(replies)
    return None

def switch_topic(current_topic=None):
    candidates = [t for t in TOPICS if t != current_topic] or TOPICS
    topic = random.choice(candidates)
    prompt = TOPIC_PROMPTS.get(topic, f"Poďme sa baviť o {topic}.")
    return topic, f"Bavme sa radšej o {topic}. {prompt}"

# ---------- Generátor odpovedí ----------

class State:
    def __init__(self):
        self.turns_without_progress = 0
        self.current_topic = None

def generate_reply(user_text: str, st: State) -> str:
    raw = user_text or ""
    txt = normalize(raw)

    if any(word in txt for word in EXIT_WORDS):
        return "OK, skončime tu. Kedykoľvek sa ozvi znova. 🙂"

    response_parts = []

    # Interpunkcia na konci
    if ends_with_question(raw):
        response_parts.append(pick(QUESTION_REPLIES))
    elif ends_with_exclaim(raw):
        response_parts.append(pick(EXCLAMATION_REPLIES))

    # Kľúčové slová
    kw = match_keywords(txt)
    if kw:
        response_parts.append(kw)

    # Ak sme nič nenašli, neutrálna reakcia
    if not response_parts:
        response_parts.append(pick(NEUTRAL_FALLBACKS))
        st.turns_without_progress += 1
    else:
        st.turns_without_progress = 0

    # Niekedy (alebo pri “záseku”) prepni tému
    want_switch = st.turns_without_progress >= 2 or random.random() < 0.15
    if want_switch:
        st.turns_without_progress = 0
        st.current_topic, switch_line = switch_topic(st.current_topic)
        response_parts.append(switch_line)

    # Jemné navádzanie, aby “viedol niť”
    nudges = [
        "Čo by si k tomu dodal?",
        "Ako to vidíš zo svojej skúsenosti?",
        "Daj príklad, nech sa chytím."
    ]
    # nepridávaj vždy, nech to nepôsobí umelo
    if random.random() < 0.35:
        response_parts.append(pick(nudges))

    return " ".join(response_parts)

# ---------- Hlavný loop ----------

def main():
    print("— Mini rozhovorový bot —")
    print("Napíš ‘koniec’ alebo ‘exit’ pre ukončenie.\n")
    print("Bot:", pick(OPENERS))

    state = State()

    while True:
        try:
            user = input("Ty: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Maj sa! 👋")
            break

        if not user:
            # prázdny vstup – skúsiť potiahnuť ďalej
            state.turns_without_progress += 1
            if state.turns_without_progress >= 2:
                state.turns_without_progress = 0
                state.current_topic, line = switch_topic(state.current_topic)
                print("Bot:", f"Nič? Nevadí. {line}")
            else:
                print("Bot:", "Som tu. Povedz čokoľvek, čo máš na mysli.")
            continue

        reply = generate_reply(user, state)
        print("Bot:", reply)

        # ukončenie ak používateľ explicitne chce
        if any(w in normalize(user) for w in EXIT_WORDS):
            break

if __name__ == "__main__":
    # Lepšia náhodnosť na dlhšie chaty
    random.seed()
    try:
        main()
    except Exception as e:
        print("Ups, niečo sa pokazilo:", e, file=sys.stderr)
        sys.exit(1)
