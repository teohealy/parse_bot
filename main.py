import requests
from bs4 import BeautifulSoup
import json


def get_first_news():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    url = 'https://news.drom.ru/'
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    article_blocks = soup.find_all('div', class_="b-info-block b-info-block_like-text b-info-block_width_215")

    news_dict = {}

    for article in article_blocks:
        article_title = article.find('div', class_='b-info-block__title b-link')
        if article_title is None:
            article_title_text = 'NoType'
        else:
            article_title_text = article_title.text.strip()

        article_url_title = article.find("a", {"class": "b-info-block__cont b-info-block__cont_state_reviews"})
        if article_url_title is None:
            continue
        article_url = 'https://news.drom.ru/' + article_url_title.get('href')

        article_date = article.find('div', class_='b-info-block__text b-info-block__text_type_news-date').text.strip()

        article_id = article_url.split('/')[-1]
        article_id = article_id[:-5]

        news_dict[article_id] = {
            "article_date": article_date,
            "article_title": article_title_text,
            "article_url": article_url
        }

        #print(f'{article_title_text} | {article_id} | {article_url} | {article_date}')
    with open('news_dict.json', 'w') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open('news_dict.json') as file:
        news_dict = json.load(file)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    url = 'https://news.drom.ru/'
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    article_blocks = soup.find_all('div', class_="b-info-block b-info-block_like-text b-info-block_width_215")

    fresh_news = {}

    for article in article_blocks:
        article_url_title = article.find("a", {"class": "b-info-block__cont b-info-block__cont_state_reviews"})
        if article_url_title is None:
            continue
        article_url = 'https://news.drom.ru/' + article_url_title.get('href')
        article_id = article_url.split('/')[-1]
        article_id = article_id[:-5]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find('div', class_='b-info-block__title b-link')
            if article_title is None:
                article_title_text = 'NoType'
            else:
                article_title_text = article_title.text.strip()
            article_date = article.find('div', class_='b-info-block__text b-info-block__text_type_news-date').text.strip()

            news_dict[article_id] = {
                "article_date": article_date,
                "article_title": article_title_text,
                "article_url": article_url
            }

            fresh_news[article_id] = {
                "article_date": article_date,
                "article_title": article_title_text,
                "article_url": article_url
            }

    with open('news_dict.json', 'w') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    #get_first_news()
    print(check_news_update())


if __name__ == '__main__':
    main()
