import time

from tables import *
from tools import pad, hex2bin, bin2hex


def key_gen(K0: str):
    """初始密钥生成16轮子密钥 64->56->48(16个)"""
    ret = []
    sk = ""
    # 64 -> 56
    for i in range(56):
        sk += K0[PC1[i] - 1]

    # 生成 16个子密钥 56->48
    for r in range(16):
        c = sk[0:28]
        d = sk[28:]
        # 循环移位
        if r in {0, 1, 8, 15}:
            c_ = c[1:] + c[0]
            d_ = d[1:] + d[0]
        else:
            c_ = c[2:] + c[0:2]
            d_ = d[2:] + d[0:2]
        sk = c_ + d_
        sk_ = ""
        for i in range(48):
            sk_ += sk[PC2[i] - 1]
        ret.append(sk_)
    return ret


def e_box(b: str):
    """E 拓展 32->48"""
    return b[-1] + b[0:5] + b[3:9] + b[7:13] + b[11:17] + b[15:21] + b[19:25] + b[23:29] + b[27:32] + b[0]


def s_box(b: str):
    """S 混淆 48->32"""
    ret = ""
    for i in range(8):
        addr = 6 * i
        row_index = int(b[addr:addr + 6][0] + b[addr:addr + 6][-1], 2)
        col_index = int(b[addr:addr + 6][1:-1], 2)
        tmp = bin(
            S_TABLE[i][row_index][col_index]
        )[2:]
        ret += pad(tmp, 4)
    return ret


def p_box(b: str):
    """P 置换 """
    ret = ""
    for i in range(len(b)):
        ret += b[P_TABLE[i] - 1]
    return ret


def f_op(A, J):
    """f函数"""
    eA = e_box(A)
    tmp = bin(int(eA, 2) ^ int(J, 2))[2:]
    ret = p_box(
        s_box(
            pad(tmp, 48)
        )
    )
    return ret


def round_fuc(L: str, R: str, K: str, LAST_ROUND: bool = False) -> str:
    """轮函数 32 32"""
    tmp = bin(int(L, 2) ^ int(f_op(R, K), 2))[2:]
    tmp = pad(tmp, 32)
    return tmp + R if LAST_ROUND else R + tmp


def DEC_encrypt(plain: str, keys: list) -> str:
    """ DEC 加密"""
    # IP置换
    cipher = ""
    for i in range(len(IP)):
        cipher += plain[IP[i] - 1]

    # 迭代加密
    for r in range(16):
        L = cipher[0:32]
        R = cipher[32:]
        cipher = round_fuc(L, R, keys[r], r == 15)
    # IP逆置换
    ret = ""
    for i in range(len(IP_REVERSE)):
        ret += cipher[IP_REVERSE[i] - 1]
    return ret


def main1():
    plain = hex2bin("02468aceeca86420")
    key = hex2bin("ff14717847d8e859")
    # plain = hex2bin("0012345678912323")
    # key = hex2bin("133457799bbcdff1")
    keys = key_gen(key)
    cipher = DEC_encrypt(plain, keys)
    re_plain = DEC_encrypt(cipher, list(reversed(keys)))
    print(f"{bin2hex(plain)}-->{bin2hex(cipher)}-->{bin2hex(re_plain)}")
    print([bin2hex(i) for i in keys])


def main2():
    """测试时间"""
    # 只用一个密钥
    key = hex2bin("133457799bbcdff1")
    keys = key_gen(key)
    cnt = 0
    t1 = time.time()
    with open("testbench.txt", "r") as f:
        for plain_ in f:
            cipher = DEC_encrypt(
                pad(
                    bin(int(plain_))[2:], 64
                ), keys)
            print(cipher, cnt)
            cnt += 1
    t2 = time.time()
    print(f"Time measured: {t2 - t1}");


def main3():
    """Test"""


if __name__ == '__main__':
    # main1()
    main2()
