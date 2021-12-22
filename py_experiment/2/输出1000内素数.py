import math


def is_prime(n: int) -> bool:
    """模6既约剩余系优化的试除法"""
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def prime_in(n: int) -> list:
    """返回包含n内的所有素数的列表"""
    return [i for i in range(2, n) if is_prime(i)]


def get_primes(n):
    """获取小于n的素数"""
    org = [True] * n
    org[:2] = False, False
    for i in range(2, int(math.sqrt(n)) + 1):
        if org[i]: org[i * i::i] = [False] * len(org[i * i::i])
    return [idx for idx, i in enumerate(org) if i]


if __name__ == '__main__':
    print(get_primes(1000))
