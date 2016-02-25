# -*- coding: utf-8 -*-


import sys, random

sys.path.append("..")
import sort


# 合并排序相比于其他排序，无需过多的随机访问
# 非常适用于链表排序
class MergeSort(sort.Sort):
    def __init__(self):
        super(MergeSort, self).__init__()
        self.funcs.append(self.main_iter)
        self.funcs.append(self.main_recur)

    # bottom-up strategy
    # iterative sort with iterative merge
    def main_iter(self, lst):
        def _merge(low, mid, high):
            # auxliary space
            alst1 = lst[low:mid]
            alst2 = lst[mid:high]
            i, j = 0, 0
            while i < len(alst1) and j < len(alst2):
                if alst1[i] <= alst2[j]:
                    lst[low + i + j] = alst1[i]
                    i += 1
                else:
                    lst[low + i + j] = alst2[j]
                    j += 1
            if i == len(alst1):
                lst[low + i + j:high] = alst2[j:]
            else:
                assert (j == len(alst2))
                lst[low + i + j:high] = alst1[i:]

        step = 1
        while step < len(lst):
            i = 0
            while i + step + step < len(lst):
                _merge(i, i + step, i + step + step)
                i += step + step
            # 以下处理边界情况
            if i + step < len(lst):
                _merge(i, i + step, len(lst))
            step *= 2
        return lst

    # top-down strategy
    # recursive sort with recursive merge
    def main_recur(self, lst):
        def _merge(lst1, lst2):
            if len(lst1) == 0:
                return lst2
            elif len(lst2) == 0:
                return lst1
            if lst1[0] <= lst2[0]:
                return [lst1[0]] + _merge(lst1[1:], lst2)
            else:
                return [lst2[0]] + _merge(lst1, lst2[1:])

        # recursion and merge
        if len(lst) < 2:
            return lst
        mid = len(lst) >> 1
        return _merge(self.main_recur(lst[:mid]), self.main_recur(lst[mid:]))


# @problem:
# Inversion Count for an array indicates – how far (or close) the array is from being sorted.
# If array is already sorted then inversion count is 0. If array is sorted in reverse order that inversion count is the maximum.
# e.g. The sequence [2, 4, 1, 3, 5] has three inversions (2, 1), (4, 1), (4, 3).
class CountInversionsInArray():
    # recursive sort with iterative merge, in place
    def main(self, lst):
        # count inversions during merge
        def _merge(low, mid, high):
            count = 0
            alst1 = lst[low:mid]
            alst2 = lst[mid:high]
            i, j = 0, 0
            while i < len(alst1) and j < len(alst2):
                if alst1[i] <= alst2[j]:
                    lst[low + i + j] = alst1[i]
                    i += 1
                else:
                    lst[low + i + j] = alst2[j]
                    j += 1
                    count += len(alst1) - i  # the only difference with MergeSort
            if i == mid - low:
                lst[low + i + j:high] = alst2[j:]
            else:
                lst[low + i + j:high] = alst1[i:]
            return count

        def _recur(low, high):
            if high - low <= 1:
                return 0
            mid = low + ((high - low) >> 1)
            count = _recur(low, mid)
            count += _recur(mid, high)
            count += _merge(low, mid, high)
            return count

        return _recur(0, len(lst))

    def testcase(self):
        def func(lst):
            # brute-force algorithm
            count = 0
            for i in range(0, len(lst) - 1):
                for j in range(i + 1, len(lst)):
                    if lst[i] > lst[j]:
                        count += 1
            # check
            cpy = lst[:]
            cpy.sort()
            assert (self.main(lst) == count)
            assert (lst == cpy)

        cases = [[1], [1, 2], [2, 1]]
        for i in range(20):
            lst = [random.randint(0, 100) for i in range(random.randint(5, 50))]
            random.shuffle(lst)
            cases.append(lst)
        map(func, cases)


if __name__ == '__main__':
    MergeSort().testcase()
    CountInversionsInArray().testcase()
    print 'done'
