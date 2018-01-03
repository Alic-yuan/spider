import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from multiprocessing import Pool
import json
import datetime

MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
MONGO_DB = 'panjue'
MONGO_TABLE = 'zhejiang_info'
#
client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]
def get_proxy():

    # 代理服务器
    try:
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = "HA0BA166652L8P6D"
        proxyPass = "EDD43CF359807834"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
          "host" : proxyHost,
          "port" : proxyPort,
          "user" : proxyUser,
          "pass" : proxyPass,
        }

        proxies = {
            "http"  : proxyMeta,
            "https" : proxyMeta,
        }
        return proxies
    except Exception as e:
        print(e)

proxies = get_proxy()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }

def get_date():
    today = datetime.date.today()
    day = today.strftime('%Y%m%d')
    return day

def get():
    url = 'http://www.zjsfgkw.cn/document/JudgmentSearch'
    for i in range(1,40000):
        data = {'pageno': i,
                'pagesize': 10,
                'jarq1': 20070101,
                'jarq2': get_date()}
        try:
            response = requests.post(url, data=data, headers=headers,proxies=proxies,timeout=10)
            r = response.text
            result = json.loads(r)
            datas = result.get('list')
            for data in datas:
                id = data.get('DocumentId')
                link = 'http://www.zjsfgkw.cn/document/JudgmentDetail/' + str(id)
                parse(link)
        except Exception as e:
            print(e)


def parse(url):
    try:
        response = requests.get(url, headers=headers,proxies=proxies,timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            info = {}
            info['_id'] = url
            info['title'] = soup.find('div', class_='books_detail_header').find('h1').get_text()
            info['date'] = soup.find('div', class_='books_detail_header').find('h6').get_text()
            href = soup.find('div', class_='books_detail_content').find('iframe')['src']
            link = 'http://www.zjsfgkw.cn' + href
            response2 = requests.get(link, headers=headers,proxies=proxies,timeout=10)
            response2.encoding = 'utf-8'
            soup2 = BeautifulSoup(response2.text, 'lxml')
            info['body'] = soup2.find('div').get_text()
            if db[MONGO_TABLE].find_one(info['_id']):
                print('已爬取')
            else:
                db[MONGO_TABLE].insert(dict(info))
                print('插入成功')
        except Exception:
            pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    get()


