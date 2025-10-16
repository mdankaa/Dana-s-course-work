# Проверка наличия конкретных слов в словаре Тихонова (для вашего формата файла)
with open('tikhonov1.txt', 'r', encoding='utf-8') as f:
    tikhonov_lemmas = set()
    for line in f:
        line = line.strip()
        if line:
            parts = line.split('\t')
            if parts:
                # Берем только первое слово до табуляции
                lemma_only = parts[0].strip()
                tikhonov_lemmas.add(lemma_only.lower())

# Слова для проверки
words_to_check = ["свет", "мир", "кулак"]

print("Проверка наличия слов в словаре Тихонова:")
print("=" * 50)

for word in words_to_check:
    word_lower = word.lower()
    if word_lower in tikhonov_lemmas:
        print(f"✓ Слово '{word}' ЕСТЬ в словаре Тихонова")
    else:
        print(f"✗ Слово '{word}' ОТСУТСТВУЕТ в словаре Тихонова")

# Дополнительно: поиск точных вхождений (с учетом регистра)
print("\n" + "=" * 50)
print("Поиск точных вхождений в файле:")

with open('tikhonov1.txt', 'r', encoding='utf-8') as f:
    for word in words_to_check:
        f.seek(0)  # возвращаемся в начало файла
        found = False
        for line_num, line in enumerate(f, 1):
            if line.strip():
                first_word = line.split('\t')[0].strip()
                if first_word == word:
                    print(f"✓ Точное вхождение '{word}' найдено в строке {line_num}")
                    print(f"  Полная строка: {line.strip()}")
                    found = True
                    break
        if not found:
            print(f"✗ Точное вхождение '{word}' не найдено")

# Проверка всех форм слова
print("\n" + "=" * 50)
print("Поиск всех связанных форм в файле:")

for word in words_to_check:
    print(f"\nПоиск слов, связанных с '{word}':")
    with open('tikhonov1.txt', 'r', encoding='utf-8') as f:
        found_related = []
        for line in f:
            if line.strip():
                first_word = line.split('\t')[0].strip()
                # Ищем слова, которые начинаются с нашего слова (для разных форм)
                if first_word.lower().startswith(word.lower()):
                    found_related.append(line.strip())

        if found_related:
            print(f"Найдено {len(found_related)} связанных слов:")
            for related in found_related[:5]:  # покажем первые 5
                print(f"  {related}")
            if len(found_related) > 5:
                print(f"  ... и еще {len(found_related) - 5} слов")
        else:
            print(f"  Связанные слова не найдены")
