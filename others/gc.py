# https://zztt45.com/page/1/

import requests


import re

artlist = []


class ART():
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.lenth = 0

    def check(self):
        # 检测页面内是否有长视频     有则返回True

        html = get_page(self.url)

        if html:
            # with open('zztt45pp.html', 'w', encoding='utf-8') as f:
            #     f.write(html)
            # re 匹配 m3u8
            info = re.findall(re.compile(r'"video":{"url":"(.*?)","pic":"","type":"auto"', re.S), html)

            if info:
                # print(info)
                # m3u8
                content = requests.get(info[0].replace('\\', '')).text
                lenth = len(re.findall(re.compile(r'#EXTINF', re.S), content))
                if lenth/12 > 3:
                    self.lenth = lenth/12
                    print(self.title, self.url, lenth/12)
                    return True
                







def get_page(url):
    # print(url)
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException as e:
        print('请求页面出错', url, e.args)
        return None


def page(num):
    url = 'https://zztt45.com/page/'+str(num)+'/'
    html = get_page(url)
    # with open('zztt45.html', 'w', encoding='utf-8') as f:
    #     f.write(html)
    info = re.findall(re.compile(r'<meta itemprop="url mainEntityOfPage" content=(.*?)<div class="post-card-info">',re.S), html)
    # with open('zztt45.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(info))

    for i in info:
        title = re.findall(re.compile(r'<h2 class="post-card-title" itemprop="headline">(.*?)</h2>', re.S), i)
        # content="https://zztt45.com/archives/16271.html"
        url = re.findall(re.compile(r'<a href="(.*?)" >\r\n', re.S), i)
        if ("wraps" not in title[0]) :
            if '大学' in title[0] or '生' in title[0]:
                # print(title, url)
                art = ART(title[0], url[0])
                if art.check():
                    artlist.append(art)
                
    with open('zztt45.txt', 'a', encoding='utf-8') as f:
        for i in artlist:
            f.write(str(i.title) + " --------- " + str(i.url) + " -- " +str(i.lenth) +"\r\n")
        



if __name__ == '__main__':
    # art = ART('警花', 'https://zztt45.com/archives/16278.html')
    # art.check()
    for i in range(170, 370):
        artlist.clear()
        try:
            page(i)
        except Exception as e:
            print(e.args)
            continue