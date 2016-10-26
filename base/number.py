# -*- coding: utf-8 -*-

import random
from test import Test


class Number(object):
    alphabet = 10000  # [0, 10000]

    def __init__(self):
        super(Number, self).__init__()


class NumberTest(Test):
    def __init__(self):
        super(NumberTest, self).__init__()

    @classmethod
    def _testcase(cls, test, cases):
        map(test, cases)
        print 'pass:', cls, '-', len(cases)

    @classmethod
    def _gencase(cls, fixed=False, minLen=1, maxLen=50, each=50, total=100, dup=True):
        cases = []
        for _ in range(total):
            case = []
            width = random.randint(minLen, maxLen) if fixed else None
            for _ in range(each):
                width = width if fixed else random.randint(minLen, maxLen)
                if dup:
                    case.append([random.randint(0, Number.alphabet) for _ in range(width)])
                else:
                    assert (width <= Number.alphabet + 1)
                    low = random.randint(0, Number.alphabet - width)
                    lst = [_ for _ in range(low, low + width)]
                    random.shuffle(lst)
                    case.append(lst)
            cases.append(case)
        return cases


if __name__ == '__main__':
    cases = NumberTest()._gencase()
    for case in cases:
        print case
        assert (isinstance(case, list) and len(case) > 0)
        for lst in case:
            assert (isinstance(lst, list) and len(lst) > 0)
            assert (all(isinstance(i, int) and 0 <= i <= Number.alphabet for i in lst))
    print len(cases)
    print 'done'
