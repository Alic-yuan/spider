import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json
from concurrent.futures import ThreadPoolExecutor


MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
# MONGO_URL = 'localhost'
MONGO_DB = 'diqu_shuju'
MONGO_TABLE = 'data'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]



headers = { 'Cookie':'JSESSIONID=w91dhVxh6DNdSrjnCMWL0sl0s0hSRgYYNrydK9HBWhhnyQk9jcxL!5596160',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}


def get(url):
    try:
        response = requests.get(url, headers=headers,timeout=10)
        response.encoding = 'utf-8'
        r = response.text
        response2 = json.loads(r)
        # print(response2)
        datas = response2.get('returndata').get('datanodes')
        shujus = []
        for data in datas:
            shuju = data.get('data').get('strdata')
            shujus.append(shuju)
        wds = response2.get('returndata').get('wdnodes')
        node1 = wds[0]
        titles = node1.get('nodes')
        list1 = []
        list3 = []
        for t in titles:
            title = t.get('name')
            code = t.get('code')
            list1.append(title)
            list3.append(code)
        node2 = wds[1]
        areas = node2.get('nodes')
        list2 = []
        for a in areas:
            area = a.get('name')
            list2.append(area)

        node3 = wds[2]
        date = node3.get('nodes')
        for d in date:
            time = d.get('name')
        try:
            for a in range(len(list1)):
                info = {}
                info['_id'] = list3[a] + time
                info['time'] = time
                info['title'] = list1[a]
                i = a * 46
                info[list2[0]] = shujus[i]
                info[list2[1]] = shujus[i + 1]
                info[list2[2]] = shujus[i + 2]
                info[list2[3]] = shujus[i + 3]
                info[list2[4]] = shujus[i + 4]
                info[list2[5]] = shujus[i + 5]
                info[list2[6]] = shujus[i + 6]
                info[list2[7]] = shujus[i + 7]
                info[list2[8]] = shujus[i + 8]
                info[list2[9]] = shujus[i + 9]
                info[list2[10]] = shujus[i + 10]
                info[list2[11]] = shujus[i + 11]
                info[list2[12]] = shujus[i + 12]
                info[list2[13]] = shujus[i + 13]
                info[list2[14]] = shujus[i + 14]
                info[list2[15]] = shujus[i + 15]
                info[list2[16]] = shujus[i + 16]
                info[list2[17]] = shujus[i + 17]
                info[list2[18]] = shujus[i + 18]
                info[list2[19]] = shujus[i + 19]
                info[list2[20]] = shujus[i + 20]
                info[list2[21]] = shujus[i + 21]
                info[list2[22]] = shujus[i + 22]
                info[list2[23]] = shujus[i + 23]
                info[list2[24]] = shujus[i + 24]
                info[list2[25]] = shujus[i + 25]
                info[list2[26]] = shujus[i + 26]
                info[list2[27]] = shujus[i + 27]
                info[list2[28]] = shujus[i + 28]
                info[list2[29]] = shujus[i + 29]
                info[list2[30]] = shujus[i + 30]
                info[list2[31]] = shujus[i + 31]
                info[list2[32]] = shujus[i + 32]
                info[list2[33]] = shujus[i + 33]
                info[list2[34]] = shujus[i + 34]
                info[list2[35]] = shujus[i + 35]
                info[list2[36]] = shujus[i + 36]
                info[list2[37]] = shujus[i + 37]
                info[list2[38]] = shujus[i + 38]
                info[list2[39]] = shujus[i + 39]
                info[list2[40]] = shujus[i + 40]
                info[list2[41]] = shujus[i + 41]
                info[list2[42]] = shujus[i + 42]
                info[list2[43]] = shujus[i + 43]
                info[list2[44]] = shujus[i + 44]
                info[list2[45]] = shujus[i + 45]
                print(info)
                if db[MONGO_TABLE].find_one(info['_id']):
                    print('已爬取')
                else:
                    db[MONGO_TABLE].insert(dict(info))
                    print('插入成功')
        except Exception:
            pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    urls = ['http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A01%22%7D%5D&k1=1515571123055',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A02%22%7D%5D&k1=1515571134473',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A03%22%7D%5D&k1=1515571144031',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A04%22%7D%5D&k1=1515571152240',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A05%22%7D%5D&k1=1515571161512',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0601%22%7D%5D&k1=1515571171912',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0602%22%7D%5D&k1=1515571180472',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0603%22%7D%5D&k1=1515571190928',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A07%22%7D%5D&k1=1515571199280',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A08%22%7D%5D&k1=1515571207671',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A09%22%7D%5D&k1=1515571216231',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0A%22%7D%5D&k1=1515571224624',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0B%22%7D%5D&k1=1515571233905',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0C%22%7D%5D&k1=1515571242081',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0D%22%7D%5D&k1=1515571250424',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0E%22%7D%5D&k1=1515571257984',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0F%22%7D%5D&k1=1515571266498',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0G%22%7D%5D&k1=1515571274928',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0H%22%7D%5D&k1=1515571283072',
            'http://www.cqdata.gov.cn/easyquery.htm?m=QueryData&dbcode=qxnd&rowcode=reg&colcode=zb&wds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%222015%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0I%22%7D%5D&k1=1515571291225'
            ]
    for url in urls:
        get(url)