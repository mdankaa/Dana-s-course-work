import json
from collections import Counter

# создаем множество с леммами из tikhonov_final.txt
with open('tikhonov_final.txt', 'r', encoding='utf-8') as f:
    tikhonov_lemmas = set()
    for line in f:
        line = line.strip()
        if line:
            parts = line.split('\t')
            if parts:
                lemma_only = parts[0].lower().strip()
                tikhonov_lemmas.add(lemma_only)

with open('learner_corpus_lemmas.json', 'r', encoding='utf-8') as f:
    corpus_data = json.load(f)

# делим слова на покрытые и непокрытые
missing_words = {}
covered_words = {}

for lemma, info_list in corpus_data.items():
    if lemma.lower() in tikhonov_lemmas:
        covered_words[lemma] = info_list
    else:
        missing_words[lemma] = info_list

# части речи непокрытых слов
pos_counter = Counter()
for lemma, info_list in missing_words.items():
    for info in info_list:
        pos = info['pos']
        pos_counter[pos] += 1

# непокрытые слова: слово + частота
word_frequencies = []
for lemma, info_list in missing_words.items():
    total_count = sum(info['count'] for info in info_list)
    word_frequencies.append((lemma, total_count))
word_frequencies.sort(key=lambda x: x[1], reverse=True)

# Функция для проверки, является ли слово именем собственным (топонимом, именем, фамилией, отчеством)
def is_proper_noun(gr_string):
    if not gr_string:
        return False
    return any(marker in gr_string for marker in ['topon', 'famn', 'persn', 'patrn'])

# Собираем ВСЕ непокрытые нарицательные существительные (исключая имена собственные)
common_nouns_all = []
proper_nouns_filtered = []  # для информации об отфильтрованных именах

for lemma, info_list in missing_words.items():
    is_proper = False

    # Проверяем, является ли лемма именем собственным в каком-либо из вариантов
    for info in info_list:
        if info['pos'] == 'S':
            gr = info.get('gr', '')
            if is_proper_noun(gr):
                is_proper = True
                proper_nouns_filtered.append((lemma, gr))
                break

    # Если не имя собственное, но есть существительные среди вариантов
    if not is_proper:
        has_noun = False
        noun_count = 0

        for info in info_list:
            if info['pos'] == 'S':
                has_noun = True
                noun_count += info['count']

        if has_noun:
            common_nouns_all.append((lemma, noun_count))

# Сортируем по частоте
common_nouns_all.sort(key=lambda x: x[1], reverse=True)

# Топ-100 самых частотных нарицательных существительных
top_100_nouns = common_nouns_all[:100]

# Сохраняем в файл ВСЕ непокрытые нарицательные существительные (только слова)
with open('missing_common_nouns.txt', 'w', encoding='utf-8') as f:
    for lemma, freq in common_nouns_all:
        f.write(f"{lemma}\n")

# Создаем файл с топ-100 (только слова)
with open('top100_missing_common_nouns.txt', 'w', encoding='utf-8') as f:
    for lemma, freq in top_100_nouns:
        f.write(f"{lemma}\n")

# Для информации: файл с отфильтрованными именами собственными (только слова)
with open('filtered_proper_nouns.txt', 'w', encoding='utf-8') as f:
    for lemma, gr in proper_nouns_filtered:
        f.write(f"{lemma}\n")

# Также создаем файл со всеми непокрытыми словами (только слова)
with open('missing_words.txt', 'w', encoding='utf-8') as f:
    for lemma, freq in word_frequencies:
        f.write(f"{lemma}\n")

# Для справки: создаем отдельный файл со статистикой
with open('statistics.txt', 'w', encoding='utf-8') as f:
    f.write(f"Всего лемм: {len(corpus_data)}\n")
    f.write(f"Покрыто словарём Тихонова: {len(covered_words)}\n")
    f.write(f"Не покрыто словарём Тихонова: {len(missing_words)}\n")
    f.write(f"Нарицательных существительных среди непокрытых: {len(common_nouns_all)}\n")
    f.write(f"Отфильтровано имен собственных: {len(proper_nouns_filtered)}\n")
    f.write(f"\nРаспределение непокрытых слов по частям речи:\n")
    for pos, count in pos_counter.most_common():
        f.write(f"  {pos}: {count}\n")

print(f"Всего лемм: {len(corpus_data)}")
print(f"Покрыто словарём Тихонова: {len(covered_words)}")
print(f"Не покрыто словарём Тихонова: {len(missing_words)}")
print(f"Нарицательных существительных среди непокрытых: {len(common_nouns_all)}")
print(f"Отфильтровано имен собственных: {len(proper_nouns_filtered)}")
print(f"\nРаспределение непокрытых слов по частям речи:")
for pos, count in pos_counter.most_common():
    print(f"  {pos}: {count}")

print(f"\n10 самых частотных непокрытых слов:")
for i, (lemma, freq) in enumerate(word_frequencies[:10]):
    print(f"  {i+1}. {lemma} ({freq})")

print(f"\n10 самых частотных непокрытых нарицательных существительных:")
for i, (lemma, freq) in enumerate(common_nouns_all[:10]):
    print(f"  {i+1}. {lemma} ({freq})")

print(f"\nСозданы файлы (только списки слов):")
print(f"  - missing_words.txt - все непокрытые слова ({len(missing_words)} слов)")
print(f"  - missing_common_nouns.txt - все непокрытые нарицательные существительные ({len(common_nouns_all)} слов)")
print(f"  - top100_missing_common_nouns.txt - топ-100 самых частотных нарицательных существительных")
print(f"  - filtered_proper_nouns.txt - список отфильтрованных имен собственных ({len(proper_nouns_filtered)} слов)")
print(f"  - statistics.txt - статистика и распределение по частям речи")
