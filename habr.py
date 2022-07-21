import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def find_articles(link, keywords):
    soup = BeautifulSoup(link, features="html.parser")
    articles = soup.findAll('article')
    for article in articles:
        body = article.find('div', class_="tm-article-body tm-article-snippet__lead")
        headers = article.find('h2', class_="tm-article-snippet__title tm-article-snippet__title_h2")
        date_and_time = article.find('span', class_="tm-article-snippet__datetime-published")
        hubs = article.find_all(class_='tm-article-snippet__hubs-item')
        hubs = set(hub.text.strip().lower() for hub in hubs)
        article_set = set(body.text.strip().split(" "))

        if set(keywords) & hubs:
            print(f'В хабах: {set(keywords) & hubs}')
            for element in date_and_time:
                print(element.get('title'))
            for header in headers:
                print(header.text)
                print('https://habr.com' + header.get('href'))

        elif set(keywords) & article_set:
            print(f'В превью: {set(keywords) & article_set}')
            for element in date_and_time:
                print(element.get('title'))
            for title in headers:
                print(title.text)
                print('https://habr.com' + title.get('href'))


if __name__ == '__main__':
    HEADERS = Headers(
        browser='chrome',
        os='win',
        headers=True
                     ).generate()
    DATA_URL = 'https://habr.com/ru/all'
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    SOURCE = requests.get(DATA_URL, headers=HEADERS).text
    find_articles(SOURCE, KEYWORDS)
