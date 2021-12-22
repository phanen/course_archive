# coding=utf-8
"""
简易推荐系统:
    1.基于物品相似度,向同一用户推荐不同的相似商品(user:items=1:N);
    2.基于用户相似度,将同一商品推荐给不同的未购买用户(users:item=N:1);
"""
import numpy as np
from numpy import *
from numpy import linalg as la


def loadExData():
    '''加载测试数据集'''
    return mat([[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
                [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
                [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
                [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
                [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
                [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
                [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
                [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
                [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
                [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
                [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]])


def ecludSim(inA, inB):
    """欧氏距离相似度  1/(1+距离)"""
    return 1.0 / (1.0 + la.norm(inA - inB))  # 范数的计算方法linalg.norm()，这里的表示将相似度的范围放在0与1之间


def pearsSim(inA, inB):
    """皮尔逊相关系数 0.5+0.5*corrcoef() 对列求相似度  """
    if len(inA) < 3:
        return 1.0
    return 0.5 + 0.5 * corrcoef(inA, inB, rowvar=False)[0][1]


def cosSim(inA, inB):
    return 0.5 + 0.5 * (float(inA.T * inB) / la.norm(inA) * la.norm(inB))


'''按照前k个奇异值的平方和占总奇异值的平方和的百分比percentage来确定k的值,
后续计算SVD时需要将原始矩阵转换到k维空间'''


def sigmaPct(sigma, percentage):
    sigma2 = sigma ** 2  # 对sigma求平方
    sumsgm2 = sum(sigma2)  # 求所有奇异值sigma的平方和
    sumsgm3 = 0  # sumsgm3是前k个奇异值的平方和
    k = 0
    for i in sigma:
        sumsgm3 += i ** 2
        k += 1
        if sumsgm3 >= sumsgm2 * percentage:
            return k


'''函数svdEst()的参数包含：数据矩阵、用户编号、物品编号和奇异值占比的阈值，
数据矩阵的行对应用户，列对应物品，函数的作用是基于item的相似性对用户未评过分的物品进行预测评分'''
xformedItems000 = []  # 存储中间过程,以备验证和查看
sssssss000 = []


def svdEst(dataMat, user, simMeas, item, percentage):
    n = np.shape(dataMat)[1]
    simTotal = 0.0;
    ratSimTotal = 0.0
    u, sigma, vt = la.svd(dataMat)  # dataMat,对商品列做降维
    sssssss000.append([u, sigma, vt])
    k = sigmaPct(sigma, percentage)  # 确定了k的值
    sigmaK = np.mat(np.eye(k) * sigma[:k])  # 构建对角矩阵
    xformedItems = dataMat.T * u[:, :k] * sigmaK.I  # 根据k的值将原始数据转换到k维空间(低维),xformedItems表示物品(item)在k维空间转换后的值
    xformedItems000.append(xformedItems)
    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0 or j == item:
            continue
        similarity = simMeas(xformedItems[item, :].T, xformedItems[j, :].T)  # 计算物品item与物品j之间的相似度
        simTotal += similarity  # 对所有相似度求和
        ratSimTotal += similarity * userRating  # 用"物品item和物品j的相似度"乘以"用户对物品j的评分"，并求和
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal  # 得到对物品item的预测评分


xformedItems1111 = []
sssssss111 = []


def svdEst1(dataMat, item, simMeas, user, percentage):
    n = np.shape(dataMat)[0]
    simTotal = 0.0;
    ratSimTotal = 0.0
    u, sigma, vt = la.svd(dataMat.T)  # dataMat.T,对用户列做降维
    sssssss111.append([u, sigma, vt])
    k = sigmaPct(sigma, percentage)  # 确定了k的值
    sigmaK = np.mat(np.eye(k) * sigma[:k])  # 构建对角矩阵
    xformedItems = dataMat.T * u[:, :k] * sigmaK.I  # 根据k的值将原始数据转换到k维空间(低维),xformedItems表示物品(item)在k维空间转换后的值
    # np.shape(xformedItems1111[0])    #(3, 11)
    xformedItems1111.append(xformedItems)
    for j in range(n):
        itemRating = dataMat.T[item, j]
        if itemRating == 0 or j == user:
            continue
        similarity = simMeas(xformedItems[user, :].T, xformedItems[j, :].T)  # 计算物品item与物品j之间的相似度
        simTotal += similarity  # 对所有相似度求和
        ratSimTotal += similarity * itemRating  # 用"物品item和物品j的相似度"乘以"用户对物品j的评分"，并求和
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal  # 得到对物品item的预测评分


'''函数recommend()产生预测评分最高的N个推荐结果，默认返回5个；
参数包括：数据矩阵、用户编号、相似度衡量的方法、预测评分的方法、以及奇异值占比的阈值；
数据矩阵的行对应用户，列对应物品，函数的作用是基于item的相似性对用户未评过分的物品进行预测评分；
相似度衡量的方法默认用余弦相似度'''


# 给同一用户,推荐不同的商品
def recommendSameUserBydiffItems(dataMat, user, cosSim, svdEst, N=5, percentage=0.9):
    unratedItems = np.nonzero(dataMat[user, :].A == 0)[1]  # 建立一个用户未评分item的列表,内部元素是有多少件未评分的物品。dataMat,行是user,列是item.
    if len(unratedItems) == 0:
        return []  # 如果都已经评过分，则退出
    itemScores = []
    for item in unratedItems:  # 对于每个未评分的item，都计算其预测评分
        estimatedScore = svdEst(dataMat, user, cosSim, item, percentage)
        itemScores.append((item, estimatedScore))
    itemScores = sorted(itemScores, key=lambda x: x[1], reverse=True)  # 按照item的得分进行从大到小排序
    return itemScores[:N]  # 返回前N大评分值的item名，及其预测评分值


dataMat = loadExData()
SameUserBydiffItems = list()
user = [i for i in range(11)]
for user1 in user:  ##给某用户推荐给top k=5个最相似的未购买的商品。
    print(user1)
    rec_score = recommendSameUserBydiffItems(dataMat, user1, cosSim, svdEst, N=5, percentage=0.9)
    SameUserBydiffItems.append(rec_score)
    del rec_score


# 将同一物品,推荐给不同的用户
def recommendSameItemBydiffUsers(dataMat, item, cosSim, svdEst1, N=5, percentage=0.9):
    # 找出最相似的top k=5个未购买item的用户,将同一商品推荐给他们
    unbuyedUsers = np.nonzero(dataMat.T[item, :].A == 0)[
        1]  # 建立一个对item这个商品未购买的用户的用户列表,内部元素是有未购买item的用户编号。dataMat.T,行是item,列是user.
    if len(unbuyedUsers) == 0:
        return []  # 如果都已经购买过该商品，则退出
    userScores = []
    for user1 in unbuyedUsers:  # 对于未购买item的每个用户计算其购买的可能性(可能打分)
        estimatedScore = svdEst1(dataMat, item, cosSim, user1, percentage)
        userScores.append((user1, estimatedScore))
    userScores = sorted(userScores, key=lambda x: x[1], reverse=True)  # 按照item的得分进行从大到小排序
    return userScores[:N]  # 返回前N个相似的user名,以及预测相似度


SameItemBydiffUsers = list()
item = [i for i in range(11)]
for item1 in item:  # 将某件商品推荐给top k=5个最相似的未购买的用户。
    print(item1)
    rec_score = recommendSameItemBydiffUsers(dataMat, item1, cosSim, svdEst1, N=5, percentage=0.9)
    SameItemBydiffUsers.append(rec_score)
    del rec_score
