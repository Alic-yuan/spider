import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import datetime


MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
# MONGO_URL = 'localhost'
MONGO_DB = 'qianlima'
MONGO_TABLE = 'qianlima_info'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
           }
def get_date():
    days = []
    today = datetime.date.today()-datetime.timedelta(days=8)
    yestoday = datetime.date.today()-datetime.timedelta(days=30)
    # day = today.strftime('%Y%m%d')
    # day2 = yestoday.strftime('%Y%m%d')
    days.append(yestoday)
    days.append(today)
    return days

def parse():
    try:
        session = requests.session()

        url1 = 'http://center.qianlima.com/login_post.jsp'
        login_data = {'username': '18302381519',
                      'password': '381519'}

        session.post(url1, data=login_data, headers=headers,timeout=30)
        for i in range(1, 201):
            date = get_date()
            url = 'http://search.qianlima.com/qlm_adv_se.jsp?p={}&kw1=&kw2=&kw3=&field=0&p_tflt=999&q_time_start={}&q_time_end={}&prg=0%3D0&prg=0%3D2'.format(i, date[0], date[1])
            time.sleep(10)
            response = session.get(url, headers=headers,timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            all_div = soup.find_all('div',class_='five_line')
            for dl in all_div:
                item = {}
                a = dl.find('div',class_='two_line').find('a')['href']
                item['_id'] = a
                item['title'] = dl.find('div',class_='two_line').find('a')['title']
                item['area'] = dl.find('div', class_='three_line').get_text()
                item['date'] = dl.find('div',class_='four_line').get_text()
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
