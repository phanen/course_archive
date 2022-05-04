if __name__ == '__main__':
    myBreak = False
    for i in range(5):
        for j in range(5):
            for k in range(5):
                if i == j == k == 3:
                    print("\nit’s over")
                    myBreak = True
                    break
                print((i, j, k), end=" ")
            if myBreak:
                break
        if myBreak:
            break
