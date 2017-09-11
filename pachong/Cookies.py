import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString


def get_html(url, cookies):
    try:
        r = requests.get(url, cookies=cookies, timeout=30)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Someting Wrong！"


def get_url(url):
    html = requests.get(url, timeout=60)
    soup = BeautifulSoup(html.text, 'lxml')
    urls = []
    result = soup.find_all('div', class_='resultBox')
    for i in result:
        url = i.find('a')['href']
        urls.append(url)
    return urls


def get_one_data(url, cookies):
    r = get_html(url, cookies)
    soup = BeautifulSoup(r, 'lxml')

    date = soup.find('div', class_='info').contents[1]
    # 判断是否抓到了数据
    if type(date) != NavigableString:
        date = soup.find('div', class_='info').contents[0]

    datalist = soup.find('tr', attrs={'bgcolor': '#FEFBEC'}).contents
    data = datalist[-2].text
    with open('hrb400_20MM.txt', 'a+') as f:
        f.write(date + '\t' + data + '\n')
    print('当前处理日期{}'.format(date))


if __name__ == '__main__':
    # 搜索页面
    base_url = 'http://search.mysteel.com/price/list.ms?page='
    #suffix = '&bn=1mp56ts&time2=2017-06-01&time1=2015-03-01&bid=01010101'

    # 获取登录cookies
    raw_cookies = '_login_token=f9ea10d8296d9c893042456ff077e073; _login_uid=2088921; _login_mid=2908280; _last_loginuname=yuan1996; f9ea10d8296d9c893042456ff077e073=17%3D5%2635%3D5%2636%3D5%2633%3D5%2634%3D5%2613%3D5%2611%3D5%2637%3D5%2638%3D5%262%3D5%261%3D5%2642%3D5%2632%3D5%2641%3D5%2640%3D5%2631%3D5%264%3D5%26catalog%3D010205%2C010202%2C0222%2C0223%2C0205'
    cookies = {}
    for line in raw_cookies.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value

    # 获取一年内符合要求的数据搜索页面
    iron_urls = []
    for i in range(1, 58):
        url = base_url + str(i)
        iron_urls.append(url)

    # 获取所有数据的详情的url页面
    urls = []
    for url in iron_urls:
        urls += (get_url(url))

    # 写入数据
    for url in urls:
        get_one_data(url, cookies)

    print('所有数据写入完毕')