def hannoi(num, src, dst, temp=None):
    if num == 0:
        return
    hannoi(num - 1, src, temp, dst)
    print(src["name"], "->", dst["name"], end="\t")
    dst["drb"].append(src["drb"].pop())
    print((src["drb"], temp["drb"], dst["drb"]))
    hannoi(num - 1, temp, dst, src)


if __name__ == '__main__':
    num = 6
    hannoi(num, {"name": "A", "drb": list(reversed(range(num)))}, {"name": "C", "drb": []}, {"name": "B", "drb": []})
