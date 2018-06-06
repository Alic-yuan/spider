import tkinter
from tkinter import scrolledtext  # 引入带滚动条的文本框
from cars_home import CarsHome
from cars_xiaofei import CarsXiaoFei
from yiche import YiChe
from baidu_cars import BaiduCars
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
import os
import sys
from redis import StrictRedis
from multiprocessing import Pool
from log import Logger
import signal

cd = tkinter.Tk()  # 创建Tk对象
cd.title("车辆图片采集器")  # 设置窗口标题
cd.geometry("470x402+500+0")  # 设置窗口尺寸
# text1 = scrolledtext.ScrolledText(cd)  # 创建用于输出的滚动条文本框text1
text1=tkinter.Text(cd)
text1.pack(fill=tkinter.X,side=tkinter.BOTTOM)

class CH(CarsHome):

    def check_count(self):
        a = self.redis.scard('urls')
        while a:
            count1 = 0  # 计数大文件夹下共有多少个小文件夹
            for filename in os.listdir('/home/yuan/carshome2'):
                path = os.path.join('/home/yuan/carshome2', filename)
                count = 0
                ls = os.listdir(path)
                for i in ls:
                    if os.path.isfile(os.path.join(path, i)):
                        count += 1
                count1 += count
            text1.insert(tkinter.END, '当前已存储车辆图片{}张...'.format(count1) + '\n')
            text1.see(tkinter.END)
            text1.update()
            a = self.redis.scard('urls')
            time.sleep(1)

    def clear(self):
        text1.delete(0.0, tkinter.END)

    def quit(self):
        exit()

    def main(self):
        p1 = Process(target=self.run)
        p2 = Process(target=self.check_count)
        p1.start()
        p2.start()
        p1.join()
        p2.join()
ch = CH()


class CX(CarsXiaoFei):
    def check_count(self):
        a = 1
        while a:
            count1 = 0  # 计数大文件夹下共有多少个小文件夹
            for filename in os.listdir('/home/yuan/carsxiaofei2'):
                path = os.path.join('/home/yuan/carsxiaofei2', filename)
                count = 0
                ls = os.listdir(path)
                for i in ls:
                    if os.path.isfile(os.path.join(path, i)):
                        count += 1
                count1 += count
            text1.insert(tkinter.END, '当前已存储车辆图片{}张...'.format(count1) + '\n')
            text1.see(tkinter.END)
            text1.update()
            time.sleep(1)
    def main(self):
        self.run()
        pool1 = ThreadPoolExecutor(max_workers=1)
        pool1.submit(self.check_count)
cx = CX()

class YC(YiChe):
    def check_count(self):
        a = 1
        while a:
            count1 = 0  # 计数大文件夹下共有多少个小文件夹
            for filename in os.listdir('/home/yuan/yiche2'):
                path = os.path.join('/home/yuan/yiche2', filename)
                count = 0
                ls = os.listdir(path)
                for i in ls:
                    if os.path.isfile(os.path.join(path, i)):
                        count += 1
                count1 += count
            text1.insert(tkinter.END, '当前已存储车辆图片{}张...'.format(count1) + '\n')
            text1.see(tkinter.END)
            text1.update()
            time.sleep(1)

    def main(self):
        p1 = Process(target=self.run)
        p2 = Process(target=self.check_count)
        p1.start()
        p2.start()
        p1.join()
        p2.join()
yc = YC()

class BC(BaiduCars):
    def check_count(self):
        a = 1
        while a:
            count1 = 0  # 计数大文件夹下共有多少个小文件夹
            for filename in os.listdir('/home/yuan/cars'):
                try:
                    path = os.path.join('/home/yuan/cars', filename)
                    count = 0
                    ls = os.listdir(path)
                    for i in ls:
                        if os.path.isfile(os.path.join(path, i)):
                            count += 1
                    count1 += count
                except Exception:
                    pass
            text1.insert(tkinter.END, '当前已存储车辆图片{}张...'.format(count1) + '\n')
            text1.see(tkinter.END)
            text1.update()
            time.sleep(1)
    def main(self):
        dataList = self.getManyPages('奥迪', 10)
        p2 = ThreadPoolExecutor(max_workers=1)
        p2.submit(self.getImg, dataList, '/home/yuan/cars/奥迪/')
        self.check_count()
bc = BC()

def quit():
    a = os.getgid()
    print(a)
    # os.kill(a, signal.SIGABRT)




tkinter.Button(cd, bg='green', text="单线程爬虫(汽车之家)", command=ch.main).place(x=0, y=0, anchor=tkinter.NW)  # 也可以通过bg/font等参数控制Button的样式
tkinter.Button(cd, bg='green',text="多线程爬虫(汽车消费网)", command=cx.main).place(x=140, y=0, anchor=tkinter.NW)  # 也可以通过bg/font等参数控制Button的样式
tkinter.Button(cd, bg='green',text="协程爬虫(易车网)", command=yc.main).place(x=290, y=0, anchor=tkinter.NW)  # 也可以通过bg/font等参数控制Button的样式
tkinter.Button(cd, bg='green',text="百度下载", command=bc.main).place(x=400, y=0, anchor=tkinter.NW)
# tkinter.Button(cd, text="停止", command=quit).place(x=220, y=30, anchor=tkinter.NW)
tkinter.Button(cd, bg='red',text="清除", command=ch.clear).place(x=200, y=30, anchor=tkinter.NW)
cd.mainloop()  # 进入主循环