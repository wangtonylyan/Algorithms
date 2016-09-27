# -*- coding: utf-8 -*-


from base.string import StringTest
from suffix import SuffixArray


# 可重叠
class LongestRepeatedSubsequence(StringTest):
    def __init__(self):
        super(LongestRepeatedSubsequence, self).__init__()

    def _longestCommonPrefix(self, lst1, lst2):
        m = min(len(lst1), len(lst2))
        for i in range(m):
            if lst1[i] != lst2[i]:
                return i
        return m

    def main_bruteForce(self, lst):
        m, n = 0, 0
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                k = self._longestCommonPrefix(lst[i:], lst[j:])
                if n < k:
                    m, n = i, k
        return lst[m:m + n]

    def main_suffixSort(self, lst):
        sfx = [lst[i:] for i in range(len(lst))]
        sfx.sort()
        m, n = 0, 0
        for i in range(len(sfx) - 1):
            j = self._longestCommonPrefix(sfx[i], sfx[i + 1])
            if n < j:
                m, n = i, j
        return sfx[m][:n]

    def testcase(self):
        def test(cases):
            assert (all(len(self.main_bruteForce(case)) == len(self.main_suffixSort(case)) for case in cases))

        self._testcase(test, self._gencase())


class MinimumLexicographicRotation():
    def __init__(self):
        self.sfxFunc = SuffixArray().main_2

    def main(self, str):
        concat = str + str
        sfx = self.sfxFunc(concat)
        for s in sfx:
            if len(concat) - s >= len(str):
                return concat[s:s + len(str)]

    def testcase(self):
        assert (self.main('alabala') == 'aalabal')
        print 'pass:', self.__class__


if __name__ == '__main__':
    LongestRepeatedSubsequence().testcase()
    MinimumLexicographicRotation().testcase()
    print 'done'
