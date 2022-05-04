import math
import random


def gcd(a, b):
    """最大公因子"""
    if b == 0:
        return a
    return gcd(b, a % b)


def exgcd(a, b):
    """拓展Euclid算法"""
    if b == 0:  # 平凡情形
        return 1, 0, a
    else:
        y, x, q = exgcd(b, a % b)
        y -= (a // b) * x
        return x, y, q


def invmod0(a, m):
    """求 a 模 m 的 逆"""
    return None if gcd(a, m) != 1 else exgcd(a, m)[0]


def invmod(a, m):  # 扩展欧几里得
    if gcd(a, m) != 1:
        return None  # 如果a和m不互质，则不存在模逆
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3  # //是整数除法运算符
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def powmod(a, n, m):
    """快速幂"""
    a = a % m
    prod = 1
    while n != 0:
        if n & 1:
            prod = (prod * a) % m
        n //= 2
        a = (a * a) % m
    return prod


def rabin_miller(p, times=10):
    """判断p是否为素数 times为测试次数"""
    # 小素因子检验
    if not p & 1: return False
    for d in [3, 5, 7, 11, 13, 17, 19, 23, 29,
              31, 37, 41, 43, 47, 53, 59, 61, 67, 71]:
        if p % d == 0:
            return False
    # 计算 b 和奇数 m 使得 p = 1 + 2^b * m
    b, m = 0, p - 1
    while m & 1 == 0:
        m >>= 1
        b += 1
    StrongLiar = 1
    for trials in range(times):
        a = random.randrange(2, p)
        z = powmod(a, m, p)
        if z != 1:
            i = 0
            while z != p - 1:  # 一旦一个不等式不成立将失去合数凭证
                if i == b - 1:  # 表明所有的不等式均成立
                    return False
                else:
                    i += 1
                    z = (z ** 2) % p
    # 素数伪证, 多次检测后都没确定为合数
    return True


def prime_gen(lb, ub, judge=rabin_miller, times=10):
    """生成 在lb到ub(不含ub) 的大素数"""
    p = random.randrange(lb, ub)
    while not judge(p, times=times):
        p = random.randrange(lb, ub)
    return p


def is_prime(p):
    """小素数检测"""
    if not p & 1:  # 偶数
        if p == 2:
            return True
        return False  # 不是2

    # 小素数列表筛
    prime_lst = [2, 3, 5]
    step = 2

    for d in prime_lst[1:]:
        if p == d:
            return True
        if p % d == 0:
            return False
        step *= d

    # 既约剩余系筛
    step_lst = list([True] * (step + 1))
    for d in prime_lst:
        step_lst[d::d] = [False] * len(step_lst[d::d])
    idx = 2
    rmd_lst = []
    for is_rmd in step_lst[idx:]:
        if is_rmd:
            rmd_lst.append(idx)
        idx += 1

    # 差分列
    dlt = [rmd_lst[i] - rmd_lst[i - 1] for i in range(1, len(rmd_lst))]
    dlt.append(1 + step - rmd_lst[-1])
    dlt.append(rmd_lst[0] - 1)
    v = rmd_lst[0]
    # print(step_lst)
    # print(rmd_lst)
    # print(dlt)
    while v < math.floor(math.sqrt(p)) + 1:
        for move in dlt:
            if p % v == 0:
                return False
            v += move
            # print(v)
    return True


def is_raw(p):
    for i in range(2, math.floor(math.sqrt(p)) + 1):
        if p % i == 0:
            return False
    return True


def rsa_key_gen(bit=1024):
    """RSA公钥私钥生成"""
    lb = 2 ** (bit - 1)
    ub = lb * 2
    p = prime_gen(lb, ub)
    q = prime_gen(lb, ub)
    n = p * q
    phi = n - p - q + 1
    e = 65537
    d = invmod(e, phi)
    return (n, e), (n, d)


def rsa_encrypt(c, key: tuple):
    """key = (n, e)"""
    n, e = key
    return powmod(c, e, n)


def rsa_decrypt(m, key: tuple):
    n, d = key
    return powmod(m, d, n)


# 测试素性检测
lst = [
    115921,
    252601,
    72934879102271241648426492271730744633800277079752665073951,
    22356556428347371191698399214467787018791948334691697578290577962216876499377539334483720552975347714328452036074010604373528959269622147129120835027063319925220078829082931022948650474024417050974139419013871612480613081473425031484830581421090988945262028469222454196445529288787619959670372054180614638559,
    59781728296291796158017561748790663563089826605613453665484905474067787844371928298271399443627910058186271964388689059202384502829570397941413694221362295301992777901316834935383384311335512396099609207669093853533128308369361287391546232562965636847929476475654404583285950058456806751391620048033664557683,
    28494763464967883432404625600246500270772945929877245405931752469865039864230821468097563814857376172612971356800192745072503914472425803446304874347819820876404436537980316277614506865977235566602316683632497367119801578047171561102922761465857684859995527428337609809476794854474027492330502370339054042789
]


def rsa_test():
    lb = 2 ** 50
    ub = 2 * lb
    for i in range(10):
        public_key, private_key = rsa_key_gen()
        c = random.randrange(lb, ub)
        # c = 465312246587465132548465132154896581
        # print(c)
        m = rsa_encrypt(c, public_key)
        cc = rsa_decrypt(m, private_key)
        if cc != c:
            return False
    return True


print(rsa_test())
print("end")
