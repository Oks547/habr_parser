import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# URL страницы со свежими статьями
URL = 'https://habr.com/ru/articles/'

def parse_habr_articles(url, keywords):
    """
    Парсит свежие статьи с Хабра и выводит те, которые содержат ключевые слова
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
       
        # Находим ВСЕ статьи на странице (без ограничений!)
        articles = soup.find_all('article', class_='tm-articles-list__item')
       
        found_articles = []
       
        # Перебираем все статьи 
        for article in articles:
            # Извлекаем заголовок
            title_elem = article.find('h2', class_='tm-title tm-title_h2')
            if not title_elem:
                continue
               
            title = title_elem.get_text(strip=True)
           
            # Извлекаем ссылку
            link_elem = title_elem.find('a')
            if not link_elem:
                continue
            link = 'https://habr.com' + link_elem.get('href')
           
            # Извлекаем дату
            time_elem = article.find('time')
            date_str = 'Дата не указана'
            if time_elem:
                date = time_elem.get('datetime', '')
                try:
                    date_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
                    date_str = date_obj.strftime('%Y-%m-%d %H:%M')
                except:
                    date_str = time_elem.get_text(strip=True)
           
            # Извлекаем превью-текст
            preview_text = ''
            content_elem = article.find('div', class_='tm-article-body tm-article-snippet__lead')
            if content_elem:
                preview_text = content_elem.get_text(strip=True)
           
            # Проверяем наличие ключевых слов (в заголовке ИЛИ в превью)
            full_text = (title + ' ' + preview_text).lower()
            for keyword in keywords:
                if keyword.lower() in full_text:
                    found_articles.append({
                        'date': date_str,
                        'title': title,
                        'link': link
                    })
                    break  # Добавляем статью только один раз
       
        return found_articles
       
    except requests.RequestException as e:
        print(f'Ошибка при запросе: {e}')
        return []
    except Exception as e:
        print(f'Ошибка при парсинге: {e}')
        return []

# Запуск
if __name__ == '__main__':
    print('=' * 80)
    print(f'Поиск статей с ключевыми словами: {", ".join(KEYWORDS)}')
    print('=' * 80)
   
    articles = parse_habr_articles(URL, KEYWORDS)
   
    if articles:
        print(f'\n✅ Найдено {len(articles)} статей:\n')
        for article in articles:
            print(f"{article['date']} – {article['title']} – {article['link']}")
        print()
    else:
        print('\n❌ Статей с указанными ключевыми словами не найдено.\n')