# -*- coding: utf-8 -*-
# problem: longest (strictly) increasing subsequence and longest common subsequence
# LIS: 非严格递增子序列的算法实现只需改变部分不等号，并不易于算法的理解，暂没有实现

import random


class LongestIncreasingSubsequence():
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
        # tab[i][j] ~ tab[i-1][j-1] or tab[i][j-1]
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
                    if tab[i - 1][j - 1] == None:  # 无解
                        assert (tab[i][j - 1] == None)
                        continue
                    elif tab[i][j - 1] == None:  # 是否有解？
                        if lst[j] > tab[i - 1][j - 1]:
                            tab[i][j] = lst[j]
                    else:  # 是否是最优解？
                        assert (tab[i - 1][j - 1] < tab[i][j - 1])  # 子问题也是最优解
                        if tab[i - 1][j - 1] < lst[j] < tab[i][j - 1]:
                            tab[i][j] = lst[j]
                        else:
                            tab[i][j] = tab[i][j - 1]

        for i in range(len(lst) - 1, -1, -1):
            if tab[i][-1] != None:
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
        print 'pass:', self.__class__


class LongestCommonSubsequence():
    # brute force algorithm, also the recursive version of main_2()
    def main_1(self, lst1, lst2):
        def recur(i, j):
            if i == 0 or j == 0:
                return 0
            if lst1[i - 1] == lst2[j - 1]:  # two sequences start from index i-1 and j-1
                return recur(i - 1, j - 1) + 1
            else:
                return max(recur(i - 1, j), recur(i, j - 1))

        return recur(len(lst1), len(lst2))

    def main_2(self, lst1, lst2):
        # tab[i][j]: the longest length of all common subsequences of lst1[:i] and lst2[:j]
        # tab[i][j] ~ tab[i-1][j-1] or tab[i-1][j] or tab[i][j-1]
        # tab[i][j] = max(tab[i-1][j-1]+1, tab[i-1][j], tab[i][j-1])
        tab = [[0 for row in range(len(lst2) + 1)] for col in range(len(lst1) + 1)]
        for i in range(len(lst1) + 1):  # index of lst1
            for j in range(len(lst2) + 1):  # index of lst2
                if i == 0 or j == 0:
                    tab[i][j] = 0
                elif tab[i - 1][j - 1] < tab[i - 1][j] or tab[i - 1][j - 1] < tab[i][j - 1]:
                    # either lst1[i] or lst2[j] has become a part of the commen subsequence
                    assert (tab[i - 1][j - 1] + 1 == tab[i - 1][j] or tab[i - 1][j - 1] + 1 == tab[i][j - 1])
                    tab[i][j] = max(tab[i - 1][j], tab[i][j - 1])
                else:
                    assert (tab[i - 1][j - 1] == tab[i - 1][j] == tab[i][j - 1])
                    tab[i][j] = tab[i - 1][j - 1] + (1 if lst1[i - 1] == lst2[j - 1] else 0)
                continue  # equivalent to
                if i == 0 or j == 0:
                    tab[i][j] = 0
                elif lst1[i - 1] == lst2[j - 1]:
                    tab[i][j] = tab[i - 1][j - 1] + 1
                else:
                    tab[i][j] = max(tab[i - 1][j], tab[i][j - 1])
        return tab[-1][-1]

    def testcase(self):
        def test((lst1, lst2)):
            assert (self.main_1(lst1, lst2) == self.main_2(lst1, lst2))

        llst = []
        for i in range(15):
            lst1 = [i for i in range(random.randint(5, 15))]
            random.shuffle(lst1)
            lst2 = [i for i in range(random.randint(5, 15))]
            random.shuffle(lst2)
            llst.append((lst1, lst2))
        map(test, llst)
        print 'pass:', self.__class__


if __name__ == '__main__':
    LongestIncreasingSubsequence().testcase()
    LongestCommonSubsequence().testcase()
    print 'done'
