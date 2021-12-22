def s(n):
    return 1 if n == 1 else \
            2 if n == 2 else \
            4 if n == 3 else \
            s(n - 1) + s(n - 2) + s(n - 3)


if __name__ == '__main__':
    print([s(i) for i in range(1, 30)])
