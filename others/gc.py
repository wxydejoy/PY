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
        self.title = re.findall(re.compile(r'<title>(.*?)</title>', re.S), html)[0].replace("黑料网 - ", "")
        # with open(self.title.replace("/","")+'zztt453.html', 'w', encoding='utf-8') as f:
        #     f.write(html)
        if not ("学" in self.title or "学生" in self.title or "吞" in self.title ):
            return False
        if html:

            info = re.findall(re.compile(r'"video":{"url":"(.*?)",', re.S), html)

            if info:
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
            print('请求页面成功', url)
            return response.text
        return None
    except requests.RequestException as e:
        print('请求页面出错', url, e.args)
        return None


def page(num):
    url = 'https://d2hf.dqtse.com/category/0/'+str(num)+'.html'
    html = get_page(url)
    # with open('zztt45.html', 'w', encoding='utf-8') as f:
    #     f.write(html)
    info = re.findall(re.compile(r'(/archives/.*?.html)',re.S), html)
    # with open('zztt45.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(info))

    for i in info:
        # log
        print("page", num)
        title = "https://d2hf.dqtse.com" + i
        

        art = ART(title, title)
        if art.check():
            artlist.append(art)
            with open('zztt453.txt', 'a', encoding='utf-8') as f:
                f.write(art.url +"\t\t\t "+art.title+ "\r\n")


if __name__ == '__main__':
    # art = ART('警花', 'https://zztt45.com/archives/16278.html')
    # art.check()
    for i in range(271, 471):
        artlist.clear()
        try:
            page(i)
        except Exception as e:
            print(e.args)
            continue

