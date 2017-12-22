import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time


MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
MONGO_DB = 'qianlima'
MONGO_TABLE = 'qianlima_info'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
           }

def parse():
    try:
        session = requests.session()

        url1 = 'http://center.qianlima.com/login_post.jsp'
        login_data = {'username': '18302381519',
                      'password': '381519'}

        session.post(url1, data=login_data, headers=headers,timeout=30)
        for i in range(1, 201):
            url = 'http://www.qianlima.com/common/7day.jsp?crtPage=' + str(i)
            time.sleep(10)
            response = session.get(url, headers=headers,timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            all_dl = soup.find('div', class_='sevenday_list').find_all('dl')
            for dl in all_dl:
                item = {}
                a = dl.find_all('a')[1]['href']
                item['_id'] = a
                item['title'] = dl.find_all('a')[1].get_text()
                item['area'] = dl.find('span', class_='sevenday_diqu').get_text()
                item['date'] = dl.find('dd').get_text().replace('\xa0', '')
                try:
                    response2 = session.get(a, headers=headers,timeout=10)
                    time.sleep(10)
                    soup2 = BeautifulSoup(response2.text, 'lxml')
                    item['body'] = soup2.find('div', id='wen').get_text()
                except Exception:
                    continue
                print(item)
                if db[MONGO_TABLE].find_one(item['_id']):
                    print('已爬取')
                else:
                    db[MONGO_TABLE].insert(dict(item))
                    print('插入成功')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    parse()
