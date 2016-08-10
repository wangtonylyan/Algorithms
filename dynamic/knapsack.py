# -*- coding: utf-8 -*-
# problem: knapsack problem (rucksack problem)
# solution: dynamic programming
# @param weight: weight of knapsack
# @param items: pairs of item info (weight,value,number)

import copy


class Knapsack(object):
    def __init__(self):
        self.funcs = []

    def testcase(self):
        def test(case):
            assert (len(self.funcs) > 0)
            for wgt in range(1, case[0] * 10):
                ret = self.funcs[0](wgt, copy.deepcopy(case[1]))
                assert (all(f(wgt, copy.deepcopy(case[1])) == ret >= 0 for f in self.funcs[1:]))

        cases = [(10, [(2, 6, 3), (2, 7, 1), (4, 3, 2), (5, 4, 2), (6, 5, 2)]),
                 (50, [(10, 60, 2), (20, 100, 2), (30, 120, 5)]),
                 ]
        map(test, cases)
        print 'pass:', self.__class__


class ZeroOneKnapsack(Knapsack):
    def __init__(self):
        super(ZeroOneKnapsack, self).__init__()
        self.funcs.append(self.main_1)
        self.funcs.append(self.main_2)
        self.funcs.append(self.main_3)

    # depth-first search, also recursive version of main_2()
    def main_1(self, weight, items):
        def recur(wgt, ind):
            if wgt <= 0 or ind < 0:
                return 0
            return max(recur(wgt - items[ind][0], ind - 1) + items[ind][1] if items[ind][0] <= wgt else 0,
                       recur(wgt, ind - 1))

        return recur(weight, len(items) - 1)

    def main_2(self, weight, items):
        # tab[i][j]: the maximum value within an i-weight knapsack with j items
        # tab[i][j] ~ tab[i-items[j-1][0]][j-1] or tab[i][j-1]
        # ......................
        # ... (i-k,j-1) ........
        # ...    .      ........
        # ...    .      ........
        # ... (i,j-1)   (i,j) ..
        # ......................
        tab = [[0] * (len(items) + 1) for _ in range(weight + 1)]  # 范围加1可以避免边界情况的讨论
        for i in range(1, weight + 1):  # weight of knapsack
            for j in range(1, len(items) + 1):  # number of items
                tab[i][j] = max(tab[i - items[j - 1][0]][j - 1] + items[j - 1][1] if items[j - 1][0] <= i else 0,
                                tab[i][j - 1])
        return tab[-1][-1]

    # space optimization for main_2()
    def main_3(self, weight, items):
        tab = [0] * (weight + 1)
        for i in range(len(items)):
            for j in range(weight, items[i][0] - 1, -1):
                tab[j] = max(tab[j - items[i][0]] + items[i][1], tab[j])
        return tab[-1]


class CompleteKnapsack(Knapsack):
    def __init__(self):
        super(CompleteKnapsack, self).__init__()
        self.funcs.append(self.main_1)
        self.funcs.append(self.main_2)
        self.funcs.append(self.main_3)
        self.funcs.append(self.main_4)

    # convert to 01-knapsack problem
    # 优化：从数的二进制表示，对物品数量的构成进行优化
    def main_1(self, weight, items):
        for it in items[:]:
            dup = []
            w, v = it[0], it[1]
            k = 1  # exponential of 2
            # while (w << (k + 1)) - w <= weight:
            while w << (k + 1) <= weight:
                dup.append((w << k, v << k))
                k += 1
            # 该if条件可以同时弥补/覆盖上述两个while条件所造成的"空隙"
            if (w << k) - w <= weight - w:
                k = (weight - (w << k) + w) / w
                assert (isinstance(k, int) and k > 0)
                dup.append((w * k, v * k))
            # @assert: items中同种物品的重量总和不大于weight
            assert (w > weight or weight - sum([x[0] for x in dup + [(w, v)]]) <= w)
            items += dup
        return ZeroOneKnapsack().main_3(weight, items)

        for it in items[:]:
            dup = []
            w, v = it[0], it[1]
            k = 2  # power of 2
            while w * k <= weight:
                dup.append((w * k, v * k))
                k *= 2
            dup.append((w * k, v * k))
            # @assert: items中同种物品的重量总和不小于weight
            assert (sum([x[0] for x in dup + [(w, v)]]) >= weight)
            items += dup
        return ZeroOneKnapsack().main_3(weight, items)

    def main_2(self, weight, items):
        def recur(wgt, ind):
            if wgt <= 0 or ind < 0:
                return 0
            return max(recur(wgt - items[ind][0], ind) + items[ind][1] if items[ind][0] <= wgt else 0,
                       recur(wgt, ind - 1))

        return recur(weight, len(items) - 1)

    def main_3(self, weight, items):
        # tab[i][j] ~ tab[i-items[j-1][0]][j] or tab[i][j-1]
        # ......................
        # .......... (i-k,j) ...
        # ..........    .    ...
        # ..........    .    ...
        # .. (i,j-1)  (i,j)  ...
        # ......................
        tab = [[0] * (len(items) + 1) for _ in range(weight + 1)]
        for i in range(1, weight + 1):
            for j in range(1, len(items) + 1):
                tab[i][j] = max(tab[i - items[j - 1][0]][j] + items[j - 1][1] if items[j - 1][0] <= i else 0,
                                tab[i][j - 1])
        return tab[-1][-1]

    def main_4(self, weight, items):
        tab = [0] * (weight + 1)
        for i in range(len(items)):
            for j in range(1, weight + 1):
                tab[j] = max(tab[j - items[i][0]] + items[i][1] if items[i][0] <= j else 0,
                             tab[j])
        return tab[-1]


class MultipleKnapsack(Knapsack):
    def __init__(self):
        super(MultipleKnapsack, self).__init__()
        self.funcs.append(self.main_1)
        self.funcs.append(self.main_2)

    def main_1(self, weight, items):
        def recur(wgt, ind):
            if wgt <= 0 or ind < 0:
                return 0
            return max([recur(wgt - items[ind][0] * num, ind - 1) + items[ind][1] * num
                        if items[ind][0] * num <= wgt else 0 for num in range(items[ind][2] + 1)])

        return recur(weight, len(items) - 1)

    def main_2(self, weight, items):
        cpy = items[:]
        for it in items:
            k = 2
            while k * 2 <= it[2] and it[0] * k <= weight:
                cpy.append((it[0] * k, it[1] * k))
                k *= 2
            if k <= it[2]:
                k = it[2] - k + 1
                if it[0] * k <= weight:
                    cpy.append((it[0] * k, it[1] * k))
        return ZeroOneKnapsack().main_3(weight, cpy)


if __name__ == '__main__':
    ZeroOneKnapsack().testcase()
    CompleteKnapsack().testcase()
    MultipleKnapsack().testcase()
    print 'done'
