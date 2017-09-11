import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        html = requests.get(url,timeout=3)
        html.raise_for_status
        html.encoding = 'utf-8'
        return html.text
    except:
        print('Error')

def get_content(url):
    content = get_html(url)
    soup = BeautifulSoup(content,'lxml')

    results = soup.find('ul',class_='area_three area_list').find_all('li')

    for top in results:
        rank = top.find('div', class_='top_num').text
        name = top.find('div', class_='info').h3.a.text
        singer = top.find('p', class_='cc').a.text
        time = top.find('p', class_='c9').text
        score = top.find('div', class_='score_box').h3.text
        a = '{}\t {}\t {}\t {}\t {}\n'.format(rank,name,singer,time,score)
        print(a)
        with open('D:/song/song_list.csv','a') as f:
            f.write(a)


def get_areas():
    area = ['ML','HT','US','KR','JP']
    base_url = 'http://vchart.yinyuetai.com/vchart/trends?area='
    for i in range(5):
        url = base_url + area[i]
        get_content(url)

if __name__ == '__main__':
    get_areas()
