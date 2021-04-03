# -*- coding: utf-8 -*-

import random
from number.sort import Sort


# @problem: Given two sorted arrays A and B, A has a large enough buffer
# at the end to hold B. Merge B into A in sorted order.
class InPlaceMerge():
    # start merging from the largest
    def main(self, lst1, lst2):
        k = len(lst1) - 1
        i = len(lst1) - len(lst2) - 1
        j = len(lst2) - 1
        while i >= 0 and j >= 0:
            if lst1[i] > lst2[j]:
                lst1[k] = lst1[i]
                i -= 1
            else:
                lst1[k] = lst2[j]
                j -= 1
            k -= 1
        while j >= 0:
            lst1[k] = lst2[j]
            j -= 1
            k -= 1
        return lst1

    def testcase(self):
        ret = [i for i in range(20)]

        lst1 = [i for i in range(10)]
        lst2 = [i for i in range(10, 20)]
        lst1 += [None] * len(lst2)
        assert (self.main(lst1, lst2) == ret)

        lst1 = [i for i in range(10, 20)]
        lst2 = [i for i in range(10)]
        lst1 += [None] * len(lst2)
        assert (self.main(lst1, lst2) == ret)

        print 'pass:', self.__class__


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
            t1 = lst[low:mid]
            t2 = lst[mid:high]
            i, j = 0, 0
            while i < len(t1) and j < len(t2):
                if t1[i] <= t2[j]:
                    lst[low + i + j] = t1[i]
                    i += 1
                else:
                    lst[low + i + j] = t2[j]
                    j += 1
                    count += len(t1) - i  # the only difference with MergeSort

            if i == mid - low:
                lst[low + i + j:high] = t2[j:]
            else:
                lst[low + i + j:high] = t1[i:]
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
        def test(lst):
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
        for _ in range(20):
            lst = [random.randint(0, 100)
                   for i in range(random.randint(5, 50))]
            random.shuffle(lst)
            cases.append(lst)
        map(test, cases)
        print 'pass:', self.__class__


if __name__ == '__main__':
    InPlaceMerge().testcase()
    CountInversionsInArray().testcase()

    print('done')
