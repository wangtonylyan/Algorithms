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


if __name__ == '__main__':
    SelectionSort().testcase()
    BubbleSort().testcase()
    print 'done'


def heap():
    # 实现中只利用了sink()这一基本操作，且是原地排序
    def iter(lst):
        def _sink(lst, i, l):  # == heap.MaxHeap._sink()
            while i * 2 < l:
                j = i * 2
                if j + 1 < l and lst[j + 1] > lst[j]:
                    j += 1
                if lst[i] >= lst[j]:
                    break
                lst[i], lst[j] = lst[j], lst[i]
                i = j
            return lst

        # 1)make heap：从下至上地利用sink()建堆，此方式比从上至下地利用float()更效率
        lst = [0] + lst
        for i in range((len(lst) - 1) / 2, 0, -1):
            lst = _sink(lst, i, len(lst))
        # 2)heapsort：不断地执行heap.pop()操作并保留其结果，就可以得到整个递增数列
        for i in range(len(lst) - 1, 1, -1):
            lst[1], lst[i] = lst[i], lst[1]  # 相当于heap.pop()操作
            lst = _sink(lst, 1, i)
        return lst[1:]

    print '==========================================='
    print 'heap'
    print iter(gList[:])
    print '==========================================='


gList = [6, 5, 7, 4, 8, 3, 9, 2]
# gList = [8, 7, 6, 5, 4, 4, 3, 3, 2, 2, 1]
