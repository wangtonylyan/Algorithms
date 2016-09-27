# -*- coding: utf-8 -*-
# problem: range minimum/maximum query (RMQ)
# The RMQ comprises all variations of the problem of finding the smallest/biggest element
# in a contiguous subsequence of a list of items taken from a totally ordered set (usually numbers).
# This is one of the most extensively-studied problems in computer science,
# and many algorithms are known, each of which is appropriate for a specific variation.

import math
from base.number import NumberTest


class RangeMinimumQuery(NumberTest):
    def __init__(self):
        super(RangeMinimumQuery, self).__init__()
        self.funcs = [
            self.main_bruteForce,
            self.main_dynamic,
            self.main_blockDecomposition,
        ]

    def main_bruteForce(self, lst):
        # 1) preprocess: O(1)
        pass
        # 2) query: O(n)
        low, high = yield
        while True:
            assert (0 <= low < high <= len(lst))
            low, high = yield min(lst[low:high])

    def main_dynamic(self, lst):
        # 1) preprocess: O(n^2)
        tab = [[None] * len(lst) for _ in range(len(lst))]
        for i in range(len(lst)):
            tab[i][i] = lst[i]
            for j in range(i + 1, len(lst)):
                tab[i][j] = lst[j] if lst[j] < tab[i][j - 1] else tab[i][j - 1]
        # 2) query: O(1)
        low, high = yield
        while True:
            assert (0 <= low < high <= len(lst))
            low, high = yield tab[low][high]

    def main_blockDecomposition(self, lst):
        # 1) preprocess: O(n)
        blk = int(len(lst) ** 0.5)
        tab = []
        for i in range(0, len(lst), blk):
            tab.append(min(lst[i:i + blk]) if i + blk < len(lst) else min(lst[i:len(lst)]))
        # 2) query: O(n^0.5)
        low, high = yield
        while True:
            assert (0 <= low < high <= len(lst))
            left, right = low / blk + 1, high / blk  # boundary of 'tab'
            if left < right:
                m = tab[left:right] + lst[low:low + left * blk] + lst[right * blk:high]
            else:
                assert (high - low < blk * 2)
                m = lst[low:high]
            low, high = yield min(m)

    def main_sparseTable(self, lst):
        # 1) preprocess: O(nlogn)
        tab = [[None] * (math.sqrt(len(lst))) for _ in range(len(lst))]
        for i in range(len(lst)):
            j = 0
            while i + (1 << j) - 1 <= len(lst):
                tab[i][j] = min(tab[i][j - 1], tab[i + (1 << (j - 1)) - 1][j - 1])
                j += 1
        # 2) query: O(1)
        low, high = yield
        while True:
            assert (0 <= low < high <= len(lst))
            low, high = yield

    def testcase(self):
        def test(cases):
            for case in cases:
                funcs = [f(case) for f in self.funcs]
                map(lambda f: f.next(), funcs)
                for i in range(len(case) - 1):
                    for j in range(i + 1, len(case)):
                        ret = funcs[0].send((i, j))
                        assert (ret == x for x in map(lambda f: f.send((i, j)), funcs[1:]))

        self._testcase(test, self._gencase(maxLen=100, each=1, total=500))


if __name__ == '__main__':
    RangeMinimumQuery().testcase()
    print 'done'
