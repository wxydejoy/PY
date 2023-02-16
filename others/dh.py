import requests
from selenium import webdriver
import re
from time import sleep

browser = webdriver.Chrome()


# https://dp2212.xyz/pw/thread1022.php?fid=3&type=2&page=2

page = 2


url = "https://dp2212.xyz/pw/thread1022.php?fid=3&type=2&page=" + str(page)
# print(url)


html = requests.get(url).text
# with open('dp2212.html', 'w', encoding='utf-8') as f:
#     f.write(html)
# print(html)
# <a href="html_data/3/2301/6450950.html" id="a_ajax_6450950"><font color="#008080">★●最新の國產無碼㊣↗️精彩合集↘️♀ [01.23]</font></a>

info = re.findall(re.compile(r'<a href="(.*?)".*color=#008080>'), html)
print(info)


for i in info:
    # 新标签页打开
    browser.execute_script("window.open('https://dp2212.xyz/pw/" + i + "')")

    # 保持
sleep(1000000)