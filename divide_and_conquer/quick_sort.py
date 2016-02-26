# -*- coding: utf-8 -*-


import sys

sys.path.append("..")
import sort


class QuickSort(sort.Sort):
    def __init__(self):
        super(QuickSort, self).__init__()
        self.funcs.append(self.main)

    # in-place implementation
    # recursive sort with iterative partition
    def main(self, lst):
        # Quick sort is faster in practice, because its inner loop is efficiently
        # implemented on most architectures, and in most real-world data.
        def _partition(low, high):
            # pick first element as pivot
            flag = low
            for i in range(low + 1, high):
                if lst[i] < lst[low]:
                    flag += 1
                    lst[i], lst[flag] = lst[flag], lst[i]
            lst[low], lst[flag] = lst[flag], lst[low]
            return flag  # in-place partition, so returns index only

        def _recur(low, high):
            if high - low < 2:
                return
            mid = _partition(low, high)
            _recur(low, mid)
            _recur(mid + 1, high)

        if len(lst) < 2:
            return lst
        _recur(0, len(lst))
        return lst


if __name__ == '__main__':
    QuickSort().testcase()
    print 'done'
