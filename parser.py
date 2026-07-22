import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = 'https://habr.com/ru/articles/'

def debug_parse_habr(url, keywords):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
   
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
       
        articles = soup.find_all('article', class_='tm-articles-list__item')
       
        print(f"Всего статей на странице: {len(articles)}\n")
        print("="*80)
       
        found_articles = []
       
        for idx, article in enumerate(articles[:10], 1):  # Проверим первые 10
            # Заголовок
            title_elem = article.find('h2', class_='tm-title tm-title_h2')
            if not title_elem:
                continue
            title = title_elem.get_text(strip=True)
           
            # Ссылка
            link_elem = title_elem.find('a')
            link = 'https://habr.com' + link_elem.get('href') if link_elem else 'Нет ссылки'
           
            # Дата
            time_elem = article.find('time')
            date_str = time_elem.get_text(strip=True) if time_elem else 'Дата не указана'
           
            # Превью
            preview_text = ''
            content_elem = article.find('div', class_='tm-article-body')
            if content_elem:
                preview_text = content_elem.get_text(strip=True)[:200]
           
            # Проверяем ключевые слова
            found_words = []
            full_text = (title + ' ' + preview_text).lower()
            for keyword in keywords:
                if keyword.lower() in full_text:
                    found_words.append(keyword)
           
            print(f"{idx}. {date_str}")
            print(f"   Заголовок: {title}")
            print(f"   Найдены слова: {', '.join(found_words) if found_words else 'НЕТ'}")
            print(f"   Ссылка: {link}")
            if preview_text:
                print(f"   Превью: {preview_text[:150]}...")
            print("-"*80)
           
            if found_words:
                found_articles.append({
                    'date': date_str,
                    'title': title,
                    'link': link,
                    'keywords': found_words,
                    'preview': preview_text
                })
       
        print(f"\n✅ ИТОГО: Найдено {len(found_articles)} статей с ключевыми словами:")
        for article in found_articles:
            print(f"   {article['date']} – {article['title']} – {article['link']}")
            print(f"   Ключевые слова: {', '.join(article['keywords'])}")
            print()
       
        return found_articles
       
    except Exception as e:
        print(f'Ошибка: {e}')
        return []

if __name__ == '__main__':
    print("🔍 Отладка парсера Хабра\n")
    debug_parse_habr(URL, KEYWORDS)