# -*- coding: utf-8 -*-
# problem: sorting (into increasing order)
# solution: insertion sort, shellsort, selection sort, bubble sort,
#           quicksort, merge sort, heapsort
# 采用递归和迭代两种形式实现算法
# 其中递归偏向于表现算法的核心思想，因而忽略空间复杂度、性能等方面
# 对于quicksort和mergesort这两种算法，递归实现则是为最常见且简单的方式

import random


class Sort(object):
    def __init__(self):
        self.funcs = []

    def testcase(self):
        def test(sort):
            assert (sort([1]) == [1])
            assert (sort([1, 2]) == [1, 2])
            assert (sort([2, 1]) == [1, 2])
            for i in range(20):
                num = random.randint(5, 50)
                lst = [i for i in range(num)]
                for i in range(num):
                    random.shuffle(lst)
                    ret = sort(lst[:])  # pass by reference, so need to copy
                    lst.sort()
                    assert (ret == lst)
            print 'pass:', sort

        map(test, self.funcs)


class SelectionSort(Sort):
    def __init__(self):
        super(SelectionSort, self).__init__()
        self.funcs.append(self.main_iter_min)
        self.funcs.append(self.main_iter_max)
        self.funcs.append(self.main_recur)

    def main_iter_min(self, lst):
        for i in range(0, len(lst) - 1):
            m = i  # minimum
            for j in range(i + 1, len(lst)):
                if lst[j] < lst[m]:
                    m = j
            lst[i], lst[m] = lst[m], lst[i]
        return lst

    def main_iter_max(self, lst):
        for i in range(len(lst) - 1, 0, -1):
            m = i  # maximum
            for j in range(0, i):
                if lst[j] > lst[m]:
                    m = j
            lst[i], lst[m] = lst[m], lst[i]
        return lst

    def main_recur(self, lst):
        # inner loop: select the minimum of lst[ind:] and return its index
        def _select(ind):
            if ind >= len(lst) - 1:
                return ind
            m = _select(ind + 1)
            return ind if lst[ind] <= lst[m] else m

        # outer loop: select and (tail) recursion
        if len(lst) < 2:
            return lst
        m = _select(0)
        lst[0], lst[m] = lst[m], lst[0]
        return [lst[0]] + self.main_recur(lst[1:])


class BubbleSort(Sort):
    def __init__(self):
        super(BubbleSort, self).__init__()
        self.funcs.append(self.main_iter)
        self.funcs.append(self.main_recur)

    def main_iter(self, lst):
        for i in range(len(lst) - 1, 0, -1):
            swap = False
            for j in range(0, i):
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
                    swap = True
            if not swap:
                break  # small optimization
        return lst

    def main_recur(self, lst):
        # inner loop: bubble up the maximum into lst[-1]
        def _bubble(lst):
            if len(lst) < 2:
                return lst
            if lst[0] > lst[1]:
                lst[0], lst[1] = lst[1], lst[0]
            return [lst[0]] + _bubble(lst[1:])

        # outer loop: bubble and (tail) recursion
        if len(lst) < 2:
            return lst
        lst = _bubble(lst)
        return self.main_recur(lst[:-1]) + [lst[-1]]


import data_structure.heap as heap


class HeapSort(Sort):
    def __init__(self):
        super(HeapSort, self).__init__()
        self.funcs.append(self.main)

    def main(self, lst):
        # build heap
        hp = heap.MaxHeap(lst)
        # sort heap
        lst = hp.sort()
        return lst


if __name__ == '__main__':
    SelectionSort().testcase()
    BubbleSort().testcase()
    HeapSort().testcase()
    print 'done'
