from bs4 import BeautifulSoup
import os
import time
from log import Logger
import requests
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import re
from gevent import monkey; monkey.patch_all()
import gevent


'''多进程
   多线程
   单线程
   协程'''




class YiChe(object):

    # 构造函数
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
        }

    # 获取每个品种车辆的页面链接
    def get_links(self):
        url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=tupian&pagetype=masterbrand&objid=108'
        response = requests.get(url, headers=self.headers)
        lists1 = re.findall('/master/\d+', response.text)
        links = ['http://photo.bitauto.com' + link for link in lists1]
        return links

    # 获取图片
    def get_imgs(self, link):
        self.logyc = Logger('yc2.log')
        # link = str(link)[2:-1]
        self.logyc.info('进入一级界面{}'.format(link))
        localpath = '/home/yuan/yiche2/'
        html2 = requests.get(link, headers=self.headers)
        response2 = html2.text
        soup2 = BeautifulSoup(response2,'html.parser')
        typ = soup2.find('div', class_='crumbs-txt').find('strong').text
        all_li2 = soup2.find_all('div',class_='row block-4col-180')
        for li in all_li2:
            all_l = li.find_all('div', class_='col-xs-3')
            for li in all_l:
                link2 = 'http://photo.bitauto.com' + li.find('a')['href']
                self.logyc.info('进入二级界面{}'.format(link2))
                html3 = requests.get(link2, headers=self.headers)
                response3 = html3.text
                soup3 = BeautifulSoup(response3,'html.parser')
                try:
                    x = 0
                    all_li3 = soup3.find('div', class_='row block-4col-180').find_all('div', class_='col-xs-3')
                    for li in all_li3:
                        link3 = 'http://photo.bitauto.com' + li.find('a')['href']
                        self.logyc.info('进入三级界面{}'.format(link3))
                        html4 = requests.get(link3, headers=self.headers)
                        response4 = html4.text
                        soup4 = BeautifulSoup(response4,'html.parser')
                        src = soup4.find('div',class_='pic_box').find('img')['src']
                        self.logyc.info('找到图片链接{}'.format(src))
                        html5 = requests.get(src, headers=self.headers)
                        self.logyc.info('下载图片...')
                        img = html5.content
                        type = soup4.find('div',class_='b-1').find('h2').get_text() + '_' +str(x)
                        path = localpath + typ + '/'
                        if not os.path.exists(path):  # 新建文件夹
                            os.mkdir(path)
                            self.logyc.info('创建文件夹成功')
                        open(path + '%s.jpg' % type, 'wb').write(img)
                        self.logyc.info('{}存入成功'.format(type))
                        x += 1
                except Exception:
                    self.logyc.error('在{}出错'.format(link2))
                    pass







if __name__ == '__main__':
    yc = YiChe()
    urls = yc.get_links()
    # url = urls[:4]
    # print(url)
    starttime = time.time()
    # 协程
    tasks = []
    for i in urls:
        tasks.append(gevent.spawn(yc.get_imgs, i))
    gevent.joinall(tasks)
    # 多线程
    # pool = ThreadPoolExecutor(max_workers=100)
    # for i in urls:
    #     pool.submit(yc.get_imgs, i)
    # 单线程
    # yc.get_imgs(url)
    # 多进程
    # p = Pool(4)
    # p.map(yc.get_imgs, url)
    # p.close()
    # p.join()
    print(time.time()-starttime)