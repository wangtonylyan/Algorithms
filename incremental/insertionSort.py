# -*- coding: utf-8 -*-

from number.sort import Sort


# 插入排序非常适用于输入域增量式地动态变化
class InsertionSort(Sort):
    def main_recur(self, lst):
        # inner loop: insert (bubble up) lst[0] into sorted lst[1:]
        def _insert(lst):
            if len(lst) < 2 or lst[0] <= lst[1]:
                return lst
            lst[0], lst[1] = lst[1], lst[0]
            return [lst[0]] + _insert(lst[1:])

        # outer loop: recursion and insert
        if len(lst) < 2:
            return lst
        lst[1:] = self.main_recur(lst[1:])
        return _insert(lst)



# @problem:
# Given an unsorted array arr[0..n-1] of size n,
# find the minimum length subarray arr[s..e]
# such that sorting this subarray makes the whole array sorted.
class FindMinLengthUnsortedSubarray():
    # O(nlogn), based on insertion sort
    def main_sort(self, lst):
        low = len(lst)  # the larger the better
        high = 0  # the smaller the better
        for i in range(len(lst) - 1):
            t = lst[i + 1]
            j = i
            while j >= 0 and lst[j] > t:
                lst[j + 1], lst[j] = lst[j], lst[j + 1]
                j -= 1
            if j != i:
                if low > j + 1:
                    low = j + 1
                if high < i + 1:
                    high = i + 1
            lst[j + 1] = t
        if low >= high:  # lst has already been sorted
            low, high = -1, -1
        return (low, high)

    # O(n), based on linear search
    def main_search(self, lst):
        low, high = 0, len(lst) - 1
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                low = i
                break
        for i in range(len(lst) - 1, 0, -1):
            if lst[i] < lst[i - 1]:
                high = i
                break
        assert (low <= high)
        m, n = lst[low], lst[high]
        for i in range(low, high + 1):
            if lst[i] < m:
                m = lst[i]
            if lst[i] > n:
                n = lst[i]
        for i in range(low):
            if lst[i] > m:
                low = i
                break
        for i in range(len(lst) - 1, high, -1):
            if lst[i] < n:
                high = i
                break
        return (low, high)

    def testcase(self):
        def test(func):
            assert (func([10, 12, 20, 30, 25, 40, 32, 31, 35, 50, 60]) == (3, 8))
            assert (func([0, 1, 15, 25, 6, 7, 30, 40, 50]) == (2, 5))
            assert (func([1, 2, 4, 7, 10, 11, 7, 12, 3, 7, 16, 18, 19]) == (2, 9))
            print 'pass:', func

        map(test, [self.main_sort, self.main_search])


if __name__ == '__main__':
    InsertionSort().testcase()
    ShellSort().testcase()
    FindMinLengthUnsortedSubarray().testcase()
    print 'done'
