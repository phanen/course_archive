from hashlib import md5
from string import ascii_letters, digits
from itertools import permutations

# 基本思路
# 遍历5-10个英文或者数字字符组成的所有字符串
# 分别计算每个字符串的md5值,转化为十六进制字符串,与密文进行比对
# 若发现与密文相同的字符串,那么明文就是该md5值对应的原字符串
# 利用permutation的代码实现逻辑基于明文无重复字符的前提
# 若明文有重复字符，那么应采用可重复的排列（在itertools有相关函数，可类似地实现）


if __name__ == '__main__':
    s = 0
    my_dic = ascii_letters + digits
    ciphertxt = '23eeeb4347bdd26bfc6b7ee9a3b755dd'
    for length in range(5, 11):
        for x in permutations(my_dic, length):
            s = "".join(x)
            if md5(s.encode()).hexdigest() == ciphertxt:
                print("明文是:", s)
                exit(0)