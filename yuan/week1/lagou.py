import json

import requests
from pymongo import MongoClient
from lxml import etree
from multiprocessing import Pool
import datetime
from concurrent.futures import ThreadPoolExecutor



MONGO_URL = 'localhost'
MONGO_DB = 'lagou2'
MONGO_TABLE = 'lagou_job2'

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


headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'23',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'JSESSIONID=ABAAABAAAIAACBIC3716278BA5AFF7895FBDDC0E8C4B902; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512979725; _ga=GA1.2.1354609368.1512979725; _gid=GA1.2.666920385.1512979725; user_trace_token=20171211160846-83033e41-de4a-11e7-8ecc-525400f775ce; LGSID=20171211160846-83034002-de4a-11e7-8ecc-525400f775ce; PRE_UTM=; PRE_HOST=link.zhihu.com; PRE_SITE=http%3A%2F%2Flink.zhihu.com%2F%3Ftarget%3Dhttps%253A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20171211160846-830341a1-de4a-11e7-8ecc-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_navigation; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512981168; LGRID=20171211163248-de9c1786-de4d-11e7-9cc5-5254005c3644; SEARCH_ID=852d545d038a495db857fdbd3683914c',
    'Host':'www.lagou.com',
    'Origin':'https://www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_Java?px=default&city=%E5%8C%97%E4%BA%AC',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'X-Anit-Forge-Code':'0',
    'X-Anit-Forge-Token':'None',
    'X-Requested-With':'XMLHttpRequest'
           }
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    }

proxies = get_proxy()



def get_html():
    try:
        url = "https://www.lagou.com/"
        html = requests.get(url,headers=header,timeout=10)
        return html.text
    except:
        pass


def parse(html):
    # url = "https://www.lagou.com/"
    # html = requests.get(url,headers=header,proxies=proxies)
    # response = etree.HTML(html.text)
    # 获取所有职位
    try:
        response = etree.HTML(html)
        for i in range(1, 8):
            occos = response.xpath('//*[@id="sidebar"]/div/div[{}]/div/dl/dd/a/text()'.format(i))
            for occo in occos:
                # url = "https://www.lagou.com/jobs/list_{}?px=default&city=%E5%85%A8%E5%9B%BD#filterBox".format('java')
                # yield scrapy.Request(url,callback=self.parse_page)
                occu_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0'
                data = {
                    'first': 'true',
                    'pn': 1,
                    'kd': 'java'
                }
                # 获取返回的json数据
                response = requests.post(occu_url, data=data, headers=headers)
                # positionIds = json.loads(response.text).get('content').get('positionResult').get('result')
                try:
                    pageSize = json.loads(response.text).get('content').get('pageSize')
                    totalCount = json.loads(response.text).get('content').get('positionResult').get('totalCount')
                except json.decoder.JSONDecodeError:
                    continue
                # 获取总页数
                if int(totalCount) % int(pageSize) == 0:
                    pages = int(int(totalCount) / int(pageSize))
                else:
                    pages = int(int(totalCount) / int(pageSize)) + 1

                for page in range(int(pages)):
                    pn = page + 1
                    occu_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0'
                    data = {
                        'first': 'true',
                        'pn': pn,
                        'kd': occo
                    }

                    response = requests.post(occu_url, data=data, headers=headers)

                    try:
                        if 'content' in json.loads(response.text).keys():
                            positionIds = json.loads(response.text).get('content').get('positionResult').get('result')

                        for positionId in positionIds:
                            position = positionId.get('positionId')
                            info_url = "https://www.lagou.com/jobs/{}.html".format(str(position))
                            download(info_url)
                    except json.decoder.JSONDecodeError:
                        continue
                    except TimeoutError:
                        continue
    except Exception as e:
        print(e)

def download(info_url):
    try:
        item = {}
        html2 = requests.get(info_url,headers=header,proxies=proxies,timeout=10)
        # soup = BeautifulSoup(html2.text,'lxml')
        response2 = etree.HTML(html2.text)
        # a = soup.find('dd',class_='job-advantage').find('p').get_text()
        item['_id'] = info_url
        item['address'] = response2.xpath(
            'string(normalize-space(//*[@id="job_detail"]/dd[3]/div[1]))').replace('\n', '')
        item['companyFullName'] = response2.xpath('//*[@id="job_company"]/dt/a/img/@alt')  # 公司名字
        item['city'] = response2.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[2]/text()')  # 职位城市
        item['positionName'] = response2.xpath('/html/body/div[2]/div/div[1]/div/span/text()')  # 招聘职位
        fbsj = response2.xpath('/html/body/div[2]/div/div[1]/dd/p[2]/text()')[0]  # 发布时间
        if fbsj == '1天前  发布于拉勾网':
            fbsj = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        elif fbsj == '2天前  发布于拉勾网':
            fbsj = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%Y%m%d')
        else:
            fbsj = datetime.date.today().strftime('%Y%m%d')
        ar = []
        ar.append(fbsj)
        item['formatCreateTime'] = ar
        item['salary'] = response2.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[1]/text()')  # 薪资待遇
        item['workYear'] = response2.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[3]/text()')  # 经验要求
        item['Jobdescriptions'] = response2.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')  # 职位描述
        item['companySize'] = response2.xpath('//*[@id="job_company"]/dd/ul/li[3]/text()')[1]  # 公司大小
        item['positionAdvantage'] = response2.xpath('//*[@id="job_detail"]/dd[1]/p/text()')  # 公司福利
        item['district'] = response2.xpath('//*[@id="job_detail"]/dd[3]/div[1]/a/text()')  # 公司地址
        item['companyhref'] = info_url # 公司链接
        item['fuli'] = response2.xpath('//*[@id="job_detail"]/dd[1]/p/text()')
        items = response2.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
        lists = []
        for i in items:
            a = i.replace('\xa0', '')
            lists.append(a)
        item['duty'] = lists
        item['address'] = response2.xpath(
            'string(normalize-space(//*[@id="job_detail"]/dd[3]/div[1]))').replace('\n', '')
        if db[MONGO_TABLE].find_one(item['_id']):
            db[MONGO_TABLE].update_one({'_id': item['_id']},{"$addToSet": {'formatCreateTime':fbsj}}, upsert=True)
            print('更新成功')
        else:
            db[MONGO_TABLE].insert(dict(item))
            print('插入成功')
    except Exception as e:
        print(e)



if __name__ == '__main__':
    html = get_html()
    parse(html)





