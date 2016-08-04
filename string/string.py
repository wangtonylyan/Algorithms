# -*- coding: utf-8 -*-

import random


class String(object):
    def __init__(self):
        self.alphabet = ord('z') + 1  # 256  # number of legal characters by ASCII, [0,255]

    def _gencase(self, fixed=False, maxLen=40, each=50, total=100):
        cases = []
        for _ in range(total):
            case = []
            width = random.randint(1, maxLen) if fixed else None
            for _ in range(each):
                s = ''
                width = width if fixed else random.randint(1, maxLen)
                for _ in range(width):
                    s += chr(random.randint(ord('a'), ord('z')))
                case.append(s)
            cases.append(case)
        return cases

    def _testcase(self, test, cases):
        map(test, cases)
        print 'pass:', self.__class__, '-', len(cases)


if __name__ == '__main__':
    print 'done'
