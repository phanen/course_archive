if __name__ == '__main__':
    print([i for i in filter(lambda x: x == sum(i for i in range(1, x) if x % i == 0), range(1, 1000))])