# -*- coding: utf-8 -*-
# problem: find the k-th smallest element in a collection
# solution: sort-based selection

import random


class Select():
    # @solution: bubble-based selection
    def main_bubble(self, lst, k):
        for i in range(k + 1):
            for j in range(len(lst) - 1, i, -1):
                if lst[j] < lst[j - 1]:
                    lst[j], lst[j - 1] = lst[j - 1], lst[j]
        return lst[k]

    # @solution: quick-based selection
    # O(n) in best case, O(n^2) in worst case
    def main_quick(self, lst, k):
        def _partition(low, high):
            flag = low
            for i in range(low + 1, high):
                if lst[i] < lst[low]:
                    flag += 1
                    lst[i], lst[flag] = lst[flag], lst[i]
            lst[low], lst[flag] = lst[flag], lst[low]
            return flag

        low = 0
        high = len(lst)
        while low < high:
            flag = _partition(low, high)
            if flag > k:
                high = flag
            elif flag < k:
                low = flag + 1
            else:
                break
        assert (flag == k)
        return lst[flag]

    # @solution: minimum-heap-based selection
    def main_min_heap(self, lst, k):
        def _sink(low, high):
            it = low << 1 | 1
            while it < high:
                if it + 1 < high and lst[it + 1] < lst[it]:
                    it += 1
                if lst[low] <= lst[it]:
                    break
                lst[low], lst[it] = lst[it], lst[low]
                low = it
                it = low << 1 | 1

        for i in range((len(lst) - 1) >> 1, -1, -1):
            _sink(i, len(lst))
        for i in range(k):
            high = len(lst) - 1 - i
            lst[0], lst[high] = lst[high], lst[0]
            _sink(0, high)
        return lst[0]

    # @solution: maximum-heap-based selection
    def main_max_heap(self, lst, k):
        def _sink(low, high):
            it = low << 1 | 1
            while it < high:
                if it + 1 < high and lst[it + 1] > lst[it]:
                    it += 1
                if lst[low] >= lst[it]:
                    break
                lst[low], lst[it] = lst[it], lst[low]
                low = it
                it = low << 1 | 1

        for i in range(k >> 1, -1, -1):
            _sink(i, k + 1)
        for i in range(k + 1, len(lst)):
            if lst[i] < lst[0]:
                lst[0], lst[i] = lst[i], lst[0]
                _sink(0, k + 1)
        return lst[0]

    def main_best(self, lst, k):
        pass

    def testcase(self):
        def test(func):
            for i in range(20):
                lst = [i for i in range(random.randint(5, 50))]
                for i in range(len(lst)):
                    random.shuffle(lst)
                    assert (func(lst[:], i) == i)
            print 'pass:', func

        map(test, [self.main_bubble, self.main_quick,
                   self.main_min_heap, self.main_max_heap])


if __name__ == "__main__":
    Select().testcase()
    print 'done'
