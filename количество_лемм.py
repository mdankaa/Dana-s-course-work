with open('full_tikhonov.txt', 'r', encoding='utf-8') as f:
    tikhonov_lemmas = set(line.strip().lower() for line in f)
print(f"Загружено лемм из словаря Тихонова: {len(tikhonov_lemmas)}")
