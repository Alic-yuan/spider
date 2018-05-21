import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
from redis import StrictRedis
from multiprocessing import Pool
from log import Logger
from concurrent.futures import ThreadPoolExecutor




class CarsHome(object):

    # 构造函数
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
        }
        self.redis = StrictRedis(host='localhost', port=6379, db=0, password='foobared')
        self.logch = Logger('ch.log')

    # 获取每个品种车辆的页面链接
    def get_links(self):
        links = []
        url = 'https://car.autohome.com.cn/pic/'
        browser = webdriver.PhantomJS()
        browser.get(url)
        browser.implicitly_wait(3)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        all_ul = soup.find('div', id='cartree').find_all('ul')[:-1]
        for ul in all_ul:
            all_li = ul.find_all('li')
            for li in all_li:
                link = 'https://car.autohome.com.cn' + li.find('a')['href']
                print(link)
                links.append(link)
        return links

    # 获取图片
    def get_imgs(self, link):
        self.logch.debug('进入一级界面{}'.format(link))
        localpath = '/home/yuan/carshome/'
        try:
            response2 = requests.get(link, headers = self.headers)
            soup2 = BeautifulSoup(response2.text,'html.parser')
            typ = soup2.find('div',class_='breadnav').find_all('a')[-1].text
            all_li2 = soup2.find_all('div',class_='uibox-con carpic-list02')
            for li in all_li2:
                all_l = li.find_all('li')
                for li in all_l:
                    link2 = 'https://car.autohome.com.cn' + li.find('a')['href']
                    self.logch.info('进入二级界面{}'.format(link2))
                    response3 = requests.get(link2, headers = self.headers)
                    soup3 = BeautifulSoup(response3.text,'html.parser')
                    try:
                        x = 0
                        all_li3 = soup3.find('div',class_='uibox-con carpic-list03').find_all('li')
                        for li in all_li3:
                            link3 = 'https://car.autohome.com.cn' + li.find('a')['href']
                            self.logch.info('进入三级界面{}'.format(link3))
                            response4 = requests.get(link3, headers = self.headers)
                            soup4 = BeautifulSoup(response4.text,'html.parser')
                            src = 'https:' + soup4.find('div',class_='pic').find('img')['src']
                            self.logch.info('找到图片链接{}'.format(src))
                            self.logch.info('下载图片...')
                            img = requests.get(src)
                            type = soup4.find('div',class_='pic-info').get_text() + '_' + str(x)
                            path = localpath + typ + '/'
                            if not os.path.exists(path):  # 新建文件夹
                                os.mkdir(path)
                                self.logch.info('创建文件夹成功')
                            open(path + '%s.jpg' % type, 'wb').write(img.content)
                            self.logch.info('{}存入成功'.format(type))
                            x += 1
                    except Exception:
                        self.logch.war('在{}出错'.format(link2))
                        pass
        except Exception:
            self.logch.error('在{}出错'.format(link))
            pass

    # 存储到redis
    def to_redis(self):
        links = self.get_links()
        for i in links:
            print(i)
            self.redis.sadd('urls', i)
        print('finish')

    # 查看redis
    def check_redis(self):
        print(self.redis.smembers('urls'))
        print(self.redis.scard('urls'))

    # 执行函数
    def run(self):
        url = self.redis.spop('urls')
        print(url)
        while url:
            self.get_imgs(url)
            print('done')
            url = self.redis.spop('urls')
            time.sleep(3)

    # 主函数，多进程运行执行函数
    def main(self):
        start_time = time.time()
        self.run()
        print(time.time() - start_time)





if __name__ == '__main__':
    ch = CarsHome()
    # ch.to_redis()
    ch.check_redis()
    ch.main()

