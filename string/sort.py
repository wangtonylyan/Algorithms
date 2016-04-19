# -*- coding: utf-8 -*-
# problem: string sorting
# solution: lease-significant-digit-first (LSD), most-significant-digit-first (MSD)

import random


class StringSort(object):
    def __init__(self):
        self.alphabet = 256  # number of legal characters by ASCII, [1,255]

    # @param type: 0==fixed length string, 1==variable length string
    def testcase(self, type):
        def test(case):
            ret = self.main(case[:])
            case.sort()
            if ret != case:
                print ret
                print case
            assert (ret == case)

        cases = []
        for i in range(20):
            width = random.randint(1, 25) if type == 0 else 0
            case = []
            for j in range(20):
                s = ''
                width = width if type == 0 else random.randint(1, 25)
                for k in range(width):
                    s += chr(random.randint(ord('a'), ord('z')))
                case.append(s)
            cases.append(case)

        map(test, cases)
        print 'pass:', self.__class__


class LSDFixed(StringSort):
    def __init__(self):
        super(LSDFixed, self).__init__()

    def main(self, lst):
        assert (reduce(lambda x, y: x and len(lst[0]) == len(y), lst[1:], True))  # fixed length
        width = len(lst[0])
        for w in range(width - 1, -1, -1):
            # 1) compute frequency counts
            cnt = [0] * self.alphabet
            for i in lst:
                cnt[ord(i[w]) + 1] += 1
            # 2) transfrom counts to indices
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            # 3) distribute the records from lst to aux
            aux = [None] * len(lst)
            for i in lst:
                aux[cnt[ord(i[w])]] = i
                cnt[ord(i[w])] += 1
            # 4) store result back into lst by exchanging both references
            lst, aux = aux, lst
        return lst

    def testcase(self):
        super(LSDFixed, self).testcase(0)


class LSDVariable(StringSort):
    def __init__(self):
        super(LSDVariable, self).__init__()

    def main(self, lst):
        width = max(map(lambda x: len(x), lst))
        for w in range(width - 1, -1, -1):
            cnt = [0] * self.alphabet
            for i in lst:
                # 较短字符串通常都是根据实际情况
                # 利用空闲的cnt[0]或cnt[-1]来统计
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
        super(LSDVariable, self).testcase(1)


class MSD(StringSort):
    def __init__(self):
        super(MSD, self).__init__()

    def main(self, lst):
        def recur(low, high, ind):
            if high - low < 2 or ind >= max(map(lambda x: len(x), lst[low:high])):
                return
            cnt = [0] * self.alphabet
            for i in lst[low:high]:
                cnt[ord(i[ind]) + 1 if ind < len(i) else 0 + 1] += 1
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            aux = [None] * (high - low)
            for i in lst[low:high]:
                aux[cnt[ord(i[ind]) if ind < len(i) else 0]] = i
                cnt[ord(i[ind]) if ind < len(i) else 0] += 1
            lst[low:high] = aux

            recur(low, cnt[0], ind + 1)
            for i in range(len(cnt) - 1):
                recur(low + cnt[i], low + cnt[i + 1], ind + 1)
            assert (cnt[-1] == high - low)

        recur(0, len(lst), 0)
        return lst

    def testcase(self):
        super(MSD, self).testcase(1)


if __name__ == '__main__':
    LSDFixed().testcase()
    LSDVariable().testcase()
    MSD().testcase()
    print 'done'
