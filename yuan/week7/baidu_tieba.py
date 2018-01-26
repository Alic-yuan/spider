import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
import datetime

MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
# MONGO_URL = 'localhost'
MONGO_DB = 'luntan'
MONGO_TABLE = 'tieba_info'
#
client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

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
def get_html(url):
    try:
        r = requests.get(url,proxies=proxies,timeout=30)
        r.raise_for_status()
        # 这里我们知道百度贴吧的编码是utf-8，所以手动设置的。爬去其他的页面时建议使用：
        # r.endcodding = r.apparent_endconding
        r.encoding = 'utf-8'
        return r.text
    except:
        return " ERROR "

def get_allurls():
    allurls = []
    url = 'http://tieba.baidu.com/f/index/forumclass'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    all_clearfix = soup.find_all('div', class_='clearfix')
    for clearfix in all_clearfix:
        all_classitem = clearfix.find_all('div', class_='class-item')
        for classitem in all_classitem:
            all_li = classitem.find('ul').find_all('li')
            for li in all_li:
                h = li.find('a')['href']
                href = 'http://tieba.baidu.com' + h
                allurls.append(href)
    return allurls

def parse_urls(url):
    try:
        links = []
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        max_page = soup.find('div', class_='pagination').find_all('a')[-1]['href'].split('pn=')[1]
        for i in range(1, int(max_page) + 1):
            link = url + '&st=new&pn=' + str(i)
            links.append(link)
        return links
    except Exception as e:
        print(e)

def get_tiebaurl(url):
    try:
        hrefs = []
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        all_div = soup.find('div', class_='ba_list clearfix').find_all('div', class_='ba_info')
        for div in all_div:
            a = div.find('a', rel='noopener')['href']
            href = 'http://tieba.baidu.com' + a
            hrefs.append(href)
        return hrefs
    except Exception as e:
        print(e)

def get_pageurl(url):
    try:
        pages = []
        response = get_html(url)
        soup = BeautifulSoup(response,'lxml')
        max_page = soup.find('div',id='frs_list_pager').find_all('a')[-1]['href'].split('pn=')[1]
        for i in range(int(max_page)//50+1):
            link = url + '&ie=utf-8&pn=' + str(int(i)*50)
            pages.append(link)
        return pages
    except Exception as e:
        print(e)

def detail(url):
    try:
        html = get_html(url)

        soup = BeautifulSoup(html, 'lxml')

        tieba = soup.find('div',class_='card_title').find('a').get_text('','\n')

        liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})

        for li in liTags:
            comment = {}
            try:
                comment['tieba'] = tieba
                comment['title'] = li.find(
                    'a', attrs={'class': 'j_th_tit '}).text.strip()
                comment['link'] = "http://tieba.baidu.com/" + \
                                  li.find('a', attrs={'class': 'j_th_tit '})['href']
                comment['name'] = li.find(
                    'span', attrs={'class': 'tb_icon_author '}).text.strip()
                time = li.find('span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
                comment['replyNum'] = li.find(
                    'span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
                comment['_id'] = comment['link']
                if ':' in time:
                    time = datetime.date.today().strftime('%m-%d')
                comment['time'] = time
                if db[MONGO_TABLE].find_one(comment['_id']):
                    print('已爬取')
                else:
                    db[MONGO_TABLE].insert(dict(comment))
                    print('插入成功')
            except:
                print('出了点小问题')
    except Exception as e:
        print(e)

def work(urls):
    links = parse_urls(urls)
    for link in links:
        hrefs = get_tiebaurl(link)
        for href in hrefs:
            pages = get_pageurl(href)
            for page in pages:
                detail(page)



def main():
    all_urls = get_allurls()
    pool = ThreadPoolExecutor(max_workers=10)
    for urls in all_urls:
        pool.submit(work,urls)


if __name__ == '__main__':
    main()




