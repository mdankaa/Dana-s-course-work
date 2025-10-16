import json
from collections import Counter

# создаем множество с леммами из full_tikhonov.txt
with open('tikhonov1.txt', 'r', encoding='utf-8') as f:
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

# Топ-100 самых частотных имен существительных среди непокрытых слов
noun_frequencies = []
for lemma, info_list in missing_words.items():
    for info in info_list:
        if info['pos'] == 'S':
            total_count = sum(info['count'] for info_dict in missing_words[lemma]
                            if info_dict['pos'] == 'S')
            noun_frequencies.append((lemma, total_count))
            break

# избавление от дубликатов и сортировка по частоте
noun_frequencies = list(set(noun_frequencies))
noun_frequencies.sort(key=lambda x: x[1], reverse=True)

# Функция для проверки, является ли слово именем собственным (топонимом, именем, фамилией, отчеством)
def is_proper_noun(lemma):
    if lemma not in missing_words:
        return False

    # Проверяем только первое значение
    if missing_words[lemma]:
        first_gr = missing_words[lemma][0].get('gr', '')
        return any(marker in first_gr for marker in ['topon', 'famn', 'persn', 'patrn'])

    return False

# Функция для получения типа имени собственного
def get_proper_noun_type(lemma):
    if lemma not in missing_words or not missing_words[lemma]:
        return None

    first_gr = missing_words[lemma][0].get('gr', '')
    types = []

    if 'topon' in first_gr:
        types.append('topon')
    if 'famn' in first_gr:
        types.append('famn')
    if 'persn' in first_gr:
        types.append('persn')
    if 'patrn' in first_gr:
        types.append('patrn')

    return types if types else None

# Фильтруем топ-100 существительных на две группы
filtered_nouns = []
proper_nouns = []

for lemma, freq in noun_frequencies[:100]:
    if is_proper_noun(lemma):
        proper_nouns.append((lemma, freq))
    else:
        filtered_nouns.append((lemma, freq))

with open('missing_words.txt', 'w', encoding='utf-8') as f:
    for word in sorted(missing_words.keys()):
        f.write(word + '\n')

print(f"Всего лемм: {len(corpus_data)}")
print(f"Покрыто словарём Тихонова: {len(covered_words)}")
print(f"Не покрыто словарём Тихонова: {len(missing_words)}")
print(f"Распределение непокрытых слов по частям речи:")
for pos, count in pos_counter.most_common():
    print(f"  {pos}: {count}")
print(f"10 самых частотных непокрытых слов:")
for i, (lemma, freq) in enumerate(word_frequencies[:10]):
    print(f"  {i+1}. {lemma} ({freq})")

print(f"\nТоп-100 непокрытых существительных:")
print(f"Имен собственных: {len(proper_nouns)}")
print(f"Обычных существительных: {len(filtered_nouns)}")

print(f"\nВсе обычные существительные из топ-100 (без имен собственных):")
for i, (lemma, freq) in enumerate(filtered_nouns):
    print(f"  {i+1}. {lemma} ({freq})")

print(f"\nВсе имена собственные из топ-100:")
for i, (lemma, freq) in enumerate(proper_nouns):
    proper_types = get_proper_noun_type(lemma)
    type_names = {
        'topon': 'топоним',
        'famn': 'фамилия',
        'persn': 'имя',
        'patrn': 'отчество'
    }
    type_descriptions = [type_names.get(t, t) for t in proper_types] if proper_types else ['неизвестный тип']
    print(f"  {i+1}. {lemma} ({freq}) - {', '.join(type_descriptions)}")
