import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os



def get_image(url):
    hrefs = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_li = soup.find('div',class_='uibox-con carpic-list02').find_all('li')
    for li in all_li:
        href = 'https:' + li.find('img')['src']
        # name = li.find('div').find('a').text
        hrefs.append(href)
    return hrefs

def get_links():
    localPath = '/home/yuan/carshome/'
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
            typ = li.find('a').text.split('(', 1)[0]
            path = localPath + typ + '/'
            if not os.path.exists(path):  # 新建文件夹
                os.mkdir(path)
                print('创建文件夹成功')
            hrefs = get_image(link)
            x = 0
            for href in hrefs:
                img= requests.get(href)
                open(path + '%d.jpg' % x, 'wb').write(img.content)
                print('读入成功')
                x += 1


if __name__ == '__main__':
    get_links()