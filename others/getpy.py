# 获取影视作品封面
# 2019-12-31
# https://www.seejav.icu/

import requests
import re
import os
import time
import random
from progressbar import *

javurl = 'https://www.seejav.icu/'

# filepaths = os.listdir(os.getcwd())
allpath = "./zk9/"

# 延时开关
delay = 1


class Cart:
    def __init__(self, name):
        self.url = javurl+name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.name = name        
        self.html = ''
        self.coverurl=''
        self.sampleurllist=[]
        self.path = allpath

    def get_html(self):
        try:
            r = requests.get(self.url, headers=self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            self.html = r.text
        except:
            return '产生异常'

    def get_img(self):
        
        
        result = re.findall(re.compile(r'src="(/pics/cover/.*?\.jpg)"'), self.html)
        if len(result) == 1:
            self.coverurl = result[0]
            print(self.coverurl)
        elif len(result) == 0:
            print('没有找到封面')
        else: 
            self.coverurl = result[0]
        
        result = re.findall(re.compile(r'href="(.*?video/.*?\.jpg)"'), self.html)
        self.sampleurllist = result

    def save_img(self):
        widgets = [
            self.name+'Progress: ',
            Percentage(), ' ',
            Bar('='), ' ',
            Timer(), ' '
        ]
        total = len(self.sampleurllist)+1
        bar = ProgressBar(widgets=widgets,maxval=10 * total).start()
        # 创建文件夹
        if not os.path.exists(self.path+self.name):
            os.mkdir(self.path+self.name)
            if self.coverurl != '':
                r = requests.get(javurl+self.coverurl, headers=self.headers)
                with open(self.path+self.name+'/'+self.name+'.jpg', 'wb') as f:
                    f.write(r.content)
                bar.update(10)
            if len(self.sampleurllist) != 0:
                for i in range(len(self.sampleurllist)):
                    r = requests.get(self.sampleurllist[i], headers=self.headers)
                    with open(self.path+self.name+'/'+self.name+'-'+str(i)+'.jpg', 'wb') as f:
                        f.write(r.content)
                    bar.update(10*(i+2))
                    time.sleep(delay)
        else:
            return '文件夹已存在'
            bar.update(10 * total)

        
        bar.finish()

    def deal(self):
        self.get_html()
        self.get_img()
        self.save_img()

class Star:
    def __init__(self, name):
        self.url = javurl+'star/'+name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.name = name   
        self.realname = ''     
        self.html = ''
        self.movielist = []
        self.coverlist = []
        self.path = allpath
        self.info = {}
    
    def get_html(self):
        try:
            r = requests.get(self.url, headers=self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            self.html = r.text
        except:
            return '产生异常'
    
    def get_info(self):
        # <span class="pb10">百永さりな</span>
        result = re.findall(re.compile(r'<span class="pb10">(.*?)</span>'), self.html)
        if len(result) == 1:
            self.realname = result[0]
        elif len(result) == 0:
            print('没有找到明星姓名')
        else: 
            self.realname = result[0]
        
        # print(self.realname,self.html)
        
        # <a class="movie-box" href="https://www.seejav.icu/SAN-085">
        info = re.findall(re.compile(r'<a class="movie-box"(.*?)</span>',re.S), self.html)
        # print(info)
        for i in info:
            # <img src="/pics/thumb/9f90.jpg"
            try:

                cover = re.findall(re.compile(r'<img src="(.*?)"'), i)[0].replace('/pics/thumb/', '/pics/cover/').replace('.jpg', '_b.jpg')
                # moviename <span>女好きの義理の父に寝取られて孕んでしまった人妻 百永さりな<br />
                # moviename = re.findall(re.compile(r'<span>(.*?)<br />'), i)
                # movie num <date>SAN-085</date>
                movienum = re.findall(re.compile(r'<date>(.*?)</date>'), i)[0]
                self.coverlist.append(cover)
                self.movielist.append(movienum)
                # 建立字典
                self.info[movienum] = cover
            except:
                pass

    def getallhtml(self):
        # 获取所有明星的html
        # <a href="/star/xl9/4">4</a> 
        # 正则表达式
        result = re.findall(re.compile(r'<a href=".*?/(\d|[1-9]\d|1[0-4]\d)">'), self.html)
        # 筛选出最大页数
        if len(result) == 0:
            print('没有找到页码')
        else:
            maxpage = int(result[-1])
            print("最大页码:"+str(maxpage))
            # 循环获取所有明星的html
            for i in range(2, maxpage+1):
                print('正在获取第'+str(i)+'页')
                url = javurl+'star/'+self.name+'/'+str(i)
                r = requests.get(url, headers=self.headers)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                self.html += r.text
                print('第'+str(i)+'页已保存')

    def saveall(self):
        # 保存所有明星的图片
        for i in self.movielist:
            print('正在保存'+str(self.movielist.index(i)),"共"+str(len(self.movielist))+"个")
            cart = Cart(i)
            cart.deal()

    def deal(self):
        self.get_html()
        self.getallhtml()
        # save html 
        with open(self.path+'/'+self.name+'.html', 'w', encoding='utf-8') as f:
            f.write(self.html)
        self.get_info()
        self.saveall()



if __name__ == '__main__':
    # import sys
    # # 从命令行获取参数
    # #parser = argparse.ArgumentParser()
    # allpath = "./"+sys.argv[1]+"/"
    # print(sys.argv[1])
    # # 路径不存在则创建
    # if not os.path.exists(allpath):
    #     os.mkdir(allpath)

    # star = Star(sys.argv[1])
    # star.deal()
    # print(star.info)

    html = requests.get('https://www.seejav.icu/AVOP-127').text
    with open('AVOP-127.html', 'w', encoding='utf-8') as f:
        f.write(html)


