import pandas as pd
import os

root = './宿舍情况汇总'
lst = os.listdir(root)
print(lst)

# df = pd.read_excel("./宿舍情况汇总/20211008宿舍检查/网安s11-s13(1).xls")
t = 0
for dirname in lst:
    dirname = root + '/' + dirname
    sub_lst = os.listdir(dirname)
    for nm in sub_lst:
        if ("s11" in nm) and (".xls" in nm):
            path = dirname + '/' + nm
            print(path)
            df = pd.read_excel(path)  # sheet_name不指定时默认返回全表数据
            id = df.columns[-1]
            diff = df[id][2] - 100
            t += diff
            print(diff)
print(f"total: {cur}")