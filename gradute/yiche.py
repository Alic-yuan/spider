from bs4 import BeautifulSoup
from selenium import webdriver
import os
from redis import StrictRedis
import time
import asyncio
import aiohttp
from multiprocessing import Pool




class YiChe(object):

    # 构造函数
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
        }
        self.redis = StrictRedis(host='localhost', port=6379, db=0, password='foobared')

    # 获取每个品种车辆的页面链接
    def get_links(self):
        links = []
        url = 'http://photo.bitauto.com/'
        browser = webdriver.PhantomJS()
        browser.get(url)
        browser.implicitly_wait(3)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        all_ul = soup.find_all('ul', class_='brand-list')
        for ul in all_ul:
            all_li = ul.find_all('li')
            for li in all_li:
                link = 'http://photo.bitauto.com' + li.find('a')['href']
                links.append(link)
        return links

    # 获取图片
    async def get_imgs(self, link):
        link = str(link)[2:-1]
        print('进入一级界面{}'.format(link))
        localpath = '/home/yuan/yiche/'
        async with aiohttp.ClientSession() as session:
            async with session.get(link, headers=self.headers) as html2:
                response2 = await html2.text()
                soup2 = BeautifulSoup(response2,'html.parser')
                typ = soup2.find('div', class_='crumbs-txt').find('strong').text
                all_li2 = soup2.find_all('div',class_='row block-4col-180')
                for li in all_li2:
                    all_l = li.find_all('div', class_='col-xs-3')
                    for li in all_l:
                        link2 = 'http://photo.bitauto.com' + li.find('a')['href']
                        print('进入二级界面{}'.format(link2))
                        async with session.get(link2, headers=self.headers) as html3:
                            response3 = await html3.text()
                            soup3 = BeautifulSoup(response3,'html.parser')
                            try:
                                x = 0
                                all_li3 = soup3.find('div', class_='row block-4col-180').find_all('div', class_='col-xs-3')
                                for li in all_li3:
                                    link3 = 'http://photo.bitauto.com' + li.find('a')['href']
                                    print('进入三级界面{}'.format(link3))
                                    async with session.get(link3, headers=self.headers) as html4:
                                        response4 = await html4.text()
                                        soup4 = BeautifulSoup(response4,'html.parser')
                                        src = soup4.find('div',class_='pic_box').find('img')['src']
                                        print('找到图片链接{}'.format(src))
                                        async with session.get(src, headers=self.headers) as html5:
                                            print('下载图片...')
                                            img = await html5.content.read()
                                            type = soup4.find('div',class_='b-1').find('h2').get_text() + str(x)
                                            path = localpath + typ + '/'
                                            if not os.path.exists(path):  # 新建文件夹
                                                os.mkdir(path)
                                                print('创建文件夹成功')
                                            open(path + '%s.jpg' % type, 'wb').write(img)
                                            print('{}存入成功'.format(type))
                                            x += 1
                            except Exception:
                                continue

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

    # 执行函数
    def run(self):
        urls = []
        url = self.redis.spop('url')
        while url:
            print(url)
            urls.append(url)
            url = self.redis.spop('url')
        tasks = [self.get_imgs(i) for i in urls]
        loop = asyncio.get_event_loop()
        # 执行coroutine
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    # 主函数，多进程运行执行函数
    def main(self):
        start_time = time.time()
        p = Pool()
        for i in range(4):
            p.apply_async(self.run())
        p.close()
        p.join()
        print(time.time() - start_time)





if __name__ == '__main__':
    yc = YiChe()
    # yc.to_redis()
    yc.check_redis()
    # yc.main()




