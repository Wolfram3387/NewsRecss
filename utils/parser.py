import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse

from utils.neural_networks.get_keywords import get_keywords
from utils.db_api.api import get_all_news, add_news

df = pd.DataFrame(columns=['ID', 'Keywords', 'Link', 'Title', 'Text'])
get_new_news_count = 0

def extract_info_from_url(url):
    domain = urlparse(url).netloc

    if domain == 'lenta.ru':

        article_page = requests.get(url)
        article_soup = BeautifulSoup(article_page.text, 'html.parser')

        title = article_soup.find('span', class_='topic-body__title').text.strip()
        # time = article_soup.find('a', class_='topic-header__time').text.strip()
        # abstract = article_soup.find('span', class_='topic-body__title').text.strip()
        text = ' '.join([p.text.strip() for p in article_soup.find_all('p', class_='topic-body__content-text')])

        return {'Title': title, 'Text': text}

    elif domain == 'moslenta.ru':

        article_page = requests.get(url)
        article_soup = BeautifulSoup(article_page.text, 'html.parser')

        title = article_soup.find('h1', class_='jsx-3552357312 Cqvs5c42').text.strip()
        # time = article_soup.find('div', class_='qzByRHub P5lPq1qA').text.strip()
        # abstract = article_soup.find('p', class_='jsx-4260339384').text.strip()
        text = ' '.join([p.text.strip() for p in article_soup.find_all('p', class_='jsx-2193584331')])

        return {'Title': title, 'Text': text}


def parse_news(limit=20):
    global df, news_counter

    if len(df) > 20:
        df = df.head(20)

    page = requests.get('https://lenta.ru/parts/news')
    soup = BeautifulSoup(page.text, 'html.parser')

    news_items = soup.find_all('li', class_='parts-page__item')

    for item in news_items[:limit]:

        link = item.find('a', class_='_parts-news')['href']
        full_url = link if link.startswith('http') else urljoin('https://lenta.ru', link)

        domain = urlparse(full_url).netloc

        # Проверяем домен и извлекаем информацию
        if domain == 'lenta.ru':
            article_info = extract_info_from_url(full_url)
        elif domain == 'moslenta.ru':
            article_info = extract_info_from_url(full_url)
        else:
            continue

        article_info['ID'] = str(hash(full_url.strip()))

        df = pd.concat([df, pd.DataFrame({'Link': [full_url], **article_info})], ignore_index=True)

        df = df.drop_duplicates(subset='Title', keep='first')

        # text = df['Title'] + ' ' + df['Text']
        # keywords = get_keywords(text)
        # df.at[df.index[-1], 'Keywords'] = keywords

    df['Keywords'] = df.apply(lambda row: get_keywords(pd.Series([row['Title'] + ' ' + row['Text']])), axis=1)

    return df


def get_new_news():
    global get_new_news_count
    pd.set_option('display.max_columns', 3)


    df = parse_news().drop(columns=['Title'])

    previous_df = pd.DataFrame(get_all_news(), columns=['ID', 'Keywords', 'Link', 'Text'])

    if get_new_news_count == 0:
        add_news(df)
        get_new_news_count +=1
        return df.head(3)

    if previous_df.empty:
        add_news(df)
        return df.iloc[[0, -1]]

    common_ids = set(df['ID']).intersection(set(previous_df['ID']))

    new_df = df[~df['ID'].isin(common_ids)]

    add_news(new_df)
    return new_df
