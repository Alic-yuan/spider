import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor


# MONGO_URL = 'localhost'
MONGO_DB = 'luntan'
MONGO_TABLE = 'tianya_info'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}


def get(url):
    try:
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text,'lxml')
        all_tr = soup.find('table',class_='tab-bbs-list tab-bbs-list-2').find('tbody').find_all('tr')
        for tr in all_tr:
            try:
                l = tr.find('td',class_='td-title faceblue').find('a')['href']
                link = 'http://groups.tianya.cn' + l
                parse(link)
            except:
                continue
    except Exception as e:
        print(e)

def parse(url):
    try:
        info = {}
        info['_id'] = url
        if db[MONGO_TABLE].find_one(info['_id']):
            print('已爬取')
        else:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            info['title'] = soup.find('span',class_='s_title').get_text('','\n')
            info['link'] = url
            info['author'] = soup.find('div',class_='atl-info').find('span').find('a').get_text()
            info['time'] = soup.find('div',class_='atl-info').find_all('span')[1].get_text('','\t').split('时间：')[1]
            info['replynum'] = soup.find('div',class_='atl-info').find_all('span')[-1].get_text('','\t').split('回复：')[1]
            info['text'] = soup.find('div',class_='bbs-content clearfix').get_text('','\t')
            db[MONGO_TABLE].insert(dict(info))
            print('插入成功')
    except Exception as e:
        print(e)


def get_allurls():
    urls = []
    for i in range(1,51):
        url = 'http://groups.tianya.cn/group_home.jsp?itemId=163879&orderType=1&searchType=1&tabNum=2&t=0&classId=0&curPageNo=' + str(i)
        urls.append(url)
    return urls


if __name__ == '__main__':
    all_url = get_allurls()
    pool = ThreadPoolExecutor(max_workers=10)
    for url in all_url:
        pool.submit(get,url)




