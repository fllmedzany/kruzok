def quiz():
    questions = [
        {
            "question": "Aké je hlavné mesto Slovenska?",
            "choices": ["a) Bratislava", "b) Košice", "c) Žilina", "d) Prešov"],
            "answer": "a"
        },
        {
            "question": "Koľko je 2 + 2?",
            "choices": ["a) 3", "b) 4", "c) 5", "d) 6"],
            "answer": "b"
        }
    ]
    score = 0

    for q in questions:
        print(q["question"])
        for choice in q["choices"]:
            print(choice)
        answer = input("Tvoja odpoveď: ")
        if answer.lower() == q["answer"]:
            score += 1

    print(f"Tvoj výsledok je {score} z {len(questions)}.")

quiz()
