# -*- coding: utf-8 -*-
# problem: knapsack problem (rucksack problem)
# solution: dynamic programming
# @param weight: weight of knapsack
# @param items: pairs of item info (weight,value)

class Knapsack(object):
    def __init__(self):
        self.funcs = []

    def testcase(self):
        def test(case):
            assert (len(self.funcs) > 1)
            assert (reduce(lambda x, y: x if x == y(case[0], case[1]) else -1,
                           self.funcs[1:], self.funcs[0](case[0], case[1])) > 0)

        cases = [(10, [(2, 6), (2, 6), (4, 3), (5, 4), (6, 5)]),
                 (50, [(10, 60), (20, 100), (30, 120)]),
                 ]
        map(test, cases)
        print 'pass:', self.__class__


class Knapsack01(Knapsack):
    def __init__(self):
        super(Knapsack01, self).__init__()
        self.funcs.append(self.main_1)
        self.funcs.append(self.main_2)

    # recursive version of main_2()
    def main_1(self, weight, items):
        def _recur(wgt, ind):
            if wgt == 0 or ind < 0:
                return 0
            return max(_recur(wgt - items[ind][0], ind - 1) + items[ind][1] if items[ind][0] <= wgt else 0,
                       _recur(wgt, ind - 1))

        return _recur(weight, len(items) - 1)

    def main_2(self, weight, items):
        # tab[i][j]: the maximum value within an i-weight knapsack with j items
        # tab[i][j] ~ tab[i-items[j-1][0]][j-1] or tab[i][j-1]
        # ......................
        # ... (i-k,j-1) ........
        # ...    .      ........
        # ...    .      ........
        # ... (i,j-1)   (i,j) ..
        # ......................
        tab = [[0 for col in range(len(items) + 1)] for row in range(weight + 1)]  # 范围加1可以避免边界情况的讨论(使用默认值)
        for i in range(1, weight + 1):  # weight of knapsack
            for j in range(1, len(items) + 1):  # number of items
                tab[i][j] = max(tab[i - items[j - 1][0]][j - 1] + items[j - 1][1] if items[j - 1][0] <= i else 0,
                                tab[i][j - 1])
        return tab[-1][-1]


class KnapsackComplete(Knapsack):
    def __init__(self):
        super(KnapsackComplete, self).__init__()
        self.funcs.append(self.main_1)
        self.funcs.append(self.main_2)

    def main_1(self, weight, items):
        def _recur(wgt, ind):
            if wgt == 0 or ind < 0:
                return 0
            return max(_recur(wgt - items[ind][0], ind) + items[ind][1] if items[ind][0] <= wgt else 0,
                       _recur(wgt, ind - 1))

        return _recur(weight, len(items) - 1)

    def main_2(self, weight, items):
        # tab[i][j] ~ tab[i-items[j-1][0]][j] or tab[i][j-1]
        # ......................
        # .......... (i-k,j) ...
        # ..........    .    ...
        # ..........    .    ...
        # .. (i,j-1)  (i,j)  ...
        # ......................
        tab = [[0 for col in range(len(items) + 1)] for row in range(weight + 1)]
        for i in range(1, weight + 1):
            for j in range(1, len(items) + 1):
                tab[i][j] = max(tab[i - items[j - 1][0]][j] + items[j - 1][1] if items[j - 1][0] <= i else 0,
                                tab[i][j - 1])
        return tab[-1][-1]


if __name__ == '__main__':
    Knapsack01().testcase()
    KnapsackComplete().testcase()
    print 'done'
