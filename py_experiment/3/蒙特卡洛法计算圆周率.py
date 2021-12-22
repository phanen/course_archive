import math
import random

# 基本思路
# 在平面坐标系中取一区域作为正方形
# 每次在正方形内随机取一个点（先后获取两个随机数，分别作为横坐标和纵坐标）
# 由于python内置了获取0~1的随机小数的函数random.random()
# 因此可以取正方形面积为4（边长2），圆的半径为1
# 由对称性，只在第一象限（如题）随机取点，讨论内是否落在四分之一圆内即可

if __name__ == '__main__':
    count = 0
    n = 10000
    for i in range(n):
        # 在第一象限的正方形内随机取点
        x = random.random()  # 横坐标
        y = random.random()  # 纵坐标
        # 是否在四分之一圆内
        if x * x + y * y <= 1:
            count += 1
    print(4 * count / n)
    print(math.pi)
