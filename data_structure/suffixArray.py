# -*- coding: utf-8 -*-

from string.string import String


class SuffixArray(String):
    def __init__(self):
        super(SuffixArray, self).__init__()

    def main_bruteForce(self, str):
        sfx = [None] * len(str)
        for i in range(len(str)):
            sfx[i] = (str[i:], i)
        sfx.sort(key=lambda x: x[0])
        return [s[1] for s in sfx]

    def main_nlogn(self, str):
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
            '''
            ret1 = self.main_bruteForce(case[0])
            ret2 = self.main_nlogn(case[0])
            if ret1 != ret2:
                print case[0]
                print ret1
                print ret2
            '''
            assert (self.main_bruteForce(case[0]) == self.main_nlogn(case[0]))

        self._testcase(test, self._gencase(each=1))


if __name__ == '__main__':
    SuffixArray().testcase()
    print 'done'
