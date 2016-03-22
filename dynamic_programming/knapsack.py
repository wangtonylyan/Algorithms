# -*- coding: utf-8 -*-
# problem: knapsack problem (rucksack problem)
# solution: dynamic programming


class Knapsack01():
    # bag: total weight
    # items: item pair (weight,value)
    def main(self, bag, items):
        # tab[i][j]: the maximum value in an i-weight bag with j+1 items
        # tab[i][j] ~ tab[i-items[j][0]][j-1] or tab[i][j-1]
        tab = [[0 for row in range(len(items))] for i in range(bag + 1)]
        for i in range(1, bag + 1):  # weight of bag
            for j in range(len(items)):  # number of items
                if j == 0:
                    tab[i][j] = items[j][1] if items[j][0] <= i else 0
                else:
                    tab[i][j] = max(items[j][1] + tab[i - items[j][0]][j - 1] if items[j][0] <= i else 0,
                                    tab[i][j - 1])
        return tab

    def testcase(self):
        def test(func):
            assert (func(10, [(2, 6), (2, 6), (4, 3), (5, 4), (6, 5)])[-1][-1] == 17)
            assert (func(50, [(10, 60), (20, 100), (30, 120)])[-1][-1] == 220)

        map(test, [self.main])


if __name__ == '__main__':
    Knapsack01().testcase()
