import requests
from bs4 import BeautifulSoup
import os
import xlwt


class meizi(object):

    def __init__(self):
        self.f = None
        self.count = 1
        self.sheetInfo = None
        self.create_execl()
        pass

    def craw_data(self):
        headers =  {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
        }
        urls = ['http://www.budejie.com/new-pic/']
        for i in range(2,10):
            url = 'http://www.budejie.com/new-pic/' + str(i)
            urls.append(url)
        for url in urls:
            print(url)
            response = requests.get(url,headers=headers)
            self.parse_date(response.text)

    def parse_date(self, response):
        try:
            soup = BeautifulSoup(response,'lxml')
            all_list = soup.find_all('div',class_='j-r-list')
            for list in all_list:
                all_li = list.find('ul').find_all('li')
                for li in all_li:
                    try:
                        name = li.find('div',class_='j-list-user').find('div',class_='u-txt').find('a').get_text()
                        time = li.find('div', class_='j-list-user').find('div', class_='u-txt').find('span').get_text()
                        content = li.find('div',class_='j-r-list-c').find('a').get_text()
                        picture = li.find('div',class_='j-r-list-c-img').find('a').img['data-original']
                        print(name,time,content,picture)
                        self.store_info(name,picture)
                        self.store_info_execl(name,time,content,picture)
                    except:
                        pass
        except Exception as e:
            print(e)

    def store_info(self,name,picture):
        filename = '{}.png'.format(name)
        try:
            image_path = '/home/yuan/pic'
            if not os.path.exists(image_path):
                os.makedirs(image_path)
                print(image_path + '创建成功')

            with open(image_path + '/' + filename,'wb') as f:
                f.write(requests.get(picture).content)
        except Exception as e:
            print(e)

    def store_info_execl(self,name,time,content,picture):
        lists = []
        lists.append(self.count)
        lists.append(name)
        lists.append(time)
        lists.append(content)
        lists.append(picture)
        for j in range(len(lists)):
            self.sheetInfo.write(self.count,j,lists[j])
        self.f.save('百思不得姐.xlsx')
        self.count += 1
        print('插入了{}条数据'.format(self.count))

    def create_execl(self):
        self.f = xlwt.Workbook()
        self.sheetInfo = self.f.add_sheet('百思不得姐',cell_overwrite_ok=True)
        rowTitle = ['编号','发布者昵称','发布时间','发布内容','发布图片']
        for i in range(0,len(rowTitle)):
            self.sheetInfo.write(0,i,rowTitle[i])


if __name__ == '__main__':
    mz = meizi()
    mz.craw_data()