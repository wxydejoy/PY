# hellowgithub.py
# 整理hellogithub的内容，按语言分类

import os
import re



# md 文件夹路径 HelloGitHub\content
# 读取md文件夹下的所有文件
# 读取文件内容


# 读取文件内容
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# 读取文件夹下的所有文件
def read_dir(dir_path):
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if os.path.splitext(file)[1] == '.md':
                file_list.append(os.path.join(root, file))
    return file_list




def savaefile(t):
    if not os.path.exists("./hello/A"+t.split("\n")[0]+".md"):
        with open("./hello/A"+t.split("\n")[0]+".md", 'w+', encoding='utf-8') as f:
            f.write(str(t.removeprefix(t.split("\n")[0])))
    else:
        with open("./hello/A"+t.split("\n")[0]+".md", 'a+', encoding='utf-8') as f:
            f.write(str(t.removeprefix(t.split("\n")[0])))
    return




def clearfile():
    if os.path.exists("./hello"):
        # 删除文件
        for root, dirs, files in os.walk("./hello"):
            for file in files:
                if os.path.splitext(file)[1] == '.md':
                    os.remove(os.path.join(root, file))
    return



if __name__ == '__main__':
    # md 文件夹路径
    dir_path = 'HelloGitHub\content'
    # # 读取md文件夹下的所有文件
    file_list = read_dir(dir_path)
    # print(file_list)
    # # 读取文件内容
    for file in file_list:
        content = read_file(file)
        rule = re.compile(r'###(.*?)<br>',re.S)
        result = rule.findall(content)
        for i in result:
            savaefile(i)

    # # 读取文件内容
    # file_path = 'HelloGitHub\content\HelloGitHub19.md'
    # content = read_file(file_path)
    # # print(content)

    # # 正则匹配
    # # ### <br>

    #     # print(i)
    #     # print('-----------------------')
    # clearfile()
