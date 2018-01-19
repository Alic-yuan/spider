import json
import time
import requests
from pymongo import MongoClient
from scrapy.selector import Selector

MONGO_URL = 'localhost'
MONGO_DB = 'guojia'
MONGO_TABLE = 'data'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]

def getSession(url='http://data.stats.gov.cn/'):
    session = requests.Session()
    session.get(url)
    resp1 = session.get(
        'http://data.stats.gov.cn/adv.htm',
        params={'cn':'A01'},
        data={'cn':'A01'}
    )
    # resp2 = session.post(
    #     'http://data.stats.gov.cn/adv.htm',
    #     params={'m': 'advquery', 'cn': 'E0101'},
    #     data={'c': json.dumps([{"wd":"zb","zb":["A020101"],"name":["工业增加值_同比增长"]},{"wd":"reg","zb":["110000"],"name":[None]}])}
    # )
    resp3 = session.get(
        'http://data.stats.gov.cn/easyquery.htm',
        params={
            'm': 'QueryData',
            'dbcode': 'fsyd',
            'rowcode': 'reg',
            'colcode': 'sj',
            'wds': json.dumps([{"wdcode": "zb", "valuecode": "A020101"}]),
            'dfwds': json.dumps([{"wdcode": "sj", "valuecode": "last100000"}]),
            'k1': int(time.time()*1000)})
    print(json.dumps(resp3.json(), indent=4, ensure_ascii=False))

if __name__ == '__main__':
    getSession()