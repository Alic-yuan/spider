import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        html = requests.get(url)
        html.raise_for_status
        html.encoding = html.apparent_encoding
        return html.text
    except:
        print('something wrong')

def get_content(url):
    content = get_html(url)
    soup = BeautifulSoup(content,'lxml')

    all_li = soup.find('ul',class_='area_three area_list').find_all('li')

    for top in all_li:
        rank = top.find('div',class_='top_num').text
        name = top.find('div',class_='info').h3.a.text
        singer = top.find('p',class_='cc').a.text
        time = top.find('p',class_='c9').text
        score = top.find('div',class_='score_box').h3.text
        a ='{}\t {}\t {}\t {}\t {}\n'.format(rank,name,singer,time,score)
        print(a)
        with open('D:/song/song_list.csv','a') as f:
            f.write(a)

def area(url):
    url_list = []
    name_list = []
    list = ['ML','HT','US','JP','KR']
    for i in range(5):
        url1 = url+list[i]
        url_list.append(url1)
    return url_list

def get_songs(url_list):
    for url in url_list:
        get_content(url)

def main():
    url ='http://vchart.yinyuetai.com/vchart/trends?area='
    url_list = area(url)
    get_songs(url_list)

if __name__ == '__main__':
    main()



