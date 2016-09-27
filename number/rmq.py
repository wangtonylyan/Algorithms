# -*- coding: utf-8 -*-

from base.number import NumberTest


class RangeMinimumQuery(NumberTest):
    def main_bruteForce(self, lst, low, high):
        # 1) preprocess: O(1)
        # 2) query: O(n)
        m = low
        for i in range(low + 1, high):
            if lst[i] < lst[m]:
                m = i
        return lst[m]

    def main_dynamic(self, lst, low, high):
        # 1) preprocess: O(n^2)
        tab = [[None] * len(lst) for _ in range(len(lst))]
        for i in range(len(lst)):
            tab[i][i] = lst[i]
            for j in range(i + 1, len(lst)):
                tab[i][j] = lst[j] if lst[j] < tab[i][j - 1] else tab[i][j - 1]
        # 2) query: O(1)
        return tab[low][high]

    def main_blockDecomposition(self, lst, low, high):
        # 1) preprocess: O(n)
        # 2) query: O(n^1/2)
        pass

    def main_sparseTable(self, lst, low, high):
        # 1) preprocess: O(nlogn)
        tab = [[None]]
        # 2) query: O(1)
        pass


if __name__ == '__main__':
    print 'done'
