import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'http://www.mmonly.cc/mmtp/wgmv'
start_html = requests.get(all_url,headers = headers)
all_class = BeautifulSoup(start_html.text,'lxml').find('div',class_='item_list infinite_scroll masonry').find_all('div',class_='item masonry_brick masonry-brick')
for all_class1 in all_class:
    a = all_class1.find('div',class_='item_b clearfix').find('div',class_='title').find('a')


    title = a.get_text()
    path = str(title).strip()
    os.makedirs(os.path.join("D:\weiyituku",path))
    os.chdir(os.path.join("D:\weiyituku",path))
    href = a['href']
    html = requests.get(href,headers = headers)
    max_a = BeautifulSoup(html.text,'lxml').find('div',class_='pages').find_all('li')[-2].get_text()
    for page in range(1,int(max_a)+1):
        page_url = href[:-5]+'_'+str(page)+'.html'
        print(page_url)
        img_html = requests.get(page_url,headers = headers)
        img_url = BeautifulSoup(img_html.text,'lxml').find('div',class_='big-pic').find('div',id='big-pic').find('p',align='center').find('a').find('img')['src']
        print(img_url)
        img = requests.get(img_url,headers=headers)
        name = img_url[-10:-4]
        f = open(name+'.jpg','ab')
        f.write(img.content)
        f.close()

