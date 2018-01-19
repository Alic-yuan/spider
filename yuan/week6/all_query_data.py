import requests

from pymongo import MongoClient
import json
import copy
# MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
MONGO_URL = 'localhost'
MONGO_DB = 'guojia_shuju'
MONGO_TABLE = 'yuedu_data'

client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}


def TreeLevel(initDict, follow=True):
    res1 = requests.post(
        url='http://data.stats.gov.cn/adv.htm',
        headers=headers,
        data=initDict,
    )
    for record in res1.json():
        record['_id'] = record['id']
        db[initDict['wd'] + '_' + initDict['db']].update_one(
            {'_id': record['_id']},
            {'$set': record},
            upsert=True,
        )
        print(json.dumps(record, indent=4, ensure_ascii=False))
        if follow == True:
            TreeLevel(getNewDict(initDict, {'treeId': record['id']}), record['isParent'])

def getNewDict(initDict, addDict):
    result = copy.deepcopy(initDict)
    result.update(addDict)
    return result

TreeLevel({'db': 'hgyd', 'wd': 'zb','m': 'findZbXl'}) # 月度数据
TreeLevel({'db': 'hgjd', 'wd': 'zb','m': 'findZbXl'}) # 季度数据
TreeLevel({'db': 'hgnd', 'wd': 'zb','m': 'findZbXl'}) # 年度数据
TreeLevel({'db': 'fsyd', 'wd': 'zb','m': 'findZbXl'}) # 分省月度数据
TreeLevel({'db': 'fsyd', 'wd': 'reg','m': 'findZbXl'}) # 分省月度数据-地区
TreeLevel({'db': 'fsjd', 'wd': 'zb','m': 'findZbXl'}) # 分省季度数据
TreeLevel({'db': 'fsjd', 'wd': 'reg','m': 'findZbXl'}) # 分省季度数据-地区
TreeLevel({'db': 'fsnd', 'wd': 'zb','m': 'findZbXl'}) # 分省年度数据
TreeLevel({'db': 'fsnd', 'wd': 'reg','m': 'findZbXl'}) # 分省年度数据-地区
TreeLevel({'db': 'csyd', 'wd': 'zb','m': 'findZbXl'}) # 主要城市月度价格
TreeLevel({'db': 'csyd', 'wd': 'reg','m': 'findZbXl'}) # 主要城市月度价格
TreeLevel({'db': 'csnd', 'wd': 'zb','m': 'findZbXl'}) # 主要城市年度数据
TreeLevel({'db': 'csnd', 'wd': 'reg','m': 'findZbXl'}) # 主要城市月度价格