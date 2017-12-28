import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from multiprocessing import Pool

MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
MONGO_DB = 'panjue'
MONGO_TABLE = 'shanghai_info'
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
def get():
    url = 'http://www.hshfy.sh.cn/shfy/gweb/flws_list_content.jsp'

    for i in range(1,1569):
        data = {'pagesnum': i}
        try:
            response = requests.post(url, data=data,proxies=proxies, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            all_tr = soup.find_all('tr')[1:]
            for tr in all_tr:
                info = {}
                info['title'] = tr.find_all('td')[1].get_text()
                info['date'] = tr.find_all('td')[-1].get_text()
                href = tr['onclick']
                text1 = href.split('(', 1)[1]
                text2 = 'http://www.hshfy.sh.cn/shfy/gweb/flws_view.jsp?pa=' + text1[1:-2]
                info['_id'] = text2
                try:
                    response2 = requests.get(text2, headers=headers, proxies=proxies, timeout=10)
                    soup2 = BeautifulSoup(response2.text, 'lxml')
                    info['body'] = soup2.find('div', id='wsTable').get_text()
                    if db[MONGO_TABLE].find_one(info['_id']):
                        print('已爬取')
                    else:
                        db[MONGO_TABLE].insert(dict(info))
                        print('插入成功')
                except Exception:
                    continue
        except Exception:
            continue

if __name__ == '__main__':
    pool = Pool()
    pool.apply_async(get)
    pool.close()
    pool.join()

