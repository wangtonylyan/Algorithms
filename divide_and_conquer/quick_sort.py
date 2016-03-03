# -*- coding: utf-8 -*-


import sys

sys.path.append("..")
import sort


class QuickSort(sort.Sort):
    def __init__(self):
        super(QuickSort, self).__init__()
        self.funcs.append(self.main_recur)
        self.funcs.append(self.main_iter)

    # Quick sort is faster in practice, because its inner loop is efficiently
    # implemented on most architectures, and in most real-world data.
    @staticmethod
    def _partition(lst, low, high):
        # pick first element as pivot
        flag = low
        for i in range(low + 1, high):
            if lst[i] < lst[low]:
                flag += 1
                lst[i], lst[flag] = lst[flag], lst[i]
        lst[low], lst[flag] = lst[flag], lst[low]
        return flag  # in-place partition, so returns index only

    def main_recur(self, lst):
        def _sort(lst, low, high):
            if high - low < 2:
                return
            mid = self._partition(lst, low, high)
            _sort(lst, low, mid)
            _sort(lst, mid + 1, high)

        if len(lst) < 2:
            return lst
        _sort(lst, 0, len(lst))
        return lst

    def main_iter(self, lst):
        stack = [None for i in range(0, len(lst) + 1)]
        top = 0
        stack[top] = 0
        top += 1
        stack[top] = len(lst)
        while top > -1:
            high = stack[top]
            top -= 1
            low = stack[top]
            top -= 1
            mid = self._partition(lst, low, high)
            if mid - low > 1:
                top += 1
                stack[top] = low
                top += 1
                stack[top] = mid
            if high - (mid + 1) > 1:
                top += 1
                stack[top] = mid + 1
                top += 1
                stack[top] = high
        return lst


if __name__ == '__main__':
    QuickSort().testcase()
    print 'done'
