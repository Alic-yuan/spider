import requests
from pymongo import MongoClient
import json
import copy

MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
# MONGO_URL = 'localhost'
MONGO_DB = 'tjj_GJ'
MONGO_TABLE = 'zycsyd_data'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]


headers = {'Cookie':'_trs_uv=jciqyg2x_6_s1q; JSESSIONID=7E9292C73BC76461A15F6078B8695175; u=1',
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
        code1 = node1.get('nodes')[0].get('code')
        node3 = wds[1]
        place = node3.get('nodes')[0].get('cname')
        code2 = node3.get('nodes')[0].get('code')
        node2 = wds[2]
        dates = node2.get('nodes')
        list2 = []
        for d in dates:
            date = d.get('name')
            list2.append(date)
        info = {}
        info['_id'] = code2 + '_' + code1
        info['place'] = place
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
valcodes = []
def TreeLevel1(initDict, follow=True):
    res1 = requests.post(
        url='http://data.stats.gov.cn/adv.htm',
        headers=headers,
        data=initDict,
    )
    for record in res1.json():
        try:
            valuecode1 = record['id']
            valcodes.append(valuecode1)
            if follow == True:
                TreeLevel1(getNewDict(initDict, {'treeId': record['id']}), record['isParent'])
        except:
            continue
    return valcodes

ids = []
def TreeLevel2(initDict, follow=True):
    res1 = requests.post(
        url='http://data.stats.gov.cn/adv.htm',
        headers=headers,
        data=initDict,
    )
    for record in res1.json():
        try:
            valuecode1 = record['id']
            ids.append(valuecode1)
            if follow == True:
                TreeLevel2(getNewDict(initDict, {'treeId': record['id']}), record['isParent'])
        except:
            continue
    return ids

def getNewDict(initDict, addDict):
    result = copy.deepcopy(initDict)
    result.update(addDict)
    return result

if __name__ == '__main__':
    url = 'http://data.stats.gov.cn/easyquery.htm?'
    place = TreeLevel1({'db': 'csyd', 'wd': 'reg', 'm': 'findZbXl'})
    places = set(place)
    tids = TreeLevel2({'db': 'csyd', 'wd': 'zb', 'm': 'findZbXl'})
    for place in places:
        for id in tids:
            a = '[{"wdcode":"reg","valuecode":"%s"}]' % place
            b = '[{"wdcode":"zb","valuecode":"%s"}]' % id
            data = {'m': 'QueryData', 'dbcode': 'csyd', 'rowcode': 'zb', 'colcode': 'sj',
                    'wds': a,
                    'dfwds': b}
            get(url,data)