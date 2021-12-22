idList = ["440524188001015368",
          "11010519491231002X",
          "53010219200508011X"]

x, y, z = var('x y z')
weigh = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, x, y, z]
f = "10X98765432"
eqs = [0, 0, 0]

for i, string in enumerate(idList):
    for a, w in zip(string, weigh):
        eqs[i] += int(a) * w
    eqs[i] -= f.find(string[17])

print(eqs)
solve(eqs, x, y, z)

A = matrix(Zmod(11), 3, 3, [5, 3, 6, 0, 0, 2, 0, 1, 1])
B = matrix(Zmod(11), 3, 1, [-189, -161, -181])
A.solve_right(B)
