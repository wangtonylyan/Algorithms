# -*- coding: utf-8 -*-
# problem: string sorting
# solution: LSD, MSD

import random


class StringSort(object):
    def __init__(self):
        self.alphabet = 256  # number of legal characters by ASCII, [1,255]

    # @param type: 0==fixed length string, 1==variable length string
    def testcase(self, type, func=cmp):
        def test(case):
            ret = self.main(case[:])
            case.sort(func)
            if ret != case:
                print ret, case
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


# algorithm: least-significant-digit-first string sort
class FixedLengthLSD(StringSort):
    def __init__(self):
        super(FixedLengthLSD, self).__init__()

    def main(self, lst):
        assert (reduce(lambda x, y: x and len(lst[0]) == len(y), lst[1:], True))  # fixed length
        width = len(lst[0])
        for w in range(width - 1, -1, -1):
            # 1) compute frequency counts
            cnt = [0] * self.alphabet
            for i in lst:
                cnt[ord(i[w])] += 1
            # 2) transfrom counts to indices
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            # 3) distribute the records from lst to aux
            aux = [None] * len(lst)
            for i in lst:
                aux[cnt[ord(i[w]) - 1]] = i
                cnt[ord(i[w]) - 1] += 1
            # 4) store result back into lst by exchanging both references
            lst, aux = aux, lst
        return lst

    def testcase(self):
        super(FixedLengthLSD, self).testcase(0)


# 变长字符串排序有两种
# 1)将各个字符串的首字母对齐，不足的低有效位用0补齐，即cmp的实现方式
# 2)将各个字符串的尾字母对齐，不足的高有效位用0补齐，即此处的实现方式
class VariableLengthLSD(StringSort):
    def __init__(self):
        super(VariableLengthLSD, self).__init__()

    def main(self, lst):
        width = max(map(lambda x: len(x), lst))
        for w in range(1, width + 1):
            cnt = [0] * self.alphabet
            for i in lst:
                if w > len(i):
                    cnt[1] += 1
                else:
                    cnt[ord(i[-w]) + 1] += 1
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            aux = [None] * len(lst)
            for i in lst:
                if w > len(i):
                    aux[cnt[0]] = i
                    cnt[0] += 1
                else:
                    aux[cnt[ord(i[-w])]] = i
                    cnt[ord(i[-w])] += 1
            lst, aux = aux, lst
        return lst

    def testcase(self):
        def _cmp(s1, s2):
            if len(s1) < len(s2):
                return -1
            elif len(s1) > len(s2):
                return 1
            else:
                return cmp(s1, s2)

        super(VariableLengthLSD, self).testcase(1, _cmp)


class MSD(StringSort):
    def __init__(self):
        super(MSD, self).__init__()

    def main(self, lst):
        return lst

    def testcase(self):
        # super(MSD, self).testcase(1)
        pass


if __name__ == '__main__':
    FixedLengthLSD().testcase()
    VariableLengthLSD().testcase()
    MSD().testcase()
    print 'done'
