# 基本思路：
# 用state元组存放棋子的摆放方式，state元素的索引值是行，元素的值是列号(均为0~7)
# 递归函数queens的作用是回state状态下剩余棋子所有摆放的方式
# 每次在新行中寻找棋子，遍历所有列试图放置棋子，并判断是否与已经摆放好的棋子发生冲突
#   冲突检测：当前棋子是否与已经摆放好的棋子位于同一列或者同一对角线(行是新取的不会冲突)
#       如果冲突继续遍历，否则就摆放棋子：
#           如果这是最后一个要摆放的棋子：直接返回当前棋子摆放的位置
#           如果不是最后一个，摆放棋子更新状态，递归解决剩余的棋子摆放


def queens_yield(n=8):
    """用yield解决八皇后问题"""

    def conflict(state, nextX):
        """在新的一行的nextX列放一枚棋子，判断是否与其他棋子位置冲突"""
        nextY = len(state)  # 新取一行
        for i in range(nextY):  # 遍历摆放好的棋子
            if abs(state[i] - nextX) in (0, nextY - i):  # 列冲突或对角线冲突
                return True
        return False

    def queens(num=n, state=()):
        """返回state状态下剩余棋子所有摆放的方式"""
        for pos in range(num):  # 在新行中找一列
            if not conflict(state, pos):  # 当选取的位置不冲突时
                if len(state) == num - 1:  # 如果就剩最后一行，那么这个位置就是剩余的摆放方式
                    yield pos,
                else:  # 如果不是就剩最后一行，在这里放置棋子，更新state进行递归
                    for result in queens(num, state + (pos,)):
                        yield (pos,) + result

    res = list(queens(n))
    print("解数：%d \n解：%s" % (len(res), res))


def queens_no_yield(n=8):
    """不用yield"""

    def conflict(state, nextX):
        """在新的一行的nextX列放一枚棋子，判断是否与其他棋子位置冲突"""
        nextY = len(state)  # 新取一行
        for i in range(nextY):  # 遍历摆放好的棋子
            if abs(state[i] - nextX) in (0, nextY - i):  # 列冲突或对角线冲突
                return True
        return False

    def queens(num=n, state=()):
        """返回state状态下剩余棋子所有摆放的方式"""
        lst = []
        for pos in range(num):  # 在新行中找一列
            if not conflict(state, pos):  # 当选取的位置不冲突时
                if len(state) == num - 1:  # 如果就剩最后一行，那么这个位置就是剩余的摆放方式
                    lst.append((pos,))
                else:  # 如果不是就剩最后一行，在这里放置棋子，更新state进行递归
                    for result in queens(num, state + (pos,)):
                        lst.append((pos,) + result)
        return lst

    res = list(queens(n))
    print("解数：%d \n解：%s" % (len(res), res))


if __name__ == '__main__':
    # queens_yield(8)
    queens_no_yield(8)
