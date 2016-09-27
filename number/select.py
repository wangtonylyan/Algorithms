# -*- coding: utf-8 -*-
# problem: find the k-th smallest element in a collection
# solution: sort-based selection

from base.number import NumberTest


class Select(NumberTest):
    def __init__(self):
        super(Select, self).__init__()
        self.funcs = [
            self.main_bubble, self.main_quick,
            self.main_min_heap, self.main_max_heap,
            # self.main_best,
        ]

    # @algorithm: bubble-based
    def main_bubble(self, lst, k):
        for i in range(k + 1):
            for j in range(len(lst) - 1, i, -1):
                if lst[j] < lst[j - 1]:
                    lst[j], lst[j - 1] = lst[j - 1], lst[j]
        return lst[k]

    # @algorithm: quick-based
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

    # @algorithm: minimum-heap-based
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

    # @algorithm: maximum-heap-based
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
        def test(case):
            cpy = case[:]
            cpy.sort()
            for i in range(len(case)):
                ret = cpy[i]
                assert (all(x == ret for x in map(lambda f: f(case[:], i), self.funcs)))

        self._testcase(test, self._gencase(each=1, total=500))


if __name__ == "__main__":
    Select().testcase()
    print 'done'
