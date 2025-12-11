with open('multi_meaning_all_words.txt', 'r', encoding='utf-8') as f:
    words_to_remove = set(line.strip().lower() for line in f if line.strip())

with open('missing_common_nouns.txt', 'r', encoding='utf-8') as f:
    words_to_keep = []
    for line in f:
        word = line.strip()
        if word and word.lower() not in words_to_remove:
            words_to_keep.append(word)

# Сортируем слова в алфавитном порядке
words_to_keep.sort()

with open('final_file.txt', 'w', encoding='utf-8') as f:
    for word in words_to_keep:
        f.write(word + '\n')

print(f"Результат сохранен в final_file.txt")
print(f"Удалено слов: {len(words_to_remove)}")
print(f"Осталось слов: {len(words_to_keep)}")
