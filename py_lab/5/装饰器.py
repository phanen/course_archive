import time


def timer(func):
    def inner(*args, **kwargs):
        start = time.time()
        o = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return o

    return inner


@timer
def func1():
    time.sleep(0.5)
    print('in func1')


@timer
def func2(a, b, c):
    print("abc")
    return a, b, c


if __name__ == '__main__':
    func1()
    print(func2(1, "aa", {3: [12, 21]}))
