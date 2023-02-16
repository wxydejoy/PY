import threading
import requests
 
iptv_list = ['cctv{}'.format(i) for i in range(1, 13)]
other_list = ['北京卫视', '江苏卫视', '浙江卫视', '东方卫视', 
                '东南卫视', '黑龙江卫视','安徽卫视', '广东卫视', '山东卫视', '湖北卫视', '四川卫视', '天津卫视', '河北卫视', '深圳卫视']
iptv_list += other_list
print(iptv_list)
 
result = {}
 
 
# 使用正则表达式提取IPTV list
def get_iptv_list_by_regex(target):
    print(target)
    import re
    url = 'https://www.foodieguide.com/iptvsearch/?s={}'.format(target)
    r = requests.get(url)
    # pattern = re.compile(r'<a href="(.*?)" title="(.*?)">')
    pattern = re.compile(r'http://.*?\.m3u8')
    # print(target,pattern.findall(r.text)[:2])
    # 将结果保存到字典中
    resultlist = []
    for i in pattern.findall(r.text):
        try:
            if test_iptv_link(i) == 200:
                result[target] = i
                print(i,target)
                break
        except Exception as e:
            print(e)
            continue
    # result[target] = pattern.findall(r.text)[0]
    return
    # /^https?:\/\/(.+\/)+.+(\.(swf|avi|flv|mpg|rm|mov|wav|asf|3gp|mkv|rmvb|mp4))$/i
 
# 测试链接是否可用
 
 
def test_iptv_link(link):
    import requests
    r = requests.get(link)
    return r.status_code


# 多线程获取链接


# def get_iptv_list_by_thread(iptv_list):
#     threads = []
#     for i in range(0, len(iptv_list)):
#         t = threading.Thread(target=get_iptv_list_by_regex,args=(iptv_list[i],))
#         threads.append(t)
#     for t in threads:
#         t.start()
#     for t in threads:
#         t.join()
#     return threads
for i in iptv_list:
    try:
        get_iptv_list_by_regex(i)
    except Exception as e:
        print(e)
        continue
    
# get_iptv_list_by_thread(iptv_list)
print(result)
# 将字典以m3u格式写入文件
with open('iptv.m3u', 'w') as f:
    for key in result:
        f.write('#EXTINF:-1 ,{}\n'.format(key))
        f.write(result[key])
        f.write('\n')
f.close()