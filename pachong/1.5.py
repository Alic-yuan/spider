import time
import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return 'ERROR'



def get_content(url):
    comments = []
    html = get_html(url)
    soup = BeautifulSoup(html,'lxml')
    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})

    for li in liTags:
        comment = {}
        try:
            # 开始筛选信息，并保存到字典中
            comment['title'] = li.find(
                'a', attrs={'class': 'j_th_tit '}).text.strip()
            comment['link'] = "http://tieba.baidu.com/" + \
                              li.find('a', attrs={'class': 'j_th_tit '})['href']
            comment['name'] = li.find(
                'span', attrs={'class': 'tb_icon_author '}).text.strip()
            comment['time'] = li.find(
                'span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find(
                'span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)
        except:
            print('出了点小问题')
    return comments



def save(dict):
    with open('TTBT.txt', 'a+') as f:
        for comment in dict:
            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(
                comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))

        print('当前页面爬取完成')


def main(base_url,deep):
    urls = []
    for i in range(0,deep):
        urls.append(base_url+'$pn='+str(i * 50))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')
    for url in urls:
        content = get_content(url)
        save(content)
    print('所有的信息都已经保存完毕！')

base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'
# 设置需要爬取的页码数量
deep = 1

if __name__ == '__main__':
    main(base_url, deep)