import re

if __name__ == '__main__':
    for i in range(5):
        pwd = input("输入口令:")
        pat = re.compile("((^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$)|(^(?=.*\d)(?=.*[a-z])(?=.*[,?!;@.<>]).{8,}$)|(^(?=.*\d)(?=.*[A-Z])(?=.*[,?!;@.<>]).{8,}$)|(^(?=.*[a-z])(?=.*[A-Z])(?=.*[,?!;@.<>]).{8,}$))")
        print("弱口令" if pat.search(pwd) is None else "强口令")
