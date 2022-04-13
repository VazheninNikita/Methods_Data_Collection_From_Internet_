from lxml import html
import requests
from pprint import pprint
import datetime
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news_db']
news_yandex = db.news_yandex

# news_yandex.delete_many({})

def write_to_db(news, news_db):
    if news_yandex.find_one({'link': news['link']}):
        print(f'Dublicated news {news["link"]}')
    else:
        news_yandex.insert_one(news)
        print(f'Success insert the link {news["link"]}')

url = 'https://yandex.ru/news'
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

response = requests.get(url, headers=header)

dom = html.fromstring(response.text)

news_list = dom.xpath("//div[contains(@class, 'mg-card mg-card')]")
news = []

for o_news in news_list:
    news_info = {}
    name = o_news.xpath(".//h2[@class='mg-card__title']//text()")
    link = o_news.xpath(".//h2[@class='mg-card__title']/a/@href")
    source = o_news.xpath(".//span[@class='mg-card-source__source']//text()")
    date_news = o_news.xpath(".//span[@class='mg-card-source__time']/text()")

    news_info['_id'] = link[0]
    news_info['name'] = name[0].replace('\xa0',' ')
    news_info['link'] = link[0]
    news_info['source'] = source[0]
    news_info['date_news'] = str(datetime.datetime.now().strftime("%d-%m-%Y")) + ' ' + date_news[0]

    news.append(news_info)
    write_to_db(news_info, news_yandex)

result = list(news_yandex.find({}))
pprint(result)
pprint(f'Кол-во новостей в базе {len(result)}')

