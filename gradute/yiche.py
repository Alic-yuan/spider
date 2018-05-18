from bs4 import BeautifulSoup
import os
from redis import StrictRedis
import time
import asyncio
import aiohttp
from log import Logger
import requests
import re




class YiChe(object):

    # 构造函数
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
        }
        self.redis = StrictRedis(host='localhost', port=6379, db=0, password='foobared')
        self.logyc = Logger('yc.log')

    # 获取每个品种车辆的页面链接
    def get_links(self):
        url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=tupian&pagetype=masterbrand&objid=108'
        response = requests.get(url, headers=self.headers)
        lists1 = re.findall('/master/\d+', response.text)
        links = ['http://photo.bitauto.com' + link for link in lists1]
        return links

    # 获取图片
    async def get_imgs(self, link):
        link = str(link)[2:-1]
        self.logyc.info('进入一级界面{}'.format(link))
        localpath = '/home/yuan/yiche/'
        async with aiohttp.ClientSession() as session:
            # await asyncio.sleep(3)
            async with session.get(link, headers=self.headers) as html2:
                response2 = await html2.text()
                soup2 = BeautifulSoup(response2, 'html.parser')
                try:
                    typ = soup2.find('div', class_='box').find('h2').text
                    path = localpath + typ + '/'
                    all_li2 = soup2.find_all('div', class_='row block-4col-180')
                    for li in all_li2:
                        all_l = li.find_all('div', class_='col-xs-3')
                        for li in all_l:
                            link2 = 'http://photo.bitauto.com' + li.find('a')['href']
                            self.logyc.info('进入二级界面{}'.format(link2))
                            # await asyncio.sleep(3)
                            async with session.get(link2, headers=self.headers) as html3:
                                response3 = await html3.text()
                                soup3 = BeautifulSoup(response3, 'html.parser')
                                try:
                                    x = 0
                                    all_li3 = soup3.find('div', class_='row block-4col-180').find_all('div',
                                                                                                      class_='col-xs-3')
                                    for li in all_li3:
                                        link3 = 'http://photo.bitauto.com' + li.find('a')['href']
                                        self.logyc.info('进入三级界面{}'.format(link3))
                                        # await asyncio.sleep(3)
                                        async with session.get(link3, headers=self.headers) as html4:
                                            response4 = await html4.text()
                                            soup4 = BeautifulSoup(response4, 'html.parser')
                                            src = soup4.find('div', class_='pic_box').find('img')['src']
                                            self.logyc.info('找到图片链接{}'.format(src))
                                            # await asyncio.sleep(3)
                                            async with session.get(src, headers=self.headers) as html5:
                                                self.logyc.info('下载图片...')
                                                img = await html5.content.read()
                                                type = soup4.find('div', class_='b-1').find(
                                                    'h2').get_text() + '_' + str(x)
                                                if not os.path.exists(path):  # 新建文件夹
                                                    os.mkdir(path)
                                                    self.logyc.info('创建{}文件夹成功'.format(typ))
                                                open(path + '%s.jpg' % type, 'wb').write(img)
                                                self.logyc.info('{}存入成功'.format(type))
                                                x += 1
                                except Exception:
                                    self.logyc.war('在二级目录出错{}'.format(link2))
                                    pass
                except Exception:
                    self.logyc.error('在一级目录出错{}'.format(link))
                    pass

    # 存储到redis
    def to_redis(self):
        links = self.get_links()
        for i in links:
            print(i)
            self.redis.sadd('url', i)
        print('finish')

    # 查看redis
    def check_redis(self):
        print(self.redis.smembers('url'))
        print(self.redis.scard('url'))

    # 执行函数
    def run(self):
        urls = []
        url = self.redis.spop('url')
        while url:
            print(url)
            urls.append(self.get_imgs(url))
            url = self.redis.spop('url')
        tasks = [asyncio.ensure_future(i) for i in urls]
        loop = asyncio.get_event_loop()
        # 执行coroutine
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    # 主函数，多进程运行执行函数
    def main(self):
        start_time = time.time()
        self.run()
        print(time.time() - start_time)





if __name__ == '__main__':
    yc = YiChe()
    yc.to_redis()
    # yc.check_redis()
    yc.main()




