# -*- coding: utf-8 -*-
# problem: longest (strictly) increasing subsequence
# 非严格递增子序列的算法实现只需改变部分不等号
# 并不易于算法的理解，暂没有实现

import random


class LIS():
    def main_1(self, lst):
        # lis记录了以lst中每个字符为结尾的最大递增序列的长度
        lis = [1 for i in range(len(lst))]
        for i in range(1, len(lst)):
            for j in range(0, i):
                if lst[i] > lst[j] and lis[i] < lis[j] + 1:
                    lis[i] = lis[j] + 1
        return max(lis)

    def main_2(self, lst):
        # tab[i][j]: the minimum end number of all i-length subsequences in a j-length sequence
        # tab[i][j] ~ tab[i-1][j] or tab[i-1][j-1] or tab[i][j-1]
        # tab[i][j] = lst[j] or tab[i][j-1] or None
        tab = [[None for col in range(len(lst))] for row in range(len(lst))]
        for i in range(len(lst)):  # i: length of increasing subsequence
            for j in range(len(lst)):  # j: length of sequence
                if i > j:
                    continue
                elif i == 0:
                    if j == 0 or lst[j] < tab[i][j - 1]:
                        tab[i][j] = lst[j]
                    else:
                        tab[i][j] = tab[i][j - 1]
                else:
                    # 存在的可能性逐个降低：tab[i-1][j], tab[i-1][j-1], tab[i][j-1]
                    # 子问题也是最优解：tab[i-1][j] <= tab[i-1][j-1] < tab[i][j-1]
                    if tab[i - 1][j] == None or tab[i - 1][j - 1] == None:
                        assert (tab[i][j - 1] == None)
                        assert (tab[i - 1][j] == None or tab[i - 1][j] == lst[j])
                        continue
                    elif tab[i][j - 1] == None:
                        assert (tab[i - 1][j] <= tab[i - 1][j - 1])
                        assert (tab[i - 1][j] == lst[j] or tab[i - 1][j] == tab[i - 1][j - 1])
                        # 是否有解？
                        if lst[j] > tab[i - 1][j - 1]:
                            tab[i][j] = lst[j]
                    else:
                        assert (tab[i - 1][j] <= tab[i - 1][j - 1] < tab[i][j - 1])
                        # 是否是最优解？
                        if lst[j] > tab[i][j - 1] or lst[j] < tab[i - 1][j - 1]:
                            tab[i][j] = tab[i][j - 1]
                        else:
                            tab[i][j] = lst[j]

        for i in range(len(lst) - 1, -1, -1):
            if tab[i][len(lst) - 1] != None:
                return i + 1
        assert (False)

    def testcase(self):
        def test(lst):
            assert (self.main_1(lst) == self.main_2(lst))

        llst = []
        for i in range(10):
            lst = [i for i in range(random.randint(10, 100))]
            for j in range(len(lst)):
                random.shuffle(lst)
                llst.append(lst)
        map(test, llst)


if __name__ == '__main__':
    LIS().testcase()
    print 'done'
