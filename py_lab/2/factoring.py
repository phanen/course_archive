#
# for i in range(1, 10):
#     print("x_i &\equiv a_{1,%d}\log_g{p_1} + a_{2,%d}\log_g{p_2} + \cdots + a_{b,%d}\log_g{p_b} \pmod{p - 1}" % (i, i, i))
import random

# for _ in range(128):
#     print("#10\t a <= {:2};\t b <= {:2};".format(random.randint(-8, 7), random.randint(-8, 7)))

def printQueen():
    print(queen)
    for i in range(8):
        for j in range(8):
            if queen[i][j] == 1:
                print('☆ ' * j + '★ ' + '☆ ' * (7 - j))
    print("\n\n")


def check(row, column):
    # 检查行列
    for k in range(8):
        if queen[k][column] == 1:
            return False
            # 检查主对角线
    for i, j in zip(range(row - 1, -1, -1), range(column - 1, -1, -1)):
        if queen[i][j] == 1:
            return False
            # 检查副对角线
    for i, j in zip(range(row - 1, -1, -1), range(column + 1, 8)):
        if queen[i][j] == 1:
            return False
    return True


def findQueen(row):
    if row > 7:
        global count
        count += 1
        printQueen()
        return
    for column in range(8):
        if check(row, column):
            queen[row][column] = 1
            findQueen(row + 1)
            queen[row][column] = 0


if __name__ == '__main__':
    count = 0
    queen = [[0 for i in range(8)] for i in range(8)]
    findQueen(0)
    print("满足要求的摆法总数:", count)
