import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from multiprocessing import Pool

MONGO_URL = ''
MONGO_DB = 'panjue'
MONGO_TABLE = 'beijing_info'
#
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

proxies = get_proxy()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }
def get_url():
    urls = []
    for i in range(1,44106):
        url = 'http://www.bjcourt.gov.cn/cpws/index.htm?st=1&q=&sxnflx=0&prompt=&dsrName=&ajmc=&ajlb=&jbfyId=&zscq=&ay=&ah=&cwslbmc=&startCprq=&endCprq=&page=' + str(i)
        urls.append(url)
    return urls

def parse(url):
    try:
        response = requests.get(url,headers=headers,proxies=proxies,timeout=10)
        soup = BeautifulSoup(response.text,'lxml')
        all_li = soup.find_all('li',class_='refushCpws')
        for li in all_li:
            a = li.find('a')['href']
            link = 'http://www.bjcourt.gov.cn' + a
            brower = webdriver.PhantomJS()
            brower.get(link)
            brower.implicitly_wait(3)
            info = {}
            try:
                info['_id'] = link
                info['title'] = brower.find_element_by_class_name('h3_22_m_blue').text
                info['date'] = brower.find_element_by_class_name('p_date').text
                info['body'] = brower.find_element_by_class_name('Section1').text
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
    for url in urls:
        parse(url)

