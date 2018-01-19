import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver

# MONGO_URL = 'localhost'
MONGO_DB = 'pochai_info'
MONGO_TABLE = 'pochai_qiye'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }


def download(url):
    info = {}
    info['_id'] = url
    if db[MONGO_TABLE].find_one(info['_id']):
        print('已爬取')
    else:
        brower = webdriver.PhantomJS()
        brower.get(url)
        brower.implicitly_wait(3)
        html = brower.page_source
        # print(html)
        soup = BeautifulSoup(html, 'lxml')
        info['title'] = soup.find('div', class_='fd-brief-top').get_text()
        value = soup.find('input', id='ajbh')['value']
        # print(info)
        all_li = soup.find('ul',class_='fd-asset-menu').find_all('li')
        l2 = []
        for li in all_li:
            l = []
            name = li.find('a').get_text()
            l.append(name)
            text = li['onclick'][4:]
            text1 = text.split('(')[0].lower()
            link = 'http://pccz.court.gov.cn/pcajxxw/pczwr/' + text1
            # print(link)
            num = text.split('(')[1].split(')')[0]
            data = {'ajbh':value,'wsgglx':num}
            response = requests.post(link,headers=headers,data=data)
            soup2 = BeautifulSoup(response.text,'lxml')
            all_div = soup2.find_all('div',class_='fd-item-wsgg clear')
            for div in all_div:
                title = div.find('a')['title']
                href = 'http://pccz.court.gov.cn/pcajxxw/' + div.find('a')['href']
                c = title + '-' +href
                l.append(c)
            l2.append(l)
        info['neirong'] = l2
        print(info)
        db[MONGO_TABLE].insert(dict(info))
        print('插入成功')



def get():
    url = 'http://pccz.court.gov.cn/pcajxxw/pctzr/tzrlb'
    for i in range(1,1068):
        data = {'pageNum': i}
        response = requests.post(url, headers=headers, data=data, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        all_div1 = soup.find_all('div', class_='fd-tab-region')
        for div in all_div1:
            a = div.find('a')['href']
            link = 'http://pccz.court.gov.cn/pcajxxw/' + a
            download(link)



if __name__ == '__main__':
    get()
