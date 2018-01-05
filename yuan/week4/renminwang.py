import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json



# MONGO_URL = 'localhost'
MONGO_DB = 'xinwen'
MONGO_TABLE = 'renminwang_info'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]

def get_proxy():

    # 代理服务器
    try:
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"

        # 代理隧道验证信息
        proxyUser = ""
        proxyPass = ""

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
        url = 'http://news.people.com.cn/210801/211150/index.js?_=1514863820516'
        response = requests.get(url, headers=headers,proxies=proxies,timeout=10)
        r = response.text
        result = json.loads(r)
        datas = result.get('items')
        for data in datas:
            info = {}
            href = data.get('url')
            info['_id'] = href
            info['title'] = data.get('title').replace('&nbsp','')
            info['date'] = data.get('date')
            try:
                response2 = requests.get(href,headers=headers,timeout=10)
                response2.encoding = 'gbk'
                soup = BeautifulSoup(response2.text,'lxml')
                info['body'] = soup.find('div', class_='box_con').get_text()
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




