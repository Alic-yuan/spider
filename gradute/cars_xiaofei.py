import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
from redis import StrictRedis
from concurrent.futures import ThreadPoolExecutor



class CarsXiaoFei(object):

    # 构造函数
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
        }
        self.redis = StrictRedis(host='localhost', port=6379, db=0, password='foobared')

    # 获取每个品种车辆的页面链接
    def get_links(self):
        links = []
        url = 'http://pic.315che.com/'
        browser = webdriver.PhantomJS()
        browser.get(url)
        browser.implicitly_wait(3)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        all_ul = soup.find('ul', id='tree-main').find_all('ul', class_='brand-list')
        for ul in all_ul:
            all_li = ul.find_all('li')
            for li in all_li:
                link = li.find('a')['href']
                links.append(link)
        return links

    # 获取图片
    def get_imgs(self, link):
        print('进入一级界面{}'.format(link))
        localpath = '/home/yuan/carsxiaofei/'
        response2 = requests.get(link, headers=self.headers)
        response2.encoding = 'utf-8'
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        typ = soup2.find('div', class_='uibox').find('a').find('div').get_text()
        print(typ)
        all_li2 = soup2.find_all('div',class_='ui-base-list ui-base-list-02')
        for li in all_li2:
            all_l = li.find_all('li')
            for li in all_l:
                link2 = li.find('a')['href']
                print('进入二级界面{}'.format(link2))
                response3 = requests.get(link2, headers=self.headers)
                response3.encoding = 'utf-8'
                soup3 = BeautifulSoup(response3.text, 'html.parser')
                try:
                    x = 0
                    all_li3 = soup3.find('div', class_='car-type-photo-list clearfix').find_all('li')
                    for li in all_li3:
                        link3 = li.find('a')['href']
                        print('进入三级界面{}'.format(link3))
                        response4 = requests.get(link3, headers=self.headers)
                        response4.encoding = 'utf-8'
                        soup4 = BeautifulSoup(response4.text, 'html.parser')
                        src = soup4.find('div', class_='auto-pic-show').find('img')['src']
                        print('找到图片链接{}'.format(src))
                        print('下载图片...')
                        img = requests.get(src)
                        type = soup4.find('div', class_='car-head-info mb10').find('span').get_text() + '_' + str(x)
                        path = localpath + typ + '/'
                        if not os.path.exists(path):  # 新建文件夹
                            os.mkdir(path)
                            print('创建文件夹成功')
                        open(path + '%s.jpg' % type, 'wb').write(img.content)
                        print('{}存入成功'.format(type))
                        x += 1
                except Exception:
                    continue

    # 存储到redis
    def to_redis(self):
        links = self.get_links()
        for i in links:
            print(i)
            self.redis.sadd('links', i)
        print('finish')

    # 查看redis
    def check_redis(self):
        print(self.redis.smembers('links'))
        print(self.redis.scard('links'))

    # 执行函数
    def run(self):
        start_time = time.time()
        urls = []
        url = self.redis.spop('links')
        while url:
            print(url)
            urls.append(url)
            url = self.redis.spop('links')
        pool = ThreadPoolExecutor(max_workers=5)
        for i in urls:
            pool.submit(self.get_imgs, i)
        print(time.time() - start_time)



if __name__ == '__main__':
    xf = CarsXiaoFei()
    xf.to_redis()
    # xf.check_redis()
    xf.run()