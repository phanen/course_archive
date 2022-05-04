import urllib.request
import re

target = 'http://tieba.baidu.com/p/2460150866'

# 构造图片url的正则表达式
pic_pattern = re.compile(r'class="BDE_Image"\ssrc="(.+?\.jpg)"')
with urllib.request.urlopen(url=target) as fp:
    # 得到网页html源码
    html = fp.read().decode()
# 所有图片链接
pic_url_lst = pic_pattern.findall(html)
print(pic_url_lst)
for i, pic_url in enumerate(pic_url_lst):
    # 访问每个图片地址
    with urllib.request.urlopen(url=pic_url) as fp:
        # 获取内容
        pic_content = fp.read()
        # 注意py3要用wb模式打开
        with open(f"E:\pycode\pic\{i}.jpg", "wb") as f:
            # 以图片原本格式写到自定义的路径下新建的文件中
            f.write(pic_content)
            print(f"第{i + 1}个图片下载成功....")
