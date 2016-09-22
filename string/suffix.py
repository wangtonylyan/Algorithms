# -*- coding: utf-8 -*-

from string import String
from match import StringMatch


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
        sfx = [Suffix(i, self.ord(str[i]), self.ord(str[i + gap]) if i + gap < len(str) else -1)
               for i in range(len(str))]
        ind = [None] * len(str)
        sfx.sort(cmp=cmp)  # rely on its stability
        while gap < len(str):
            # rank0
            pre = sfx[0].rank0
            sfx[0].rank0 = 0
            ind[sfx[0].index] = 0
            for i in range(1, len(str)):
                if sfx[i].rank0 == pre and sfx[i].rank1 == sfx[i - 1].rank1:
                    pre = sfx[i].rank0
                    sfx[i].rank0 = sfx[i - 1].rank0
                else:
                    pre = sfx[i].rank0
                    sfx[i].rank0 = sfx[i - 1].rank0 + 1
                ind[sfx[i].index] = i
            # rank1
            for i in range(len(str)):
                if sfx[i].index + gap < len(str):
                    sfx[i].rank1 = sfx[ind[sfx[i].index + gap]].rank0
                else:
                    sfx[i].rank1 = -1
            sfx.sort(cmp=cmp)
            gap <<= 1
        return [s.index for s in sfx]

    def testcase(self):
        def test(case):
            assert (self.main_bruteForce(case[0]) == self.main_prefixDoubling(case[0]))

        self._testcase(test, self._gencase(each=1))


class PatternSearch(StringMatch):
    def __init__(self):
        self.suffixArrayFunc = SuffixArray().main_prefixDoubling

    def main_binarySearch(self, txt, pat):
        sfx = self.suffixArrayFunc(txt)
        low, high = 0, len(sfx) - 1
        while low <= high:
            mid = low + (high - low) / 2
            if sfx[mid] + len(pat) < len(txt):
                ret = cmp(pat, txt[sfx[mid]:sfx[mid] + len(pat)])
            else:
                ret = cmp(pat, txt[sfx[mid]:])
            if ret < 0:
                high = mid - 1
            elif ret > 0:
                low = mid + 1
            else:
                return sfx[mid]
        return None

    def testcase(self):
        def test(case):
            ret = self.main_binarySearch(case[0], case[1])
            assert (ret is not None)
            assert (0 <= ret < len(case[0]) and ret + len(case[1]) <= len(case[0]))
            assert (case[0][ret:ret + len(case[1])] == case[1])

        self._testcase(test, self._gencase(total=200))


class MinimumLexicographicRotation():
    def __init__(self):
        self.suffixArrayFunc = SuffixArray().main_prefixDoubling

    def main(self, str):
        concat = str + str
        sfx = self.suffixArrayFunc(concat)
        for s in sfx:
            if len(concat) - s >= len(str):
                return concat[s:s + len(str)]

    def testcase(self):
        assert (self.main('alabala') == 'aalabal')
        print 'pass:', self.__class__


if __name__ == '__main__':
    SuffixArray().testcase()
    PatternSearch().testcase()
    MinimumLexicographicRotation().testcase()
    print 'done'
