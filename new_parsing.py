import requests
from bs4 import BeautifulSoup
import re
import time

def get_all_dictionary_pages():
    base_url = "https://www.slovorod.ru/der-tikhonov/"
    pages = [
        "tih-a.htm", "tih-b.htm", "tih-v.htm", "tih-g.htm", "tih-d.htm", "tih-zh.htm",
        "tih-z.htm", "tih-i.htm", "tih-j.htm", "tih-k.htm", "tih-l.htm", "tih-m.htm",
        "tih-n.htm", "tih-o.htm", "tih-p.htm", "tih-r.htm", "tih-s.htm", "tih-t.htm",
        "tih-u.htm", "tih-f.htm", "tih-h.htm", "tih-c.htm", "tih-ch.htm", "tih-sh.htm",
        "tih-sch.htm", "tih-e.htm", "tih-ju.htm", "tih-ja.htm"
    ]
    full_urls = [base_url + page for page in pages]
    return full_urls

def parse_page(url, page_name):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = soup.get_text()
        pattern = re.compile(r'\b([а-яёА-ЯЁ-]+?)(\d+)(?=\W|$)', re.IGNORECASE)
        matches = pattern.findall(all_text)
        found_words = []
        for word_base, number in matches:
            if re.search(r'[а-яё]', word_base, re.IGNORECASE):
                full_word = f"{word_base}{number}"
                found_words.append(full_word)
        return found_words
    except:
        return []

def parse_all_dictionary():
    urls = get_all_dictionary_pages()
    all_words_with_numbers = []
    for url in urls:
        page_name = url.split('/')[-1]
        words = parse_page(url, page_name)
        all_words_with_numbers.extend(words)
        time.sleep(0.5)

    word_groups = {}
    for word in all_words_with_numbers:
        match = re.match(r'([а-яёА-ЯЁ-]+?)\d+$', word, re.IGNORECASE)
        if match:
            base_form = match.group(1).lower()
            if base_form not in word_groups:
                word_groups[base_form] = []
            word_groups[base_form].append(word)

    multi_meaning_words = []
    detailed_groups = {}
    for base_form, variants in word_groups.items():
        if len(variants) > 1:
            unique_variants = sorted(set(variants))
            multi_meaning_words.extend(unique_variants)
            detailed_groups[base_form] = unique_variants

    multi_meaning_words = sorted(set(multi_meaning_words))
    return multi_meaning_words, detailed_groups

def remove_numbers_from_word(word):
    cleaned_word = re.sub(r'\d+$', '', word)
    return cleaned_word

def save_results(multi_meaning_words, detailed_groups):
    unique_words_without_numbers = set()
    for word in multi_meaning_words:
        cleaned_word = remove_numbers_from_word(word)
        unique_words_without_numbers.add(cleaned_word)

    unique_words_sorted = sorted(unique_words_without_numbers)

    with open('multi_meaning_all_words.txt', 'w', encoding='utf-8') as f:
        for word in unique_words_sorted:
            f.write(word + "\n")

def main():
    multi_meaning_words, detailed_groups = parse_all_dictionary()
    save_results(multi_meaning_words, detailed_groups)

if __name__ == "__main__":
    main()
