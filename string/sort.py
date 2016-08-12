# -*- coding: utf-8 -*-
# @problem: string sorting
# @solution: lease-significant-digit-first (LSD), most-significant-digit-first (MSD)
# LSD和MSD算法思想与radix sort完全相同，都是基于counting sort
# 且习惯上都将字符串和数字的首位视作MSD，但不同的是
# 较短字符串的LSD被''填充，而较短数字的MSD被0填充


from string import String


class StringSort(String):
    def __init__(self):
        super(StringSort, self).__init__()
        self.funcs = [
            self.main_LSD,
            self.main_MSD,
        ]

    def main_LSD(self, lst):
        aux = [None] * len(lst)
        for w in range(max(map(len, lst)) - 1, -1, -1):
            cnt = [0] * (self.alphabet + 2)
            for i in lst:
                if w < len(i):
                    cnt[ord(i[w]) + 2] += 1
                else:
                    cnt[1] += 1
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            for i in lst:
                if w < len(i):
                    aux[cnt[ord(i[w]) + 1]] = i
                    cnt[ord(i[w]) + 1] += 1
                else:
                    aux[cnt[0]] = i
                    cnt[0] += 1
            lst, aux = aux, lst
        return lst

    def main_MSD(self, lst):
        def recur(low, high, wid):
            if high - low < 2 or wid >= max(map(len, lst[low:high])):
                return
            cnt = [0] * (self.alphabet + 2)
            for i in lst[low:high]:
                cnt[ord(i[wid]) + 2 if wid < len(i) else 1] += 1
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            aux = [None] * (high - low)
            for i in lst[low:high]:
                aux[cnt[ord(i[wid]) + 1 if wid < len(i) else 0]] = i
                cnt[ord(i[wid]) + 1 if wid < len(i) else 0] += 1
            lst[low:high] = aux

            assert (max(map(len, lst[low:low + cnt[0]])) <= wid if cnt[0] > 0 else True)
            assert (cnt[-1] == high - low)
            for i in range(len(cnt) - 1):
                recur(low + cnt[i], low + cnt[i + 1], wid + 1)

        recur(0, len(lst), 0)
        return lst

    def testcase(self):
        def test(case):
            cpy = case[:]
            cpy.sort()
            assert (all(f(case[:]) == cpy for f in self.funcs))

        self._testcase(test, self._gencase())


if __name__ == '__main__':
    StringSort().testcase()
    print 'done'
