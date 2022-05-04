import string, random
import time


def gen_pwd(l: int = 8) -> str:
    """生成l位密码"""
    s1 = string.digits
    s2 = string.punctuation
    s3 = string.ascii_letters
    s = s1 + s2 + s3
    lst = []
    for i in range(16):
        lst.append(s[random.randint(0, len(s) - 1)])
    return "".join(lst)


def is_strong_pwd(pwd: str) -> bool:
    """检测密码强度"""
    f1, f2, f3 = False, False, False
    for c in pwd:
        if c in string.digits:
            f1 = True
            continue
        if c in string.ascii_letters:
            f2 = True
            continue
        if c in string.punctuation:
            f3 = True
            continue
    return f1 and f2 and f3


if __name__ == '__main__':
    random.seed(time.time())
    for i in range(10):
        pwd = gen_pwd(8)
        print(pwd, "是" if is_strong_pwd(pwd) else "不是", "\t强密码")  # 生成并打印八位随机密码以及其强度
