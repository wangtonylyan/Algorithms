# -*- coding: utf-8 -*-
# @problem: string sorting
# @solution: lease-significant-digit-first (LSD), most-significant-digit-first (MSD)
# LSD和MSD算法思想与radix sort完全相同，都是基于counting sort
# 且习惯上都将字符串和数字的首位视作MSD，但不同的是
# 较短字符串的LSD被''填充，而较短数字的MSD被0填充


from base.string import String, StringTest


class StringSort(String, StringTest):
    def __init__(self):
        super(StringSort, self).__init__()
        self.funcs = [
            self.main_LSD,
            self.main_MSD,
        ]

    def main_LSD(self, str):
        aux = [None] * len(str)
        for w in range(max(map(len, str)) - 1, -1, -1):
            cnt = [0] * (self.alphabet + 2)
            for i in str:
                if w < len(i):
                    cnt[self.ord(i[w]) + 2] += 1
                else:
                    cnt[1] += 1
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            for i in str:
                if w < len(i):
                    aux[cnt[self.ord(i[w]) + 1]] = i
                    cnt[self.ord(i[w]) + 1] += 1
                else:
                    aux[cnt[0]] = i
                    cnt[0] += 1
            str, aux = aux, str
        return str

    def main_MSD(self, str):
        def recur(low, high, wid):
            if high - low < 2 or wid >= max(map(len, str[low:high])):
                return
            cnt = [0] * (self.alphabet + 2)
            for i in str[low:high]:
                cnt[self.ord(i[wid]) + 2 if wid < len(i) else 1] += 1
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            aux = [None] * (high - low)
            for i in str[low:high]:
                aux[cnt[self.ord(i[wid]) + 1 if wid < len(i) else 0]] = i
                cnt[self.ord(i[wid]) + 1 if wid < len(i) else 0] += 1
            str[low:high] = aux

            assert (max(map(len, str[low:low + cnt[0]])) <= wid if cnt[0] > 0 else True)
            assert (cnt[-1] == high - low)
            for i in range(len(cnt) - 1):
                recur(low + cnt[i], low + cnt[i + 1], wid + 1)

        recur(0, len(str), 0)
        return str

    def testcase(self):
        def test(case):
            cpy = case[:]
            cpy.sort()
            assert (all(f(case[:]) == cpy for f in self.funcs))

        self._testcase(test, self._gencase())


if __name__ == '__main__':
    StringSort().testcase()
    print 'done'
