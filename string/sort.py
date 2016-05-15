# -*- coding: utf-8 -*-
# problem: string sorting
# solution: lease-significant-digit-first (LSD), most-significant-digit-first (MSD)
# LSD和MSD算法思想与radix sort完全相同，都是基于counting sort
# 且习惯上都将字符串和数字的首位视作MSD，但不同的是
# 较短字符串的LSD被''填充，而较短数字的MSD被0填充


import random


class StringSort(object):
    def __init__(self):
        self.alphabet = 256  # number of legal characters by ASCII, [1,255]

    # @param type: 0==variable length string, 1==fixed length string
    def testcase(self, type=0):
        def test(case):
            ret = self.main(case[:])
            case.sort()
            if ret != case:
                print ret
                print case
            assert (ret == case)

        cases = []
        for i in range(20):
            width = random.randint(1, 25) if type == 1 else 0
            case = []
            for j in range(20):
                s = ''
                width = width if type == 1 else random.randint(1, 25)
                for k in range(width):
                    s += chr(random.randint(ord('a'), ord('z')))
                case.append(s)
            cases.append(case)

        map(test, cases)
        print 'pass:', self.__class__


class LSD(StringSort):
    def __init__(self):
        super(LSD, self).__init__()

    def main(self, lst):
        width = max(map(len, lst))
        for w in range(width - 1, -1, -1):
            cnt = [0] * self.alphabet
            for i in lst:
                # 较短字符串通常都是根据实际情况，利用空闲的cnt[1]或cnt[-1]来统计
                if w >= len(i):
                    cnt[0 + 1] += 1
                else:
                    cnt[ord(i[w]) + 1] += 1
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            aux = [None] * len(lst)
            for i in lst:
                if w >= len(i):
                    aux[cnt[0]] = i
                    cnt[0] += 1
                else:
                    aux[cnt[ord(i[w])]] = i
                    cnt[ord(i[w])] += 1
            lst, aux = aux, lst
        return lst

    def testcase(self):
        super(LSD, self).testcase()


class MSD(StringSort):
    def __init__(self):
        super(MSD, self).__init__()

    def main(self, lst):
        def recur(low, high, wid):
            if high - low < 2 or wid >= max(map(len, lst[low:high])):
                return
            cnt = [0] * self.alphabet
            for i in lst[low:high]:
                # 由于只涵盖了[1,255]，因此空闲的cnt[1]可以用来统计长度较短的字符串个数
                # 否则所有ASCII字符的索引值偏移量都将变为2
                cnt[ord(i[wid]) + 1 if wid < len(i) else 0 + 1] += 1
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            aux = [None] * (high - low)
            for i in lst[low:high]:
                aux[cnt[ord(i[wid]) if wid < len(i) else 0]] = i
                cnt[ord(i[wid]) if wid < len(i) else 0] += 1
            lst[low:high] = aux

            assert (max(map(len, lst[low:low + cnt[0]])) <= wid if cnt[0] > 0 else True)
            assert (cnt[-1] == high - low)
            for i in range(len(cnt) - 1):
                recur(low + cnt[i], low + cnt[i + 1], wid + 1)

        recur(0, len(lst), 0)
        return lst

    def testcase(self):
        super(MSD, self).testcase()


if __name__ == '__main__':
    LSD().testcase()
    MSD().testcase()
    print 'done'
