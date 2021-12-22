def ways(n):
    if n == 1:
        return [(1,)]
    if n == 2:
        return [(1, 1), (2,)]
    if n == 3:
        return [(1, 1, 1), (1, 2), (2, 1), (3,)]
    res = []
    for i in (1, 2, 3):
        for way in ways(n - i):
            t = list(way)
            t.append(i)
            res.append(tuple(t))
    res.sort()
    return res


if __name__ == '__main__':
    print("5阶\n", ways(5))
    print("10阶\n", ways(10))
