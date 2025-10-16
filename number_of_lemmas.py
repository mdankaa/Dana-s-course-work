with open('tikhonov1.txt', 'r', encoding='utf-8') as f:
    tikhonov_lemmas = set(line.strip().lower() for line in f)
print(f"Загружено лемм из словаря Тихонова: {len(tikhonov_lemmas)}")
