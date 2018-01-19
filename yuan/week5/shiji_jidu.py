import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json
from concurrent.futures import ThreadPoolExecutor
import copy



MONGO_URL = 'localhost'
MONGO_DB = 'shiji_shuju'
MONGO_TABLE = 'jidu_data'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]


headers = {
'Cookie':'JSESSIONID=SyvhhfHVxYhS3h1208FnlRhljvMBht1xf2hkN55hyfcYXmj8T9SS!-933055557',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}


def get(url,data):
    try:
        response = requests.post(url, headers=headers, data=data,timeout=10)
        response.encoding = 'utf-8'
        r = response.text
        response2 = json.loads(r)
        datas = response2.get('returndata').get('datanodes')
        shujus = []
        for data in datas:
            shuju = data.get('data').get('strdata')
            shujus.append(shuju)
        wds = response2.get('returndata').get('wdnodes')
        node1 = wds[0]
        title = node1.get('nodes')[0].get('cname')
        code = node1.get('nodes')[0].get('code')
        node2 = wds[1]
        dates = node2.get('nodes')
        list2 = []
        for d in dates:
            date = d.get('name')
            list2.append(date)
        info = {}
        info['_id'] = code
        info['title'] = title
        if db[MONGO_TABLE].find_one(info['_id']):
            print('已爬取')
        else:
            for a in range(len(shujus)):
                info[list2[a]] = shujus[a]
            print(info)
            db[MONGO_TABLE].insert(dict(info))
            print('插入成功')
    except Exception as e:
        print(e)

def TreeLevel(initDict, follow=True):
    res1 = requests.post(
        url='http://www.cqdata.gov.cn/adv.htm',
        headers=headers,
        data=initDict,
    )
    for record in res1.json():
        url = 'http://www.cqdata.gov.cn/easyquery.htm?'
        valuecode = record['id']
        print(valuecode)
        a = '[{"wdcode":"zb","valuecode":"%s"}]' % valuecode
        data = {'m': 'QueryData', 'dbcode': 'hgjd', 'rowcode': 'zb', 'colcode': 'sj', 'wds': '[]',
                'dfwds': a}
        get(url, data)
        if follow == True:
            TreeLevel(getNewDict(initDict, {'treeId': record['id']}), record['isParent'])

def getNewDict(initDict, addDict):
    result = copy.deepcopy(initDict)
    result.update(addDict)
    return result

if __name__ == '__main__':
    TreeLevel({'db': 'hgjd', 'wd': 'zb', 'm': 'findZbXl'})
