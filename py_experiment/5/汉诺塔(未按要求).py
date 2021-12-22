def hanoi(n, a, b, c):
    """
    :param n: 阶数
    :param a: 源底座名
    :param b: 临时底座名
    :param c: 目标底座
    """
    s = {"name": a, "num": n}
    v = {"name": b, "num": 0}
    d = {"name": c, "num": 0}
    move(n, s, v, d)


def move(n, s, v, d):
    """路径"""
    if n == 0:
        return
    move(n - 1, s, d, v)
    s["num"] -= 1
    d["num"] += 1
    print(f"移动:{s['name']}->{d['name']}\t分布:", (s["num"], v["num"], d["num"]))
    move(n - 1, v, s, d)


if __name__ == '__main__':
    hanoi(4, "A", "B", "C")
