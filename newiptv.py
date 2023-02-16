
import requests
import re
import threading

import os

iptv_list = ['cctv{}'.format(i) for i in range(1, 13)]
other_list = ['北京卫视', '江苏卫视', '浙江卫视', '东方卫视', 
                '东南卫视', '黑龙江卫视','安徽卫视', '广东卫视', '山东卫视', '湖北卫视', '四川卫视', '天津卫视', '河北卫视', '深圳卫视']
iptv_list += other_list


# 请求 URL: https://www.foodieguide.com/iptvsearch/
# 请求方法: POST
# 状态代码: 200 
# search=%E6%B5%99%E6%B1%9F%E5%8D%AB%E8%A7%86%E9%AB%98%E6%B8%85&Submit=+


def get_iptv_list_by_regex(target):
    print(target)
    url = 'https://www.foodieguide.com/iptvsearch/'
    data = {
        'search': target,
        'Submit': ' '
    }
    r = requests.post(url, data=data)
    pattern = re.compile(r'http://.*?\.m3u8')
    resultlist = []
    findall = pattern.findall(r.text)
    # for i in findall:
    #     # print(pattern.findall(r.text))
    #     print("正在测试",findall.index(i)+1,"/",len(findall),i)
    #     try:
    #         if requests.get(i) == 200:
    #             resultlist.append(i)
    #             print(i,target)
    #     except Exception as e:
    #         print(e)
    #         continue
    # 判断文件是否存在，存在则删除


    with open('iptv.m3u', 'a+') as f:
        for key in findall:
            if discernVedio(key):
                f.write('#EXTINF:-1 ,{}\n'.format(target))
                f.write(key)
                f.write('\n')
    return 



# 测试链接是否可用


def discernVedio(url): 
    print("正在测试",url)
    try:
        with requests.get(url, verify = False,timeout=1) as file:
            if file.headers.get('Content-Length') not in ['0', 'None']:
                return True
            else:
                return False
    except BaseException as err:
        print(err)
        return False






if __name__ == '__main__':
    result = {}
    if os.path.exists('iptv.m3u'):
        os.remove('iptv.m3u')
    for i in iptv_list:
        get_iptv_list_by_regex(i)
    # print(discernVedio('http://hwrr.jx.chinamobile.com:8080/PLTV/88888888/224/3221225618/index.m3u8'))
    # print(requests.get('http://hwrr.jx.chinamobile.com:8080/PLTV/88888888/224/3221225618/index.8', verify = False).headers.get('Content-Length'))