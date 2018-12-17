from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    response = requests.get(url)
    return response.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        tds = soup.find('div', class_='main__col-list').find_all('div', class_='main-feed__item js-main-reload-item')
    except:
        tds = ''
    links = []
    link = soup.find('div', class_='main__col-main__inner').find('a').get('href')
    links.append(link)

    for td in tds:
        link = td.find('a').get('href')
        links.append(link)

    return links


def data_write(data):
    with open('rbk.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(('\nЗаголовок', data['title'], '\nСсылка', data['link'], '\nНовость', data['content'], '\nДата',
                         data['date']))


def get_data_main(html, link):
    soup = BeautifulSoup(html, 'lxml')

    title = soup.find('div', class_='article__header__title').find('span', class_='js-slide-title').text.strip()
    content = soup.find('div', class_='article__text__overview').text.strip()
    date = soup.find('div', class_='article__header__info-block').find('span',
                                                                           class_='article__header__date').text.strip()
    data = {'title': title, 'link': link, 'content': content, 'date': date}
    return data


def main():
    url = 'https://www.rbc.ru/'
    all_links = get_all_links(get_html(url))
    for link in all_links:
        data = get_data_main(get_html(link), link)
        data_write(data)


if __name__ == '__main__':
    main()
