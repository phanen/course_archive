actor = {}

l1 = [
    "刘昊然",
    "宋祖儿",
    "陈若轩",
    "张志坚",
    "李光洁",
    "许晴",
    "江疏影",
    "王鸥",
    "张丰毅",
    "张嘉泽"
]
l2 = [
    "吕归尘",
    "羽然",
    "姬野",
    "雷碧城",
    "息衍",
    "白凌波",
    "宫羽衣",
    "苏瞬卿",
    "嬴无翳",
    "百里景洪"
]
for i, s in enumerate(l1):
    actor[s] = {}
    actor[s]["character"] = l2[i]

actor["陈若轩"]["dub"] = "许凯"
actor["江疏影"]["dub"] = "韩啸"
actor["张丰毅"]["dub"] = "宣晓鸣"

print(actor["刘昊然"]["character"])
save = actor
actor["张静初"] = actor["江疏影"]
del actor["江疏影"]

actor["宣言"] = "白鹿颜"
actor["魏千翔"] = "百里宁卿"
actor["刘冠成"] = "拓跋山月"
actor["江涛"] = "翼天展"
actor["董勇"] = "吕嵩"
actor["杨新鸣"] = "大合萨"
actor["张智尧"] = "白毅"
actor["陈昊宇"] = "小舟公主"
actor["杨玏"] = "吕鹰扬"
actor["吴佳怡"] = "嬴玉"

print(save)
print("角色数目: ", len(save))
