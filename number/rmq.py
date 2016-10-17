# -*- coding: utf-8 -*-
# problem: range minimum/maximum query (RMQ)
# The RMQ comprises all variations of the problem of finding the smallest/biggest element
# in a contiguous subsequence of a list of items taken from a totally ordered set (usually numbers).
# This is one of the most extensively-studied problems in computer science,
# and many algorithms are known, each of which is appropriate for a specific variation.

import math
from base.number import NumberTest
from data_structure.tree.segment import SegmentTree


class RangeQuery(NumberTest):
    def __init__(self, cmp):
        super(RangeQuery, self).__init__()
        self.cmp = cmp
        self.funcs = [
            self.main_bruteForce,
            self.main_dynamic,
            self.main_blockDecomposition,
            self.main_sparseTable,
            self.main_segmentTree,
        ]

    # @param: [i, j)
    def main_bruteForce(self, lst):
        # 1) preprocess: O(1)
        pass
        # 2) query: O(n)
        low, high = yield
        while True:
            low, high = yield self.cmp(lst[low:high])

    def main_dynamic(self, lst):
        # 1) preprocess: O(n^2)
        tab = [[None] * (len(lst) + 1) for _ in range(len(lst))]
        for i in range(len(lst)):
            tab[i][i] = lst[i]
            for j in range(i + 1, len(lst) + 1):
                tab[i][j] = self.cmp(tab[i][j - 1], lst[j - 1])
        # 2) query: O(1)
        low, high = yield
        while True:
            low, high = yield tab[low][high]

    def main_blockDecomposition(self, lst):
        # 1) preprocess: O(n)
        blk = int(len(lst) ** 0.5)
        tab = []
        for i in range(0, len(lst), blk):
            tab.append(self.cmp(lst[i:i + blk]) if i + blk <= len(lst) else self.cmp(lst[i:]))
        # 2) query: O(n^0.5)
        low, high = yield
        while True:
            left, right = low / blk + 1, high / blk  # boundary of 'tab'
            if left < right:
                m = tab[left:right] + lst[low:left * blk] + lst[right * blk:high]
            else:
                assert (high - low < blk * 2)
                m = lst[low:high]
            low, high = yield self.cmp(m)

    def main_sparseTable(self, lst):
        # 1) preprocess: O(nlogn)
        # tab[i][j] == self.cmp([i:i + (1 << j)])
        tab = [[None] * (int(math.log(len(lst), 2)) + 1) for _ in range(len(lst))]
        for i in range(len(lst)):
            tab[i][0] = lst[i]
        j = 1
        while 1 << j <= len(lst):
            i = 0
            while i + (1 << j) <= len(lst):
                tab[i][j] = self.cmp(tab[i][j - 1], tab[i + (1 << (j - 1))][j - 1])
                i += 1
            j += 1
        # 2) query: O(1)
        low, high = yield
        while True:
            k = int(math.log(high - low, 2))  # floor
            assert (2 ** k <= high - low < 2 ** (k + 1))
            assert (low + (1 << k) > high - (1 << k))
            low, high = yield self.cmp(tab[low][k], tab[high - (1 << k)][k])

    def main_segmentTree(self, lst):
        def get(x, y):
            if x is not None and y is not None:
                ret = self.cmp(x, y)
            elif x is not None:
                ret = x
            elif y is not None:
                ret = y
            else:
                ret = None
            return ret

        # 1) preprocess: O(n)
        sgt = SegmentTree(lst, up=get)
        # 2) query: O(logn)
        low, high = yield
        while True:
            low, high = yield sgt.search(low, high)

    def testcase(self):
        def test(cases):
            for case in cases:
                funcs = [f(case) for f in self.funcs]
                map(lambda f: f.next(), funcs)
                for i in range(len(case)):
                    for j in range(i + 1, len(case) + 1):
                        ret = funcs[0].send((i, j))
                        assert all(ret == x for x in map(lambda f: f.send((i, j)), funcs[1:]))

        self._testcase(test, self._gencase(maxLen=100, each=1, total=100))


class RangeMinimumQuery(RangeQuery):
    def __init__(self):
        super(RangeMinimumQuery, self).__init__(cmp=min)


class RangeMaximumQuery(RangeQuery):
    def __init__(self):
        super(RangeMaximumQuery, self).__init__(cmp=max)


if __name__ == '__main__':
    RangeMinimumQuery().testcase()
    RangeMaximumQuery().testcase()
    print 'done'
