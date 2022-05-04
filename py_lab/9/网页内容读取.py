import urllib.request


# # 存储url对象的列表
# lst = ["bilibili", "baidu"]
# fp = urllib.request.urlopen(r'http://www.bilibili.com')
# # 打印读取的内容
# # 打开bilibili报错：urllib.error.HTTPError: HTTP Error 403: Forbidde
# for name in lst[1:]:
#     print(f"--------------website: {name}-----------")
#     # 请求获取网站内容
#     fp = urllib.request.urlopen(r"https://www." + name + ".com")
#     # 网站内容打印
#     print(fp.read().decode())
#     fp.close()


# 解决403
def get_ctt(url):
    headers = {
        'User-Agent': 'mozilla/5.0 (windows nt 6.1; wow64) applewebkit/537.36 (khtml, like gecko) chrome/27.0.1453.94 safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    with urllib.request.urlopen(req) as f:
        ctt = f.read().decode('utf-8')
    return ctt


print(get_ctt(r"https://www.bilibili.com"))
