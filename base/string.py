# -*- coding: utf-8 -*-

import random
from test import Test


class String(object):
    alphabet = ord('z') - ord('a') + 1  # 256  # number of legal characters by ASCII, [0,255]
    ord = lambda self, x: ord(x) - ord('a')


class StringTest(Test):
    def __init__(self):
        super(StringTest, self).__init__()

    def _gencase(self, fixed=False, maxLen=40, each=50, total=100):
        cases = []
        for _ in range(total):
            case = []
            width = random.randint(1, maxLen) if fixed else None
            for _ in range(each):
                width = width if fixed else random.randint(1, maxLen)
                case.append(''.join([chr(random.randint(ord('a'), ord('z'))) for _ in range(width)]))
            cases.append(case)
        return cases

    def _testcase(self, test, cases):
        map(test, cases)
        print 'pass:', self.__class__, '-', len(cases)


if __name__ == '__main__':
    cases = StringTest()._gencase()
    for case in cases:
        print case
        assert (isinstance(case, list) and len(case) > 0)
        assert (all(isinstance(i, str) and len(i) > 0 for i in case))
    print len(cases)
    print 'done'
