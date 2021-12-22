# 猜数游戏，编写程序模拟猜数游戏。程序运行时，系统生成一个100以内的随机数，
# 然后提示用户进行猜测，并根据用户输入进行必要的提示（猜对了、太大了、太小了），
#   如果猜对则提前结束程序，
#   如果次数用完仍没有猜对，提示游戏结束并给出正确答案。
# 要求用到异常处理，处理输入不是数字的情况。
import random

if __name__ == '__main__':
    num = random.randint(0, 99)  # 生成随机数
    ct = 7  # 机会
    while True:
        try:
            guess = int(input(f"输入100以内的非负整数(十进制)，还剩{ct}次机会\n"))
            if guess > num:
                print("太大了")
            elif guess < num:
                print("太小了")
            else:
                print("猜对了")
                break
            ct -= 1
            if ct == 0:
                print(f"答案是{num}")
        except ValueError:
            print("输入的不是十进制数字")
            break
