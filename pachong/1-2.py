import requests
from bs4 import BeautifulSoup
import os


class Mzitu():

    def all_url(self,all_url):
        html = self.request(all_url)
        all_a = BeautifulSoup(html.text,'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            print('开始保存',title)
            path = str(title).replace("?",'_')
            self.makedir(path)
            href = a['href']
            self.html(href)

    def request(self, url):
        headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url,headers = headers)
        return content

    def makedir(self, path):
        path = path.strip()
        isExist = os.path.exists("D:\mzitu",path)
        if not isExist:
            print('开始保存',path,'的文件夹')
            os.makedirs(os.path.join("D:\mzitu",path))
            os.chdir(os.path.join("D:\mzitu"),path)
            return True
        else:
            print('名字为',path,'已经存在')
            return False


    def html(self, href):
        html = self.request(href)
        max_span = BeautifulSoup(html.text,'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1,int(max_span)+1):
            page_url = href + '/' + str(page)
            self.img(page_url)

    def img(self, page_url):
        html = self.request(page_url)
        img_url = BeautifulSoup(html.text,'lxml').find('div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self, img_url):
        name = img_url[-9:-4]
        f = open(name+'.jpg','ab')
        img = self.request(img_url)
        f.write(img.content)
        f.close()

mzi = Mzitu()
mzi.all_url('http://www.mzitu.com')





