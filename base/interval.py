# -*- coding: utf-8 -*-
# interval trichotomy for two intervals i and j that hold exactly one of the following three properties:
# (a) i and j overlap
# (b) i is to the left of j, i.e. i.high <= j.low
# (c) i is to the right of j, i.e. i.low >= j.high


from number import Number
from test import Test
import random


class Interval(Number):
    __slots__ = ['low', 'high']

    def __init__(self, low, high):
        # left-closed and right-open, [low, high)
        assert (0 <= low < high <= self.alphabet + 1)
        super(Interval, self).__init__()
        self.low = low
        self.high = high

    def __len__(self):
        return (self.high - self.low)

    def overlap(self, itv):
        assert (isinstance(itv, Interval))
        return (self.low < itv.high and self.high > itv.low)
        return (max(self.high, itv.high) - min(self.low, itv.low) < len(self) + len(itv))  # by distance

    def envelop(self, itv):
        assert (isinstance(itv, Interval))
        return (self.low <= itv.low and self.high >= itv.high)


class IntervalTest(Test):
    def __init__(self):
        super(IntervalTest, self).__init__()

    def _gencase(self, maxLen=100, each=1, total=100, overlap=True):
        cases = []
        for _ in range(total):
            case = []
            for _ in range(each):
                lst = []
                for _ in range(maxLen):
                    if overlap:
                        low = random.randint(0, Number.alphabet - 1)
                        high = random.randint(low + 1, Number.alphabet + 1)
                        lst.append((low, high))
                    else:
                        pass
                case.append(lst)
            cases.append(case)
        return cases

    def _testcase(self, test, cases):
        map(test, cases)
        print 'pass:', self.__class__, '-', len(cases)


if __name__ == '__main__':
    print 'done'
