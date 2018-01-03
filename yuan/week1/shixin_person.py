import json
import requests
from pymongo import MongoClient
from multiprocessing import Pool





MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
MONGO_DB = 'shixin'
MONGO_TABLE = 'shixin_person'
#
client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]
#client = MongoClient('mongodb://admin:yjl123@42.123.126.65:27027/',connect=True)
# db = client[MONGO_DB]

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

headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Cookie':'BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID=66B73EA6BE7E6CF766CF15C1915E5C3D:FG=1; PSTM=1512985594; BIDUPSID=2D5367CBAEFDCC2DAB032BB5EAD54C80; H_PS_PSSID=1467_24565_21088_17001_25177_20929; PSINO=3',
    'Host':'sp0.baidu.com',
    'Referer':'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA&oq=%25E5%25A4%25B1%25E4%25BF%25A1%25E8%25A2%25AB%25E6%2589%25A7%25E8%25A1%258C%25E4%25BA%25BA&rsv_pq=b15531da000182b9&rsv_t=0789lhSro524u3niSiowcdVY5uE5hiS6KCmKTUEyOFJ0qV3B%2FBbNog0qVEU&rqlang=cn&rsv_enter=0&prefixsug=%25E5%25A4%25B1%25E4%25BF%25A1%25E8%25A2%25AB%25E6%2589%25A7%25E8%25A1%258C%25E4%25BA%25BA&rsp=0&rsv_sug=2',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }

proxies = get_proxy()

def get_person():
    try:
        for pn in range(10,10000,10):
            try:
                url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA&pn={}&rn=10&ie=utf-8&oe=utf-8&format=json&t=1513319802365&cb=jQuery110209542744866158159_1513318688870&_=1513318688945'.format(pn)
                response = requests.get(url,headers=headers,proxies=proxies)
                r = response.text
                text1 = r.split('(',1)[1]
                text2 = text1[:-2]
                #print(text2)

                # results1 = json.dumps(text2)
                results2 = json.loads(text2)
                #print(results2.get('status'))

                results3 = results2.get('data')[0].get('result')
                #print(results3)

                for result in results3:
                    info = {}
                    #info['siteid'] = result.get('SiteId')
                    info['_id'] = result.get('loc')
                    info['age'] = result.get('age')
                    info['areaName'] = result.get('areaName')
                    info['businessEnity'] = result.get('businessEntity')
                    info['cardNum'] = result.get('cardNum')
                    info['caseCode'] = result.get('caseCode')
                    info['changefreq'] = result.get('changefreq')
                    info['courtName'] = result.get('courtName')
                    info['disruptYypeName'] = result.get('disruptTypeName')
                    info['duty'] = result.get('duty')
                    info['focusNumber'] = result.get('focusNumber')
                    info['gistId'] = result.get('gistId')
                    info['gistUnit'] = result.get('gistUnit')
                    info['iname'] = result.get('iname')
                    info['lastmod'] = result.get('lastmod')
                    info['loc'] = result.get('loc')
                    info['partyTypeName'] = result.get('partyTypeName')
                    info['performance'] = result.get('performance')
                    info['performedPart'] = result.get('performedPart')
                    info['priority'] = result.get('priority')
                    info['publishDate'] = result.get('publishDate')
                    info['publishDateStamp'] = result.get('publishDateStamp')
                    info['regDate'] = result.get('regDate')
                    info['sexy'] = result.get('sexy')
                    info['sitelink'] = result.get('sitelink')
                    print(info)
                    if db[MONGO_TABLE].find_one(info['_id']):
                        print('已爬取')
                    else:
                        db[MONGO_TABLE].insert(dict(info))
                        print('插入成功')
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    get_person()






