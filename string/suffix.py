# -*- coding: utf-8 -*-

from string import String


class SuffixArray(String):
    def __init__(self):
        super(SuffixArray, self).__init__()

    # O(n^2logn)
    def main_bruteForce(self, str):
        sfx = [None] * len(str)
        for i in range(len(str)):
            sfx[i] = (str[i:], i)
        sfx.sort(key=lambda x: x[0])
        return [s[1] for s in sfx]

    # O(nlogn)
    def main_prefixDoubling(self, str):
        class Suffix():
            def __init__(self, index, rank0, rank1):
                self.index = index
                self.rank0 = rank0
                self.rank1 = rank1

        def cmp(x, y):
            assert (isinstance(x, Suffix) and isinstance(y, Suffix))
            if x.rank0 < y.rank0 or (x.rank0 == y.rank0 and x.rank1 < y.rank1):
                return -1
            else:
                return 1

        gap = 1
        # sfx: rank->index
        sfx = [Suffix(i, self.ord(str[i]), self.ord(str[i + gap]) if i + gap < len(str) else -1)
               for i in range(len(str))]
        # inv: index->rank
        inv = [None] * len(str)  # inverse of 'sfx'
        sfx.sort(cmp=cmp)  # rely on its stability
        gap <<= 1
        while gap < len(str):
            # rank0
            pre = sfx[0].rank0
            sfx[0].rank0 = 0
            inv[sfx[0].index] = 0
            for i in range(1, len(str)):
                if sfx[i].rank0 == pre and sfx[i].rank1 == sfx[i - 1].rank1:
                    pre = sfx[i].rank0
                    sfx[i].rank0 = sfx[i - 1].rank0
                else:
                    pre = sfx[i].rank0
                    sfx[i].rank0 = sfx[i - 1].rank0 + 1
                inv[sfx[i].index] = i
            # rank1
            for i in range(len(str)):
                if sfx[i].index + gap < len(str):
                    sfx[i].rank1 = sfx[inv[sfx[i].index + gap]].rank0
                else:
                    sfx[i].rank1 = -1
            sfx.sort(cmp=cmp)
            gap <<= 1
        return [s.index for s in sfx]

    # O(n)
    def main_skew(self, str):
        # not implemented
        pass

    def testcase(self):
        def test(case):
            assert (self.main_bruteForce(case[0]) == self.main_prefixDoubling(case[0]))

        self._testcase(test, self._gencase(each=1, total=500))


class EnhancedSuffixArray(SuffixArray):
    def __init__(self):
        super(EnhancedSuffixArray, self).__init__()

    # longest common prefix, O(n)
    def main_lcp_Kasai(self, str, sfx):
        lcp = [None] * len(str)
        inv = [None] * len(str)
        for i in range(len(str)):
            inv[sfx[i]] = i
        k = 0
        for i in range(len(str)):
            if inv[i] == len(str) - 1:
                lcp[inv[i]] = 0
                k = 0
                continue
            j = sfx[inv[i] + 1]
            while i + k < len(str) and j + k < len(str) and str[i + k] == str[j + k]:
                k += 1
            lcp[inv[i]] = k
            if k > 0:
                k -= 1
        return lcp

    # compute longest common prefix during constructing suffix array
    def main_sfx_lcp_ManberMyers(self, str):
        # not implemented
        pass


class SuffixTree(String):
    def __init__(self):
        super(SuffixTree, self).__init__()


if __name__ == '__main__':
    SuffixArray().testcase()
    print 'done'
