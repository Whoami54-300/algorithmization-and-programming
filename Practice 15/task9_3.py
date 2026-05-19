dictionary = {}

with open("en-ru.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        english, russian_part = line.split(" - ")

        russian_words = russian_part.split(", ")

        for russian in russian_words:
            if russian not in dictionary:
                dictionary[russian] = []

            dictionary[russian].append(english)

with open("ru-en.txt", "w", encoding="utf-8") as file:
    for russian in sorted(dictionary):
        english_words = ", ".join(dictionary[russian])
        file.write(russian + " - " + english_words + "\n")
