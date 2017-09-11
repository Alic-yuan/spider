import requests
from bs4 import BeautifulSoup

def get_html(url):
    html = requests.get(url)
    html.raise_for_status
    html.encoding = 'gbk'
    return html.text

def get_content(url):
    content = get_html(url)
    soup = BeautifulSoup(content,'lxml')

    movies_list = soup.find('ul', class_='picList clearfix')
    movies = movies_list.find_all('li')


    for top in movies:
        title = top.find('span',class_ = 'sTit').a.text
        img_url = top.find('div',class_='pic').img['src']
        try:
            time = top.find('span',class_='sIntro').text
        except:
            print('暂无上映时间')
        actors = top.find('p',class_='pActor')
        actor = ''
        for act in actors.contents:
            actor = actor + act.string + ''
        intro = top.find('p',class_='pTxt pIntroShow').text
        print('片名:{} {} {} {}'.format(title,time,actor,intro))
        with open('D:/movies/'+title+'.png','wb+') as f:
            f.write(requests.get(img_url).content)

def main():
    url = 'http://dianying.2345.com/top/'
    get_content(url)

if __name__ == '__main__':
    main()


