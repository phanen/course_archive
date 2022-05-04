import urllib.request
import re
from tqdm import tqdm

def get_binary(url):
    """以二进制形式返回网页内资源"""
    with urllib.request.urlopen(url) as fp:
        content = fp.read()
    return content


def writer(filename, name, intro):
    """记录一位院士(包括姓名和介绍)"""
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(name + '\n')
        f.writelines(intro)
        f.write('\n*******************************\n')


def get_content(url):
    """获取网页所需内容"""
    html = get_binary(url).decode()
    # 每位院士介绍的网址和姓名是在一起的,可用一个正则同时获取
    # 所有院士html和名字的元组列表
    info_lst = re.compile(r'<a href="(.+?)" target="_blank">(.+?)</a>').findall(html)
    # 构造每位院士介绍信息的正则
    intro_rg1 = re.compile(r'<div class=\"intro\">((?:.|\n)*?)</div>')
    intro_rg2 = re.compile(r'<p>((?:.|\n)*?)</p>')
    # print(info_lst)
    for addr, name in tqdm(info_lst[:-1]):
        intro_1 = intro_rg1.findall(get_binary('http://www.cae.cn' + addr).decode())
        intro_2 = intro_rg2.findall(intro_1[0])
        # print(intro_2)
        # 介绍信息
        intro = ""
        for s in intro_2:
            intro = intro + s.replace("&ensp;", " ").replace("&nbsp;", "\n")
        # 写入文件
        writer('E:\pycode\工程院士信息.txt', name, intro)


if __name__ == '__main__':
    url = "https://www.cae.cn/cae/html/main/col48/column_48_1.html"
    get_content(url)
