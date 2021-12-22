# 读取文本文件内容并统计其中每个英文字母的出现次数，
# 如果文件不存在则给出友好提示，使用异常处理结构实现。
import string

if __name__ == '__main__':
    dic = {c: 0 for c in string.ascii_letters}
    try:
        f = open(input("Enter a filename\n"))
        for line in f:
            for c in line:
                if c in dic:
                    dic[c] += 1
        for c, ct in dic.items():
            print(f"{c}:{ct}")
    except FileNotFoundError:
        print("file does not exist")
