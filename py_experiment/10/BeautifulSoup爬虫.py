from bs4 import BeautifulSoup  # 一个可以从HTML或XML文件中提取数据的Python库
import requests, lxml, re, sys


def writer(filename, name, intro):
    """记录一位院士(包括姓名和介绍)"""
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(name + '\n')
        f.writelines(intro)
        f.write('\n*******************************\n')


def main():
    # 获取html
    html = requests.get(url='http://www.cae.cn/cae/html/main/col48/column_48_1.html').text
    # 要找从下面中找到li标签
    li_bf = BeautifulSoup(html, features="html.parser")  # html.parser
    # 获取所有li标签的迭代器
    li = li_bf.find_all('li', class_='name_list')
    # 记录人数
    nums = len(li)
    # 对每一个li标签
    info_lst = []
    for each in li:
        # 从里面找a标签
        a_bf = BeautifulSoup(str(each), features="lxml")
        # 只有一个a标签
        a = a_bf.find_all('a')[0]
        # 获取链接和名字
        info_lst.append(('http://www.cae.cn' + a.get('href'), a.string))
    # print(info_lst)
    for url, name in info_lst:
        sub_html = requests.get(url).text
        bf = BeautifulSoup(sub_html, features="lxml")
        div = bf.find_all('div', class_='intro')
        p_bf = BeautifulSoup(str(div[0]), features="lxml")
        p = p_bf.find_all('p')  # 若干<p>…</p>
        intro = ''
        for each in p:
            intro += each.text
        writer('工程院士信息.txt', name, intro)


if __name__ == '__main__':
    main()
