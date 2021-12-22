# 基本思路
# 0. 输入今天的年份、月份、日期
# 1. 判断今年是平年还是闰年(2月有28天还是29天)
# 2. 存储12个月份各自对应天数的列表
# 3. 今天的天数就是累加当前月份前每一个月的天数和和当月的日期
import time
from functools import reduce


def sys_day_of_year():
    return time.localtime(time.time()).tm_yday


def day_of_year():
    """判断今天是今年的第几天"""
    # 获取日期
    now = list(map(int, input("年 月 日:").split(" ")))
    print(now)
    # 月份表
    m = [0] * 12
    for i in (1, 3, 5, 7, 8, 10, 12):
        m[i - 1] = 31
    for i in (4, 6, 9, 11):
        m[i - 1] = 30
    # 二月天数特判
    m[2 - 1] = 29 if (now[0] % 400 == 0 or (now[0] % 100 != 0 and now[0] % 4 == 0)) else 28
    print(m)
    return now[2] if now[1] == 1 else reduce(lambda x, y: x + y, m[:now[1] - 1]) + now[2]


if __name__ == '__main__':
    print("系统获取的当地时间(今年的天数):\n", sys_day_of_year())
    print("判断函数的返回结果:\n", day_of_year())
