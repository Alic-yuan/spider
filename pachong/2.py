import requests
from bs4 import BeautifulSoup
import os
from Download import request
from pymongo import MongoClient
import datetime


class Mzitu():

    def __init__(self):
        client = MongoClient()
        db = client['meinvxiezhenji']
        self.meizitu_collection = db['meizitu']
        self.title = ''
        self.url = ''
        self.img_urls = []

    def all_url(self,url):
        html = request.get(url,3)
        all_li = BeautifulSoup(html.text,'lxml').find('ul',id = 'pins').find_all('li')

        for all_a in all_li:
            a = all_a.find('span').find('a')
            title = a.get_text()
            self.title =title
            print('开始保存',title)
            path = str(title).replace("?",'_')
            self.makedir(path)
            href = a['href']
            self.href = href
            if self.meizitu_collection.find_one({'主题页面':href}):
                print('这个页面已经爬取过了')
            else:
                self.html(href)

    #def request(self,url):
        #headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

        #content = requests.get(url,headers = headers)
        #return content

    def makedir(self,path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\mzitu3",path))
        if not isExists:
            print('建了一个名字叫做',path,'的文件夹')
            os.makedirs(os.path.join("D:\mzitu3",path))
            os.chdir(os.path.join("D:\mzitu3",path))
            return True
        else:
            print('名字叫做',path,'已经存在')
            return False

    def html(self,href):
        html = request.get(href,3)
        max_span = BeautifulSoup(html.text,'lxml').find('div',class_='pagenavi').find_all('span')[-2].get_text()
        page_num = 0
        for page in range(1, int(max_span) + 1):
            page_num += 1
            page_url = href + '/' + str(page)
            self.img(page_url,max_span,page_num)

    def img(self,page_url,max_span,page_num):
        img_html = request.get(page_url,3)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.img_urls.append(img_url)
        if int(max_span) == page_num:
            self.save(img_url)
            post = {'标题':self.title,
                    '主题页面':self.url,
                    '图片地址':self.img_urls,
                    '获取时间':datetime.datetime.now()}
            self.meizitu_collection.save(post)
            print('插入数据成功')
        else:
            self.save(img_url)
            print(img_url)

    def save(self,img_url):
        name = img_url[-9:-4]
        img = request.get(img_url,3)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

Mzi = Mzitu()
Mzi.all_url('http://www.mzitu.com')


