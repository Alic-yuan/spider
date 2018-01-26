import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient



MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
# MONGO_URL = 'localhost'
MONGO_DB = 'luntan'
MONGO_TABLE = 'gouwu_info'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

def get(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'lxml')
    all_tbody = soup.find('table',class_='list-data').find_all('tbody')
    for tbody in all_tbody:
        info = {}
        info['title'] = tbody.find('tr').find('th').find('a')['title']
        l = tbody.find('tr').find('th').find('a')['href']
        info['link'] = 'http:' + l
        info['author'] = tbody.find('tr').find('td',class_='author').find('a').get_text()
        info['time'] = tbody.find('tr').find('td',class_='author').find('span').get_text()
        info['replynum'] = tbody.find('tr').find('td',class_='num numeral').find('em').get_text()
        info['_id'] = info['link']
        if db[MONGO_TABLE].find_one(info['_id']):
            print('已爬取')
        else:
            db[MONGO_TABLE].insert(dict(info))
            print('插入成功')

def get_allurls():
    urls = []
    for i in range(1,21):
        url = 'http://go.cqmmgo.com/thread/lastest?page=' + str(i)
        urls.append(url)
    return urls


if __name__ == '__main__':
    urls = get_allurls()
    for url in urls:
        get(url)
