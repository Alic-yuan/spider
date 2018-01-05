import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from multiprocessing import Pool
import time
import random


MONGO_URL = ''
MONGO_DB = 'zhaobiao'
MONGO_TABLE = 'zhaobiao_info'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
           }


def get_data():
    userids = ['alicu','alicy','alicyuan','lansha','shayuan','shayuansha','yuansha','yuanshayuan']
    login_data = {}
    login_data['userid'] = userids[random.randint(0,7)]
    login_data['pwd'] = 'yuan19960404'
    return login_data



def get_url():
    urls = []
    for i in range(1,500):
            url = 'http://www.bidchance.com/search.do?currentpage=' + str(i) + '&province=&channel=freegg&queryword=&searchtype=zb&bidfile=&recommend=&leftday=&searchyear=&field=all&displayStyle=title&attachment=&starttime=&endtime=&pstate='
            urls.append(url)
    return urls

def parse(url):
    try:
        session = requests.session()

        url1 = 'http://www.bidchance.com/logon.do'
        session.post(url1, data=get_data(), headers=headers, timeout=30)
        time.sleep(10)
        response = session.get(url,headers=headers,timeout=10)
        soup = BeautifulSoup(response.text,'lxml')
        all_tr = soup.find_all('tr',class_='datatr')
        for tr in all_tr:
                item = {}
                a = tr.find('a')['href']
                item['_id'] = a
                item['title'] = tr.find('a').get_text()
                item['area'] = tr.find_all('td')[-2].get_text()
                item['date'] = tr.find_all('td')[-1].get_text()
                try:
                    session2 = requests.session()
                    session2.post(url1, data=get_data(), headers=headers, timeout=30)
                    time.sleep(10)
                    response2 = session2.get(a,headers=headers,timeout=10)
                    soup = BeautifulSoup(response2.text,'lxml')
                    item['body'] = soup.find('dd',id='infohtmlcon').get_text()
                except Exception:
                    continue
                if db[MONGO_TABLE].find_one(item['_id']):
                        print('已爬取')
                else:
                    db[MONGO_TABLE].insert(dict(item))
                    print('插入成功')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    urls = get_url()
    for url in urls:
        parse(url)




