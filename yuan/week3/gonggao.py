import json
import requests
from pymongo import MongoClient
from multiprocessing import Pool





MONGO_URL = 'mongodb://admin:yjl123@42.123.126.65:27027/'
MONGO_DB = 'ktgg'
MONGO_TABLE = 'ktgg_info'
#
client = MongoClient(MONGO_URL,connect=True)
db = client[MONGO_DB]
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
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }

def get():
    try:
        for pn in range(1,9893):
            try:
                url = 'http://splcgk.court.gov.cn/gzfwww/ktgglist?pageNo=' + str(pn)
                data = {'pageNum': pn}
                response = requests.post(url,data=data, headers=headers, proxies=proxies,timeout=10)
                r = response.text
                result = json.loads(r)
                datas = result.get('data')
                for data in datas:
                    info = {}
                    info['_id'] = data.get('cBh')
                    info['cah'] = data.get('cah')
                    info['cajlb'] = data.get('cajlb')
                    info['cayBh'] = data.get('cayBh')
                    info['cbgMc'] = data.get('cbgMc')
                    info['ccbftBh'] = data.get('ccbftBh')
                    info['cfymc'] = data.get('cfymc')
                    info['cygMc'] = data.get('cygMc')
                    info['dtFbsj'] = data.get('dtFbsj')
                    info['ssxq'] = data.get('ssxq')
                    info['tnr'] = data.get('tnr')
                    print(info)
                    if db[MONGO_TABLE].find_one(info['_id']):
                        print('已爬取')
                    else:
                        db[MONGO_TABLE].insert(dict(info))
                        print('插入成功')
            except Exception:
                continue
    except Exception as e:
        print(e)


if __name__ == '__main__':
    get()