import numpy as np

# 创建不同维度的数组
# 普通方式
# a = np.array([[[1, 2, 3, 4], [5, 6, 7, 8]], [[0, 0, 0, 0], [9, 9, 9, 9]]])
# # 利用arange()
# b = np.arange(0, 16, 3)
# # 利用arange()和reshape()
# c = np.arange(0, 32).reshape(4, 8)
# print(a)
# print(b)
# print(c)
# print(a.ndim, b.ndim, c.ndim)


# # # 其他
# print(np.ones((2, 3, 4), dtype=np.int8))
# print(np.zeros((2, 3, 4), dtype=np.int8))
# print(np.empty((2, 3, 4), dtype=np.int8))
# print(np.random.randint(0, 9, (3, 4)))
# print(np.random.rand(3, 4))
# print(np.random.randn(3, 4))
# print(np.linspace(-2, 2, 10))


# # 索引
# print(c[1])
# print(c[0][1])
# print(c[0, 1])
# print(c[0][:])
# print(c[0, :])
# print(c[0][1:3])
# print(c[:][0])
# print(c[:, 0])

# # 整数索引
# # 行列索引均离散值时，只选取对应交叉元素
# print(c[[0, 1, 2, 3], [0, 1, 2, 3]])
# # 至少有一个是"连续值"时，选取的是所有交叉元素
# print(c[[1, 3], 1:4])
# print(c[1:3, [1, 3]])
# print(c[1:3, 1:7])
# # 笛卡尔积索引
# print(c[np.ix_([0, 2], [1, 2, 3])])

# # 布尔索引
# print(c[[True, False, False, True]])
# # 方阵才行？
# print(c[:, 4:][[True, True, False, True], [True, True, False, True]])
# print(c[c^2 + 5 > 20])
# # 机理揭示
# names = np.array(['Bob', 'Tom', 'Joy', 'Bob', 'Mark'], dtype='<U4')
# data = np.array([[0.53907488, 0.08239029, 0.49606765, 0.84466126, 0.78326342],
#                  [0.64214005, 0.2917917, 0.96583067, 0.377151, 0.34873902],
#                  [0.82531799, 0.61300945, 0.58824431, 0.16859125, 0.42529735],
#                  [0.96789188, 0.08368161, 0.25979403, 0.95384036, 0.77921917],
#                  [0.83331394, 0.60851424, 0.10917665, 0.04371444, 0.6726732]])
# print("========== all man ==========")
# print(names)
# print("========== all data ==========")
# print(data)
# print("========== Tom\'s data ==========")
# print(names == "Tom")  # [False  True False False False]
# print(data[names == 'Tom'])
# print("========== Bob\'s data ==========")
# print(data[names == 'Bob'])
# print("========== Tom\'s first and second data ==========")
# print(data[names == 'Tom', :2])  # 与切片配合
# print("========== data except Tom\'s ==========")
# print(data[names != 'Tom'])
# print(data[~(names == 'Tom')])
# print("========== Tom and Bob\'s  data ==========")
# print(data[(names == 'Bob') & (names == 'Tom')])
# print("========== Tom or Bob\'s data ==========")
# print(data[(names == 'Bob') | (names == 'Tom')])

# # 赋值
# x = np.array([1, -1, -2, 3])
# x[x < 0] += 20  # 所有小于0的x中的元素+20
# print("==========  X ===========")
# print(x)


# # 基本运算
# a = np.array(np.arange(1, 7))
# b = a ** 2
# print(a + b)
# print(a - b)
# print(a * b)
# print(a / b)
# print(a + 2)
# print(a - 2)
# print(a * 2)
# print(a / 2)


# # 广播机制
# a = np.array([[0], [1], [2], [3]])
# b = np.array([1, 2, 3])
# print(a + b)
# print(np.array([1, 2, 3]) == a)
# print(np.array(["tt", "dd", "aa", "dd"]) == "dd")

# # 取整
# a = np.array([1.0, 5.45, 5.55, 123, -0.567, -25.132, 0.5, 1.5, 2.5, 3.5])
# print('原数组：')
# print(a)
# print('舍入后：')
# print(np.around(a))
# print(np.floor(a))
# print(np.ceil(a))
# print(np.around(a, decimals=1))

# # 三角函数
# a = np.array([0, 30, 45, 60, 90], dtype="i8")
# print(a)
# print('含有正弦值的数组：')
# sin = np.sin(a * np.pi / 180)
# print(sin)
# print('计算角度的反正弦，返回值以弧度为单位：')
# inv = np.arcsin(sin)
# print(inv)
# print('通过转化为角度制来检查结果：')
# print(np.degrees(inv))  # 弧度转为角度
# print('arccos 和 arctan 函数行为类似：')
# cos = np.cos(a * np.pi / 180)
# print(cos)
# print('反余弦：')
# inv = np.arccos(cos)
# print(inv)
# print('角度制单位：')
# print(np.degrees(inv))
# print('tan 函数：')
# tan = np.tan(a * np.pi / 180)
# print(tan)
# print('反正切：')
# inv = np.arctan(tan)
# print(inv)
# print('角度制单位：')
# print(np.degrees(inv))

# # 算术函数
# a = np.arange(9, dtype=np.float_).reshape(3, 3)  # np.float_/np.float64
# b = np.array([10, 10, 10])
# print(a)
# print(b)
# print('两个数组相加：')
# print(np.add(a, b))
# print('两个数组相减：')
# print(np.subtract(a, b))
# print('两个数组相乘：')
# print(np.multiply(a, b))
# print('两个数组相除：')
# print(np.divide(a, b))

# # 其他算术
# a = np.array([0.25, 1.33, 1, 100])
# print('调用 reciprocal 函数：')
# print(np.reciprocal(a))
#
# a = np.array([10, 100, 1000])
# b = np.array([3, 2, 1])
# print('调用 power 函数：')
# print(np.power(a, 2))
# print(np.power(a, b))
#
# a = np.array([10, 20, 30])
# b = np.array([3, 5, 7])
# print('调用 mod() 函数：')
# print(np.mod(a, b))
# print('调用 remainder() 函数：')
# print(np.remainder(a, b))

# # 统计
# a = np.array([[3, 7, 5], [8, 4, 3], [2, 4, 9]])
# print(a)
# print('沿轴1，调用 amin() 函数：')
# print(np.amin(a, 1))  # 轴1
# print('沿轴0，调用 amin() 函数：')
# print(np.amin(a, 0))  # 轴0
# print('调用 amin() 函数：')
# print(np.amin(a))
# print('沿轴1，调用 amax() 函数：')
# print(np.amax(a, 1))
# print('沿轴0，调用 amax() 函数：')
# print(np.amax(a, axis=0))
# print('调用 amax() 函数：')
# print(np.amax(a))

# # 极差
# a = np.array([[3, 7, 5], [8, 4, 3], [2, 4, 9]])
# print(a)
# print('调用 ptp() 函数：')
# print(np.ptp(a))
# print('沿轴 1 调用 ptp() 函数：')
# print(np.ptp(a, axis=1))
# print('沿轴 0 调用 ptp() 函数：')
# print(np.ptp(a, axis=0))

# # 平均值
# a = np.array([[1, 2, 3], [3, 4, 5], [4, 5, 6]])
# print('我们的数组是：')
# print(a)
# print('调用 mean() 函数：')
# print(np.mean(a))
# print('沿轴 0 调用 mean() 函数：')
# print(np.mean(a, axis=0))
# print('沿轴 1 调用 mean() 函数：')
# print(np.mean(a, axis=1))
# # 方差
# print(np.var([1, 2, 3, 4]))
# # 标准差
# print(np.std([1, 2, 3, 4]))

# # 中位数
# a = np.array([[30, 65, 70], [80, 95, 10], [50, 90, 60]])
# print(a)
# print('调用 median() 函数：')
# print(np.median(a))
# print('沿轴 0 调用 median() 函数：')
# print(np.median(a, axis=0))
# print('沿轴 1 调用 median() 函数：')
# print(np.median(a, axis=1))

# # 百分位数
# a = np.array([[10, 7, 4], [3, 2, 1]])
# print(a)
# print('调用 percentile(a,50) 函数：')
# # 50% 的分位数，就是 a 里排序之后的中位数
# print(np.percentile(a, 50))
# # axis 为 0，在纵列上求
# print('调用 percentile(a ,50, axis=0) 函数：')
# print(np.percentile(a, 50, axis=0))
# # axis 为 1，在横行上求
# print('调用 percentile(a ,50, axis=1) 函数：')
# print(np.percentile(a, 50, axis=1))
# # 保持维度不变
# print('调用 percentile(a ,50, axis=1, keepdims=True) 函数：')
# print(np.percentile(a, 50, axis=1, keepdims=True))

# # 加权平均
# a = np.array([1, 2, 3, 4])
# print(a)
# print('未指定权重，调用 average() 函数：')
# print(np.average(a))
# # 不指定权重时相当于 mean 函数
# wts = np.array([4, 3, 2, 1])
# print('指定权重数组是：')
# print(wts)
# print('指定权重，调用 average() 函数：')
# print(np.average(a, weights=wts))
# # 如果 returned 参数设为 true，则返回权重的和
# print('加权平均值以及权重的和：')
# print(np.average([1, 2, 3, 4], weights=[4, 3, 2, 1], returned=True))
#
# # 多维数组，指定轴
# print("多维数组，指定轴")
# a = np.arange(6).reshape(3, 2)
# print(a)
# print('指定权重数组是：')
# wt = np.array([3, 5])
# print(wt)
# print('沿轴1，加权平均值：')
# print(np.average(a, axis=1, weights=wt))
# print('沿轴1，加权平均值以及权重的和：')
# print(np.average(a, axis=1, weights=wt, returned=True))

# # 视图 拷贝 引用
# a = np.array([[1], [1], [1], [1]])
# b = a.copy()
# d = a.view()
# e = a
# b += 1
# d += 2
# e += 3
# print(a)
# print(a is b)
# print(d is b)
# print(e is a)

# # 列表转矩阵
# list1 = [[1,2,3,4],[5,6,7,8]]
# mat1 = np.mat(list1)
# mat2 = np.matrix(list1)
# mat3 = np.asmatrix(list1)
# print(mat1)
# print(mat2)
# print(mat3)

# # 数组转矩阵
# list1 = [[1, 2, 3, 4], [5, 6, 7, 8]]
# array1 = np.array(list1)
# mat1 = np.mat(array1)
# mat2 = np.mat(np.ones((3, 3), dtype=np.int8))
# mat3 = np.mat(np.eye(3, 3, dtype=int))
# mat4 = np.mat(np.diag([1, 4, 9]))
# print(mat1)
# print(mat2)
# print(mat3)
# print(mat4)


# # 矩阵运算
# a = np.mat(np.arange(1, 7).reshape(2, 3))
# b = (a + 1).copy()
# bb = a
# bv = a.view()
# bc = a.copy()
# print("a = ", a)
# print("b = ", b)
# print("a + b = ", a + b)  # 矩阵相加，同型矩阵
# print("a - b = ", a - b)  # 矩阵相减，同型矩阵
# c = np.mat(np.arange(1, 7).reshape(3, 2))
# print("c = ", c)
# print("a * c = ", a * c)  # 矩阵相乘，a的列数等于矩阵c的行数
# print("np.dot(a,c) = ", np.dot(a, c))
# print("2 * a = ", 2 * a)  # 数乘矩阵
# print("a * 2 = ", a * 2)
# # 转置
# print("a.T = ", a.T)  # 矩阵转置
# a = a.T
# a[0] = 0
# print(a)
# print(bb)
# print(bv)
# print(bc)
# print("a.I = ", a.I)  # 求逆矩阵
#
# print("矩阵每一列的和 = ", a.sum(axis=0))  # 计算矩阵每一列的和
# print("矩阵每一行的和 = ", a.sum(axis=1))  # 计算矩阵每一行的和
# print("矩阵每一列的最大值 = ", a.max(axis=0))  # 计算矩阵每一列的最大值
# print("矩阵每一行的最大值 = ", a.max(axis=1))  # 计算矩阵每一行的最大值
# print("矩阵每一列的最大值索引 = ", a.argmax(axis=0))  # 计算矩阵每一列的最大值索引
# print("矩阵矩阵每一行的最大值索引 = ", a.argmax(axis=1))  # 计算矩阵每一行的最大值索引

# # 矩阵的分割和合并
# mat1 = np.mat(np.arange(20).reshape(4, 5))
# print("矩阵mat1 = ", mat1)
# # 分割出行2（含）到最后行；列3（含）到最后列，所有元素
# mat2 = mat1[2:, 3:]
# print("矩阵mat1 行2（含）到最后行；列3（含）到最后列的所有元素 = \n", mat2)
# # 分割出开始到行2（不含）；所有列，所有元素
# mat3 = mat1[:2, :]
# print("矩阵mat1 开始到行2（不含）；所有列，所有元素, mat3= \n", mat3)
# # 分割出行2（含）到最后行；所有列，所有元素
# mat4 = mat1[2:, :]
# print("矩阵mat1 行2（含）到最后行；所有列，所有元素 = \n", mat4)
# # 分割出行2（含）到最后行；所有列，所有元素
# mat4 = mat1[2:]
# print("矩阵mat1 行2（含）到最后行；所有列，所有元素, mat4 = \n", mat4)
# mat5 = np.vstack((mat3, mat4))
# print("mat3,mat4按轴0堆叠合并 = ", mat5)
# mat6 = np.hstack((mat3, mat4))
# print("mat3,mat4按轴1堆叠合并 = ", mat6)

# # 排序函数
# # 简单sort
# a = np.array([[9, 7], [3, 1]])
# print(a)
# print('调用 sort() 函数：')
# print(np.sort(a))
# print('按列排序：')
# print(np.sort(a, axis=0))
# print('\n')
#
# # 在 sort 函数中排序字段
# dt = np.dtype([('name', 'S10'), ('age', int)])
# a = np.array([("raju", 21), ("anil", 25), ("ravi", 17), ("amar", 27)], dtype=dt)
# print(a)
# print('按 name 排序：')
# print(np.sort(a, order='name'))

# # argsort()
# x = np.array([3, 1, 2])
# print(x)
# print('对 x 调用 argsort() 函数：')
# y = np.argsort(x)
# print(y)
# print('以排序后的顺序重构原数组：')
# print(x[y])

# # lexsort()
# nm = ('raju', 'anil', 'ravi', 'amar')
# dv = ('f.y.', 's.y.', 's.y.', 'f.y.')
# ind = np.lexsort((dv, nm))
# print('调用 lexsort() 函数：')
# print(ind)
# print('使用这个索引来获取排序后的数据：')
# print([nm[i] + ", " + dv[i] for i in ind])

# # partition() 分区排序
# a = np.array([3, 4, 2, 1, -8, 22, 16, 5, 7, -6, -2])
# b = np.partition(a, 6)
# c = np.partition(a, (0, 6))
# print(a)
# print(b)
# print(c)

# # 索引分区排序
# arr = np.array([46, 57, 23, 39, 1, 10, 0, 120])
# # 索引排序
# ii = np.argpartition(arr, list(range(arr.size)))
# # 找出倒数第二小的 也就是第二大的元素的索引
# jj = np.argpartition(arr, -2)[-2]
# print(ii)
# print(jj)
# print(arr[ii])
# print(arr[jj])


# # argmax() 和 argmin()
# a = np.array([[30, 40, 70], [80, 20, 10], [50, 90, 60]])
# print(a)
# print('调用 argmax() 函数：')
# print(np.argmax(a))
# print('展开数组：')
# print(a.flatten())
# print('沿轴 0 的最大值索引：')
# maxindex = np.argmax(a, axis=0)
# print(maxindex)
# print('沿轴 1 的最大值索引：')
# maxindex = np.argmax(a, axis=1)
# print(maxindex)
# print('调用 argmin() 函数：')
# minindex = np.argmin(a)
# print(minindex)
# print('展开数组中的最小值：')
# print(a.flatten()[minindex])
# print('沿轴 0 的最小值索引：')
# minindex = np.argmin(a, axis=0)
# print(minindex)
# print('沿轴 1 的最小值索引：')
# minindex = np.argmin(a, axis=1)
# print(minindex)

# # 筛选非零值
# a = np.array([[30, 40, 0], [0, 20, 10], [50, 0, 60]])
# print(a)
# print('调用 nonzero() 函数：')
# print(np.nonzero(a))
# print(a[np.nonzero(a)])

# # 更一般的条件筛选
# x = np.arange(9.).reshape(3, 3)
# print(x)
# print('大于 3 的元素的索引：')
# y = np.where(x > 3)
# print(y)
# print('使用这些索引来获取满足条件的元素：')
# print(x[y])

# 条件筛选
# x = np.arange(9.).reshape(3, 3)
# print('我们的数组是：')
# print(x)
# # 定义条件, 选择偶数元素
# condition = np.mod(x, 2) == 0
# print('按元素的条件值：')
# print(condition)
# print('使用条件提取元素：')
# print(np.extract(condition, x))
# print(x[condition])


# a = np.array([[1, 2], [3, 4]])
# b = np.array([[11, 12], [13, 14]])
# print(np.dot(a, b))
# print(np.vdot(a, b))

# # 一维
# print(np.inner(np.array([1, 2, 3]), np.array([0, 1, 0])))
# # 高维
# x = np.arange(4).reshape(2, 2)
# y = (np.arange(4) + 1).reshape(2, 2)
# print(np.inner(x, y))
# print(np.inner(x[0], y[0]))
# print(np.inner(x[0], y[1]))
# print(np.inner(x[1], y[0]))
# print(np.inner(x[1], y[1]))


# # 一般矩阵乘
# a = [[1, 0], [0, 1]]
# b = [[4, 1], [2, 2]]
# print(np.matmul(a, b))
# # 一维与二维 (补全后计算，算完再删去)
# a = [[1, 0], [0, 1]]
# b = [1, 2]
# print(np.matmul(a, b))
# print(np.matmul(b, a))
# # 多维
# a = np.arange(8).reshape(2, 2, 2)
# b = np.arange(4).reshape(2, 2)
# print(np.matmul(a, b))


# b = np.array([[6,1,1], [4, -2, 5], [2,8,7]])
# print (b)
# print (np.linalg.det(b))
# print (6*(-2*7 - 5*8) - 1*(4*7 - 5*2) + 1*(4*8 - -2*2))


# # 矩阵的秩
# A_1 = np.array([[1, 1, 0],
#                 [1, 0, 1]])
#
# A_2 = np.array([[1, 2, -1],
#                 [2, 4, -2]])
#
# A_3 = np.array([[1, 0],
#                 [0, 1],
#                 [0, -1]])
#
# A_4 = np.array([[1, 2],
#                 [1, 2],
#                 [-1, -2]])
#
# A_5 = np.array([[1, 1, 1],
#                 [1, 1, 2],
#                 [1, 2, 3]])
#
# print(np.linalg.matrix_rank(A_1))
# print(np.linalg.matrix_rank(A_2))
# print(np.linalg.matrix_rank(A_3))
# print(np.linalg.matrix_rank(A_4))
# print(np.linalg.matrix_rank(A_5))

# # 求矩阵的逆
# A = np.array([[1, 35, 0],
#               [0, 2, 3],
#               [0, 0, 4]])
# ainv = np.linalg.inv(A)
# print('A 的逆ainv：', ainv)
#
# print(np.dot(A, ainv))


# # 求解线性方程组
# A = np.array([[1, 2, 3],
#               [1, -1, 4],
#               [2, 3, -1]])
# y = np.array([14, 11, 5])
# x = np.linalg.solve(A, y)
# print("线性方程组的解为: x=", x)
# print(np.matmul(np.linalg.inv(A), y))

# # 求矩阵的特征值和特征向量(eigenvalue,eigenvector)
# A = np.array([[2, 1],
#               [1, 2]])
# evalue, evector = np.linalg.eig(A)
# print("特征值：", evalue)
# print("特征向量：", evector)
#
# A = np.array([[1, 0, 0],
#               [0, 2, 0],
#               [0, 0, 5]])
# evalue, evector = np.linalg.eig(A)
# print("特征值：", evalue)
# print("特征向量：", evector)
#
# A = np.array([[6, -2, 1],
#               [0, 4, 0],
#               [0, 0, 7]])
#
# evalue, evector = np.linalg.eig(A)
# print("特征值：", evalue)
# print("特征向量：", evector)