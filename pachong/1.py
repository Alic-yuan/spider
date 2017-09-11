import requests  ##导入requests
from bs4 import BeautifulSoup  ##导入bs4中的BeautifulSoup
import os


headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (K Gecko) Chrome/22.0.1207.1 Safari/537.1"}  ##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'http://www.mzitu.com'  ##开始的URL地址
start_html = requests.get(all_url,headers=headers)  ##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
# print(start_html.text) ##打印出start_html (请注意，concent是二进制的数据，一般用于下载图片、视频、音频、等多媒体内容是才使用concent, 对于打印网页内容请使用text)
Soup = BeautifulSoup(start_html.text, 'lxml')  ##使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）
#li_list = Soup.find_all('li') ##使用BeautifulSoup解析网页过后就可以用找标签呐！（find_all是查找指定网页内的所有标签的意思，find_all返回的是一个列表。）
#for li in li_list: ##这个不解释了。看不懂的效小哥儿回去瞅瞅基础教程
     #print(li) ##同上
all_li = Soup.find('ul',id='pins').find_all('li')  ##意思是先查找id为pins的ul的标签，然后查找所有的<a>标签。

for all_a in all_li:
    a = all_a.find('span').find('a')
    title = a.get_text()
    path = str(title).strip()
    os.makedirs(os.path.join("D:\mzitu",path))
    os.chdir("D:\mzitu\\"+path)
    href = a['href']
    html = requests.get(href,headers = headers)
    html_soup = BeautifulSoup(html.text,'lxml')
    max_span = html_soup.find('div',class_='pagenavi').find_all('span')[-2].get_text()
    for page in range(1,int(max_span)+1):
        page_url = href + '/' + str(page)
        img_html = requests.get(page_url,headers = headers)
        img_soup = BeautifulSoup(img_html.text,'lxml')
        img_url = img_soup.find('div',class_='main-image').find('img')['src']
        print(img_url)

        name = img_url[-9:-4]
        img = requests.get(img_url,headers = headers)
        f =open(name + '.jpg','ab')
        f.write(img.content)
        f.close()
























