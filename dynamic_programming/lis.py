# -*- coding: utf-8 -*-
# problem: longest increasing subsequence

import random


class LIS():
    # longest strictly increasing subsequence
    def brute_force(self, lst):
        # lis记录了以lst中每个字符为结尾的最大递增序列的长度
        lis = [1 for i in range(len(lst))]
        for i in range(1, len(lst)):
            for j in range(0, i):
                if lst[i] > lst[j] and lis[i] < lis[j] + 1:
                    lis[i] = lis[j] + 1
        return max(lis)

    # longest (not strictly) increasing subsequence
    def main(self, lst):
        # tab[i][j] ~ tab[i][j-1] or tab[i-1][j-1] or tab[i-1][j]
        tab = [[None for col in range(len(lst))] for row in range(len(lst))]
        for i in range(len(lst)):  # i: length of sequence
            for j in range(len(lst)):  # j: length of increasing subsequence
                if i < j:
                    continue
                elif j == 0:
                    if i == 0 or lst[i] < tab[i - 1][j]:
                        tab[i][j] = lst[i]
                    else:
                        tab[i][j] = tab[i - 1][j]
                else:
                    # the possibilities of the existence of
                    # tab[i][j-1], tab[i-1][j-1] and tab[i-1][j] are decreasing
                    if tab[i][j - 1] == None or tab[i - 1][j - 1] == None:
                        assert (tab[i - 1][j] == None)
                        assert (tab[i][j - 1] == None or tab[i][j - 1] == lst[i])
                        continue
                    elif tab[i - 1][j] == None:
                        assert (tab[i][j - 1] <= tab[i - 1][j - 1])
                        if lst[i] >= tab[i - 1][j - 1]:  # not strictly increasing
                            tab[i][j] = lst[i]
                    else:
                        if lst[i] > tab[i - 1][j] or lst[i] < tab[i - 1][j - 1]:
                            tab[i][j] = tab[i - 1][j]
                        else:  # not strictly increasing
                            tab[i][j] = lst[i]
        for j in range(len(lst) - 1, -1, -1):
            if tab[len(lst) - 1][j] != None:
                return j + 1
        assert (False)

    def testcase(self):
        def test(lst):
            assert (self.brute_force(lst) == self.main(lst))

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
