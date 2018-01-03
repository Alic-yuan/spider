import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
# MONGO_URL = 'localhost'
MONGO_DB = 'xinwen'
MONGO_TABLE = 'xinhuawang_info'

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
        url = 'http://www.xinhuanet.com/linktous.htm'
        response = requests.get(url, headers=headers,proxies=proxies,timeout=10)
        response.encoding = 'utf-8'
        response2 = etree.HTML(response.text)
        all_tr = response2.xpath('/html/body/div/table[8]/tbody/tr/td[3]/table[1]/tbody/tr/td/table/tbody/tr')[1:-1]
        urls = []
        for tr in all_tr:
            link = tr.xpath('./td[3]/a/text()')[0]
            urls.append(link)
        return urls
    except Exception as e:
        print(e)

def parse(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'xml')
        all_item = soup.find_all('item')
        for item in all_item:
            info = {}
            link = item.find('link').get_text()
            try:
                response2 = requests.get(link, headers=headers,timeout=10)
                response2.encoding = 'utf-8'
                soup2 = BeautifulSoup(response2.text, 'lxml')
                all_p = soup2.find('div', id='p-detail').find_all('p')
                body = []
                for p in all_p:
                    body.append(p.text)
                info['_id'] = link
                info['title'] = soup2.find('div',class_='h-title').get_text()
                info['date'] = soup2.find('span',class_='h-time').get_text()
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
    urls = get_urls()
    pool = ThreadPoolExecutor(max_workers=10)
    for url in urls:
        pool.submit(parse,url)