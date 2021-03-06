# -*- coding: utf-8 -*-

import random


# @problem: longest (strictly) increasing subsequence
# 非严格递增子序列的算法实现只需改变部分不等号，并不易于算法的理解，暂没有实现
class LongestIncreasingSubsequence():
    def main_1(self, lst):
        # tab记录了以lst中每个字符为结尾的最大递增序列的长度
        tab = [1] * len(lst)
        for i in range(1, len(lst)):
            for j in range(i):
                if lst[j] < lst[i] and tab[j] + 1 > tab[i]:
                    tab[i] = tab[j] + 1
        return max(tab)

    def main_2(self, lst):
        # tab[i][j]: the minimum end number of all i-length subsequences in a j-length sequence
        # tab[i][j] ~ tab[i-1][j-1] or tab[i][j-1]
        # tab[i][j] = lst[j] or tab[i][j-1] or None
        tab = [[None] * (len(lst)) for _ in range(len(lst))]
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
        for _ in range(15):
            lst = [i for i in range(random.randint(10, 100))]
            for _ in range(len(lst)):
                random.shuffle(lst)
                llst.append(lst)
        map(test, llst)
        print 'pass:', self.__class__


# @problem: maximum sum of all increasing subsequences
class MaximumSumIncreasingSubsequence():
    def main(self, lst):
        tab = [0] * len(lst)
        for i in range(len(lst)):
            for j in range(i):
                if lst[j] < lst[i] and tab[j] + lst[i] > tab[i]:
                    tab[i] = tab[j] + lst[i]
        return max(tab)


# @problem: longest common subsequence
class LongestCommonSubsequence():
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
        tab = [[0] * (len(lst2) + 1) for _ in range(len(lst1) + 1)]
        for i in range(1, len(lst1) + 1):  # index of lst1
            for j in range(1, len(lst2) + 1):  # index of lst2
                if tab[i - 1][j - 1] < tab[i - 1][j] or tab[i - 1][j - 1] < tab[i][j - 1]:
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
        for _ in range(15):
            lst1 = [i for i in range(random.randint(5, 13))]
            random.shuffle(lst1)
            lst2 = [i for i in range(random.randint(5, 13))]
            random.shuffle(lst2)
            llst.append((lst1, lst2))
        map(test, llst)
        print 'pass:', self.__class__


# @problem: (balanced) partition problem
# determine whether a given multiset S of positive integers
# can be partitioned into two subsets S1 and S2 such that
# the sum of the numbers in S1 equals the sum of the numbers in S2
# 可以转换成子序列问题，即是否存在一个子序列其总和等于整个序列总和的一半
# 此问题被称为是最简单的NP-hard问题，与之关联的还有以下几种问题
# @problem: subset sum problem
# Given a set of positive integers and a value sum,
# determine if there is a subset with sum equal to given sum.
# @problem: optimization problem of partition
# partition a multiset S into two subsets S1 and S2
# such that the difference between the sum of S1 and S2 is minimized
# @problem: k-partition problem，即是否存在k个子集，其总和都为sum/k
class Partition():
    def main_1(self, lst):
        def recur(ind, sum):
            if ind < 0 or sum < 0:
                return False
            elif sum == 0:
                return True
            else:
                return recur(ind - 1, sum - lst[ind]) or recur(ind - 1, sum)

        return recur(len(lst) - 1, sum(lst) >> 1) if sum(lst) & 1 == 0 else False

    def main_2(self, lst):
        # optional: if sum(lst) & 1 != 0: return False
        if sum(lst) < 2:  # makes sense
            return False
        # tab[i][j] ~ tab[i-lst[j-1]][j-1] or tab[i][j-1]
        tab = [[False if i > 0 else True for _ in range(len(lst) + 1)] for i in range((sum(lst) >> 1) + 1)]
        for i in range(1, len(tab)):
            for j in range(1, len(lst) + 1):
                tab[i][j] = (tab[i - lst[j - 1]][j - 1] if i >= lst[j - 1] else False) \
                            or tab[i][j - 1]
                # optimization
                if tab[i][j]:
                    tab[i][j + 1:] = [True] * (len(tab[i]) - j - 1)
                    break

        set = []
        i, j = len(tab) - 1, len(lst)
        while i > 0:
            flg = False
            while j >= 0:
                if tab[i][j]:
                    flg = True
                    j -= 1
                    assert (i == 0 or j >= 0)
                else:
                    if flg:
                        assert (j + 1 < len(lst) and tab[i][j + 1])
                        j += 1
                        set.append(lst[j - 1])
                        i -= lst[j - 1]
                        assert (tab[i][j])
                    else:
                        assert (tab[i][:j] == [False] * j)
                        j = -1
                    break
            if j == -1:
                assert (not tab[i][j + 1])
                j = len(lst)
                i -= 1

        if tab[-1][-1]:
            assert (sum(lst) & 1 == 0 and sum(set) == sum(lst) >> 1)
        return tab[-1][-1]

    def testcase(self):
        def test(lst):
            assert (self.main_1(lst) == self.main_2(lst))

        llst = [[1, 1], [1, 1, 100]]
        for _ in range(15):
            lst = [i for i in range(1, random.randint(10, 50))]
            while sum(lst) & 1 != 0:
                lst = [i for i in range(1, random.randint(10, 50))]
            for _ in range(len(lst)):
                random.shuffle(lst)
                llst.append(lst)
        map(test, llst)
        print 'pass:', self.__class__


if __name__ == '__main__':
    LongestIncreasingSubsequence().testcase()
    LongestCommonSubsequence().testcase()
    Partition().testcase()
    print 'done'
