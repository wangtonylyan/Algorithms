# -*- coding: utf-8 -*-

from sort import Sort


class QuickSort(Sort):
    def __init__(self):
        super(QuickSort, self).__init__()
        self.part = self._partition_one_way
        # self.part = self._partition_two_way
        self.funcs.append(self.main_recur)
        self.funcs.append(self.main_iter)

    # Quick sort is faster in practice, because its inner loop is efficiently
    # implemented on most architectures, and in most real-world data.
    @staticmethod
    def _partition_one_way(lst, low, high):
        flag = low
        for i in range(low + 1, high):
            if lst[i] < lst[low]:
                flag += 1
                lst[i], lst[flag] = lst[flag], lst[i]
        lst[low], lst[flag] = lst[flag], lst[low]
        return flag  # in-place partition, so returns index only

    @staticmethod
    def _partition_two_way(lst, low, high):
        flag = lst[low]
        i, j = low, high - 1
        while i != j:
            while j > i and lst[j] >= flag:
                j -= 1
            lst[i] = lst[j]
            while i < j and lst[i] <= flag:
                i += 1
            lst[j] = lst[i]
        lst[i] = flag
        return i

    def main_recur(self, lst):
        def _sort(lst, low, high):
            if high - low < 2:
                return
            mid = self.part(lst, low, high)
            _sort(lst, low, mid)
            _sort(lst, mid + 1, high)

        if len(lst) < 2:
            return lst
        _sort(lst, 0, len(lst))
        return lst

    def main_iter(self, lst):
        stk = [None] * (len(lst) + 1)
        top = 0
        stk[top] = 0
        top += 1
        stk[top] = len(lst)
        while top > -1:
            high = stk[top]
            top -= 1
            low = stk[top]
            top -= 1
            mid = self.part(lst, low, high)
            if mid - low > 1:
                top += 1
                stk[top] = low
                top += 1
                stk[top] = mid
            if high - (mid + 1) > 1:
                top += 1
                stk[top] = mid + 1
                top += 1
                stk[top] = high
        return lst


if __name__ == '__main__':
    QuickSort().testcase()
    print 'done'
