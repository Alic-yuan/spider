from bs4 import BeautifulSoup
import os
import time
from log import Logger
import requests
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import re
from gevent import monkey, pool
import gevent
import greenlet
import threading

monkey.patch_all()  # 把当前程序的所有的IO操作给作上标记


logyc = Logger('yc2.log')

def get_pic(url):
     try:
        pic_obj = requests.get(url).content
     except Exception as e:
         print('fail')
         return ""
     time.sleep(1)
     filename = url.split('/')[-2]
     file_path = "./picture/" + filename + '.jpg'
     open(file_path, 'wb').write(pic_obj)
     time.sleep(1)
     logyc.info('ok')
     return "ok"


urls = ['http://img4.bitautoimg.com/autoalbum/files/20140529/702/21501370297_3353683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140529/770/21120077021445_3353684_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140530/82/101221082796_3353688_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20140530/625/10120262566505_3353689_14.jpg',
        'http://img3.bitautoimg.com/autoalbum/files/20140530/413/10115641339117_3353690_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/216/22300421669834_3353691_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/438/15185443800420_2670681_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20130715/485/15185448514914_2670683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20130715/516/15185451647570_2670684_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/547/15185454783563_2670685_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/702/21501370297_3353683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140529/770/21120077021445_3353684_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140530/82/101221082796_3353688_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20140530/625/10120262566505_3353689_14.jpg',
        'http://img3.bitautoimg.com/autoalbum/files/20140530/413/10115641339117_3353690_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/216/22300421669834_3353691_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/438/15185443800420_2670681_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20130715/485/15185448514914_2670683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20130715/516/15185451647570_2670684_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/547/15185454783563_2670685_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/702/21501370297_3353683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140529/770/21120077021445_3353684_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140530/82/101221082796_3353688_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20140530/625/10120262566505_3353689_14.jpg',
        'http://img3.bitautoimg.com/autoalbum/files/20140530/413/10115641339117_3353690_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/216/22300421669834_3353691_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/438/15185443800420_2670681_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20130715/485/15185448514914_2670683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20130715/516/15185451647570_2670684_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/547/15185454783563_2670685_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/702/21501370297_3353683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140529/770/21120077021445_3353684_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140530/82/101221082796_3353688_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20140530/625/10120262566505_3353689_14.jpg',
        'http://img3.bitautoimg.com/autoalbum/files/20140530/413/10115641339117_3353690_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/216/22300421669834_3353691_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/438/15185443800420_2670681_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20130715/485/15185448514914_2670683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20130715/516/15185451647570_2670684_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/547/15185454783563_2670685_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/702/21501370297_3353683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140529/770/21120077021445_3353684_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140530/82/101221082796_3353688_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20140530/625/10120262566505_3353689_14.jpg',
        'http://img3.bitautoimg.com/autoalbum/files/20140530/413/10115641339117_3353690_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/216/22300421669834_3353691_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/438/15185443800420_2670681_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20130715/485/15185448514914_2670683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20130715/516/15185451647570_2670684_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/547/15185454783563_2670685_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/702/21501370297_3353683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140529/770/21120077021445_3353684_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140530/82/101221082796_3353688_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20140530/625/10120262566505_3353689_14.jpg',
        'http://img3.bitautoimg.com/autoalbum/files/20140530/413/10115641339117_3353690_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/216/22300421669834_3353691_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/438/15185443800420_2670681_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20130715/485/15185448514914_2670683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20130715/516/15185451647570_2670684_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/547/15185454783563_2670685_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/702/21501370297_3353683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140529/770/21120077021445_3353684_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140530/82/101221082796_3353688_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20140530/625/10120262566505_3353689_14.jpg',
        'http://img3.bitautoimg.com/autoalbum/files/20140530/413/10115641339117_3353690_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/216/22300421669834_3353691_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/438/15185443800420_2670681_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20130715/485/15185448514914_2670683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20130715/516/15185451647570_2670684_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/547/15185454783563_2670685_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/702/21501370297_3353683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140529/770/21120077021445_3353684_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140530/82/101221082796_3353688_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20140530/625/10120262566505_3353689_14.jpg',
        'http://img3.bitautoimg.com/autoalbum/files/20140530/413/10115641339117_3353690_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/216/22300421669834_3353691_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/438/15185443800420_2670681_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20130715/485/15185448514914_2670683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20130715/516/15185451647570_2670684_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/547/15185454783563_2670685_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/702/21501370297_3353683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140529/770/21120077021445_3353684_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140530/82/101221082796_3353688_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20140530/625/10120262566505_3353689_14.jpg',
        'http://img3.bitautoimg.com/autoalbum/files/20140530/413/10115641339117_3353690_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/216/22300421669834_3353691_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/438/15185443800420_2670681_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20130715/485/15185448514914_2670683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20130715/516/15185451647570_2670684_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/547/15185454783563_2670685_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/702/21501370297_3353683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140529/770/21120077021445_3353684_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20140530/82/101221082796_3353688_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20140530/625/10120262566505_3353689_14.jpg',
        'http://img3.bitautoimg.com/autoalbum/files/20140530/413/10115641339117_3353690_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20140529/216/22300421669834_3353691_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/438/15185443800420_2670681_14.jpg',
        'http://img4.bitautoimg.com/autoalbum/files/20130715/485/15185448514914_2670683_14.jpg',
        'http://img1.bitautoimg.com/autoalbum/files/20130715/516/15185451647570_2670684_14.jpg',
        'http://img2.bitautoimg.com/autoalbum/files/20130715/547/15185454783563_2670685_14.jpg',
        ]


# 单线程
for i in urls:
    get_pic(i)
# 多线程
# p = ThreadPoolExecutor(max_workers=100)
# for i in urls:
#         p.submit(get_pic, i)
# 协程
# tasks = []
# p = pool.Pool(100)
# for i in urls:
#         tasks.append(p.spawn(get_pic, i))
# gevent.joinall(tasks)



