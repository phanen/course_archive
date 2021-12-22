def calc_():
    s, ct, a = 0, 0, 0
    while True:
        num = yield a
        ct += 1
        s += num
        a = s / ct


# 使用yield from
def use_yield_from():
    while True:
        yield from calc_()


def calc_process():
    print("输入数字计算平均值, 输入非数字终止(十进制)")
    calc = use_yield_from()
    next(calc)  # 预激
    while True:
        try:
            print(calc.send(float(input())))
        except ValueError:
            print("终止")
            break


if __name__ == '__main__':
    calc_process()
