import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from multiprocessing import Pool

MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
MONGO_DB = 'panjue'
MONGO_TABLE = 'qinghai_info'
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

def get_url():
    urls = []
    for i in range(1, 1964):
        url = 'http://www.qhcourt.gov.cn:8080/susong51/fymh/3900/cpws.htm?st=0&ssmzyy=&bhxjy=&q=&ajlb=&wszl=&jbfy=&ay=&ah=&startCprq=&endCprq=&startFbrq=&endFbrq=&page=' + str(i)
        urls.append(url)
    return urls

def parse(url):
    try:
        response = requests.get(url,headers=headers,proxies=proxies,timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        all_tr = soup.find_all('tr', class_='tr_stripe')
        for tr in all_tr:
            href = tr.find_all('td')[1]['onclick']
            href1 = href.split('(', 1)[1].split(')')[0]
            href2 = href1[1:-1]
            link = 'http://www.qhcourt.gov.cn:8080/susong51/cpws/paperView.htm?wsTypeSign=undefined&id=' + href2
            brower = webdriver.PhantomJS()
            brower.get(link)
            brower.implicitly_wait(3)
            info = {}
            try:
                info['_id'] = link
                info['title'] = brower.find_element_by_class_name('ws_title').text
                info['date'] = brower.find_element_by_class_name('ws_time').find_element_by_tag_name('span').text
                info['body'] = brower.find_element_by_class_name('doc_area').text
                if db[MONGO_TABLE].find_one(info['_id']):
                    print('已爬取')
                else:
                    db[MONGO_TABLE].insert(dict(info))
                    print('插入成功')
            except Exception:
                continue
    except Exception as e:
        print(e)

if __name__ == '__main__':
    urls = get_url()
    pool = Pool()
    pool.map(parse,urls)
    pool.close()
    pool.join()