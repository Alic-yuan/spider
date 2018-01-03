import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json


MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
# MONGO_URL = 'localhost'
MONGO_DB = 'xinwen'
MONGO_TABLE = 'yangshiwang_info'

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

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

proxies = get_proxy()

def get():
    try:
        url = 'http://news.cctv.com/data/index.json'
        response = requests.get(url, headers=headers,proxies=proxies,timeout=10)
        response.encoding = 'utf-8'
        r = response.text
        response2 = json.loads(r)
        datas = response2.get('rollData')
        for data in datas:
            info = {}
            href = data.get('url')
            info['_id'] = href
            info['title'] = data.get('title')
            info['date'] = data.get('dateTime')
            try:
                response3 = requests.get(href, headers=headers,timeout=10)
                response3.encoding = 'utf-8'
                soup = BeautifulSoup(response3.text, 'lxml')
                [script.extract() for script in soup.find_all('script')]
                # title = soup.find('h1',class_='dabiaoti').get_text()
                # date = soup.find('div',id='pubtime').get_text()
                all_p = soup.find('div', class_='cnt_bd').find_all('p')[1:]
                body = []
                for p in all_p:
                    body.append(p.get_text())
                info['body'] = body
            except Exception:
                continue
            print(info)
            if db[MONGO_TABLE].find_one(info['_id']):
                print('已爬取')
            else:
                db[MONGO_TABLE].insert(dict(info))
                print('插入成功')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    get()



