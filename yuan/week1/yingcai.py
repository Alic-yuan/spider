import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from multiprocessing import Pool
import time
import random
import datetime
from concurrent.futures import ThreadPoolExecutor


# MONGO_URL = 'localhost'
MONGO_DB = 'yingcai'
MONGO_TABLE = 'yingcai_job2'

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

def occupation():
    try:
        url = "http://www.chinahr.com/jobs/"
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        ds = soup.find_all('div', class_='item-class')

        list = []

        for h in ds:
            all_a = h.find('div',class_='detail-class').find_all('a')
            for a in all_a:
                href = a['href']
                list.append(href)

        return list
    except Exception as e:
        print(e)

def get_message(href):
    try:

        response = requests.get(href,headers=headers)
        soup = BeautifulSoup(response.text,'lxml')
        try:
            pages = soup.find('div',class_='pageList').find_all('a')[-2].get_text()
        except Exception as e:
            print(e)
        for i in range(1,int(pages)+1):
            time.sleep(random.random() * 5)
            url = href + str(i) + '/'
            print('开始爬取第'+str(i)+'页')
            download(url)
    except Exception as e:
        print(e)


def download(url):
    try:
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        companies = soup.find_all('div', class_='jobList')
        for company in companies:
                positionName = company.find('li', class_='l1').find('span', class_='e1').get_text()
                formatCreateTime = company.find('li', class_='l1').find('span', class_='e2').get_text()
                if formatCreateTime == '今天':
                    formatCreateTime = datetime.date.today().strftime('%Y%m%d')
                elif formatCreateTime == '昨天':
                    formatCreateTime = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
                companyFullName = company.find('li', class_='l1').find('span', class_='e3').find('a').get_text()
                city_and_workYear = company.find('li', class_='l2').find('span', class_='e1').get_text()
                salary = company.find('li', class_='l2').find('span', class_='e2').get_text()
                companySize = company.find('li', class_='l2').find('span', class_='e3').em.get_text()
                href = company['data-url']
                info1 = companyFullName
                info2 = city_and_workYear
                info3 = positionName
                fo = []
                fo.append(formatCreateTime)
                info4 = fo
                info5 = salary
                info6 = companySize
                info7 = href
                response2 = requests.get(href,proxies=proxies,headers=headers)
                soup2 = BeautifulSoup(response2.text,'lxml')
                positiondetail = soup2.find('div',class_='job_intro_info').get_text('\n','br/')
                companydetail = soup2.find('div',class_='company_service').get_text()
                fulis = soup2.find('div',class_='job_fit_tags').find('ul',class_='clear').find_all('li')
                list = []
                for fuli in fulis:
                    list.append(fuli.get_text())
                info10 = list
                info8 = positiondetail
                info9 = companydetail
                if db[MONGO_TABLE].find_one({'_id':info7}):
                    db[MONGO_TABLE].update_one({'_id': info7}, {"$addToSet": {'发布时间': formatCreateTime}},
                                               upsert=True)
                    print('更新成功')
                else:
                    db[MONGO_TABLE].insert({'_id':info7,'公司名字': info1,'公司详细介绍':info9, '公司城市和年限': info2, '招聘职位': info3,'职位要求':info8, '发布时间': info4,
                                     '薪资待遇': info5, '福利':info10,'公司大小': info6,'网址':info7})
                    print('插入成功')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    occu_list = occupation()
    pool = ThreadPoolExecutor(max_workers=10)
    for i in occu_list:
        pool.submit(get_message,i)











