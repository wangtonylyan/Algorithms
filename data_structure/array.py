# -*- coding: utf-8 -*-
# data structure: array

import random


# @problem: 删除数组中的给定区间
class IntervalDeletion():
    def main(self, lst, low, high):
        shift = high - low
        assert (high - low >= 0)
        i = high
        while i < len(lst):
            lst[i - shift] = lst[i]
            i += 1
        return lst[:i - shift]

    def testcase(self):
        num = 100
        case = [i for i in range(num)]
        for s in range(num + 1):
            for i in range(len(case) - s):
                assert (self.main(case[:], i, i + s) == case[:i] + case[i + s:])

        print 'pass:', self.__class__


# @problem: 删除数组中连续的重复元素
class ReplicateDeletion():
    def main(self, lst):
        i, j = 0, 1
        while j < len(lst):
            if lst[i] == lst[j]:
                j += 1
            else:
                i += 1
                lst[i] = lst[j]
                j += 1
        return lst[:i + 1]

    def testcase(self):
        for t in range(100):
            case = []
            for i in range(20):
                for j in range(random.randint(1, 20)):
                    case.append(i)
            assert (self.main(case[:]) == [k for k in range(i + 1)])

        print 'pass:', self.__class__


# @problem: rotation
# rotate a array in linear time and constant space
class Rotation():
    def __init__(self):
        self.funcs = [self.main_reverse,
                      self.main_swap_recur,
                      self.main_swap_iter]

    def main_reverse(self, lst, shift):
        assert (0 <= shift <= len(lst))

        def reverse(low, high):
            assert (0 <= low <= high <= len(lst))
            for i in range(0, (high - low) >> 1):
                lst[low + i], lst[high - 1 - i] = lst[high - 1 - i], lst[low + i]

        reverse(0, shift)
        reverse(shift, len(lst))
        reverse(0, len(lst))
        return lst

    def main_swap_recur(self, lst, shift):
        def swap(low, high, shift):
            if high - low < 2 or shift == 0:
                return False
            h = low + shift
            l = high - shift
            assert (h <= l)
            lst[low:h], lst[l:high] = lst[l:high], lst[low:h]
            if h == l:
                return False
            return True

        def shiftLeft(low, high, shift):
            if not swap(low, high, shift):
                return
            high -= shift
            if 0 <= low + shift <= high - shift:
                shiftLeft(low, high, shift)
            else:
                shiftRight(low, high, high - shift - low)

        def shiftRight(low, high, shift):
            if not swap(low, high, shift):
                return
            low += shift
            if 0 <= low + shift <= high - shift:
                shiftRight(low, high, shift)
            else:
                shiftLeft(low, high, high - shift - low)

        low, high = 0, len(lst)
        if low + shift <= high - shift:
            shiftLeft(low, high, shift)
        else:
            shiftRight(low, high, high - shift)
        return lst

    def main_swap_iter(self, lst, shift):
        low, high = 0, len(lst)
        left = True
        while low < high and shift > 0:
            h = low + shift
            l = high - shift
            if h <= l:  # rotate anyway
                lst[low:h], lst[l:high] = lst[l:high], lst[low:h]
                if left:
                    high = l
                else:
                    low = h
            else:
                shift = l - low
                left = not left
        return lst

    def testcase(self):
        num = 900
        case = [i for i in range(num)]
        for s in range(num + 1):
            assert (reduce(lambda x, y: x if x == y(case[:], s) else None,
                           self.funcs[1:], self.funcs[0](case[:], s)) != None)

        print 'pass:', self.__class__


if __name__ == '__main__':
    IntervalDeletion().testcase()
    ReplicateDeletion().testcase()
    Rotation().testcase()
