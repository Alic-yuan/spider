import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
# MONGO_URL = 'localhost'
MONGO_DB = 'xinwen'
MONGO_TABLE = 'ribaowang_info'

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

def get_urls():
    try:
        urls = ['https://cn.chinadaily.com.cn/node_53002614.htm']
        for i in range(2, 11):
            url = 'https://cn.chinadaily.com.cn/node_53002614_{}.htm'.format(i)
            urls.append(url)
        return urls
    except Exception as e:
        print(e)

def parse(url):
    try:
        response = requests.get(url, headers=headers,timeout=10)
        response.encoding = 'utf-8'
        # print(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        all_div = soup.find_all('div', class_='busBox1')
        for div in all_div:
            info = {}
            href = div.find('a')['href']
            info['_id'] = href
            try:
                response2 = requests.get(href, headers=headers,timeout=10)
                response2.encoding = 'utf-8'
                soup2 = BeautifulSoup(response2.text, 'lxml')
                info['title'] = soup2.find('h1', class_='dabiaoti').get_text()
                info['date'] = soup2.find('div', id='pubtime').get_text()
                info['body'] = soup2.find('div', id='Content').get_text()
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
    urls = get_urls()
    for url in urls:
        parse(url)