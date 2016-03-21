# -*- coding: utf-8 -*-

# @problem: Given n activities with their start and finish times.
# Select the maximum number of activities that can be performed by a single person,
# assuming that a person can only work on a single activity at a time.
class ActivitySelection():
    def __init__(self):
        pass

    @staticmethod
    def _sort(lst, func):
        for i in range(len(lst) - 1):
            t = lst[i + 1]
            j = i
            while j >= 0 and func(lst[j]) > func(t):
                lst[j + 1] = lst[j]
                j -= 1
            lst[j + 1] = t

    def main_1(self, lst):
        # sort by finish time
        self._sort(lst, lambda x: x[1])
        ret = [lst[0]]
        i = 1
        while i < len(lst):
            if lst[i][0] >= ret[-1][1]:
                ret.append(lst[i])
            i += 1
        return len(ret)

    def main_2(self, lst):
        # sort by start time
        self._sort(lst, lambda x: x[0])
        ret = [lst[-1]]
        i = len(lst) - 2
        while i >= 0:
            if lst[i][1] <= ret[-1][0]:
                ret.append(lst[i])
            i -= 1
        return len(ret)

    def testcase(self):
        def test(lst):
            assert (self.main_1(lst[:]) == self.main_2(lst[:]))

        llst = [[(1, 2), (3, 4), (0, 6), (5, 7), (8, 9), (5, 9)], ]
        map(test, llst)


if __name__ == '__main__':
    ActivitySelection().testcase()
