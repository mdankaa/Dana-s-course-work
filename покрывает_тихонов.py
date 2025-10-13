import json
from collections import Counter

# создаем множество с леммами из full_tikhonov.txt
with open('full_tikhonov.txt', 'r', encoding='utf-8') as f:
    tikhonov_lemmas = set()
    for line in f:
        line = line.strip()
        if line:
            parts = line.split('\t')
            if parts:
                lemma_only = parts[0].lower().strip()
                tikhonov_lemmas.add(lemma_only)
    #print(tikhonov_lemmas)

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
#print(covered_words)

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
