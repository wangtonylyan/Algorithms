# -*- coding: utf-8 -*-
# problem: 01-package
# solution: dynamic programming


bag = 10  # total weight
its = [(2, 6), (2, 6), (4, 3), (5, 4), (6, 5)]  # item pair(weight,value)
tab = [[0 for col in range(len(its))] for row in range(bag)]


def pkg():
    # 该双重循环中，无论i和j谁先后，只需保证tab[i][j]在其所依赖的项之后被遍历到即可
    # tab[i][j] ~ tab[i-items[j][0]][j-1] or tab[i][j-1]
    for i in range(bag):  # weight of bag
        for j in range(len(its)):  # number of items
            if j == 0:
                if its[j][0] <= i:
                    tab[i][j] = its[j][1]
                else:
                    tab[i][j] = 0
            else:
                v1 = 0
                if its[j][0] <= i:
                    v1 = tab[i - its[j][0]][j - 1] + its[j][1]
                v2 = tab[i][j - 1]
                tab[i][j] = v1 if v1 > v2 else v2


if __name__ == '__main__':
    pkg()
    for i in range(bag):
        for j in range(len(its)):
            print tab[i][j], '\t',
        print
