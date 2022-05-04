import numpy as np


def cosSim(inA, inB):
    """余弦相似度"""
    return 0.5 + 0.5 * (float(np.dot(inA.T, inB)) / (np.linalg.norm(inA) * np.linalg.norm(inB)))


def estScore(scoreData, scoreDataRC, userIndex, itemIndex):
    n = np.shape(scoreData)[1]
    simSum = 0
    simSumScore = 0
    for i in range(n):
        userScore = scoreData[userIndex, i]
        if userScore == 0 or i == itemIndex:
            continue
        sim = cosSim(scoreDataRC[:, i], scoreDataRC[:, itemIndex])
        simSum = float(simSum + sim)
        simSumScore = simSumScore + userScore * sim
        if simSum == 0:
            return 0
    return simSumScore / simSum


# 获取原始的用户 - 菜品打分矩阵 scoreData
scoreData = np.loadtxt('score.csv', delimiter=',')

# 奇异值分解
U, sigma, VT = np.linalg.svd(scoreData)
# 对矩阵进行行压缩
sigma_K = np.mat(np.eye(6) * sigma[:6])
# 获取降维后规模为 6×11 行压缩矩阵
scoreDataRC = sigma_K * U.T[:6, :] * scoreData

# 人数 和 菜品数
m, n = np.shape(scoreData)
dt = np.dtype([('index', int), ('score', float)])
for userIndex in range(m):
    print(f"对用户{userIndex}的推荐：")
    rcmdTable = []
    for itemIndex in range(n):
        userScore = scoreData[userIndex, itemIndex]
        # 是否打过分
        if userScore != 0:
            continue
        rcmdTable.append((itemIndex, estScore(scoreData, scoreDataRC, userIndex, itemIndex)))
    rcmdTable = np.array(rcmdTable, dtype=dt)
    # 分值由高到低 推荐三个
    for idx, sc in np.sort(rcmdTable, order='score')[-1:-4:-1]:
        print(f"----{idx}号菜，{sc}分")
