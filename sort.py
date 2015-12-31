# -*- coding: utf-8 -*-
# problem: sorting (into increasing order)
# solution: insertion sort, shellsort, selection sort, bubble sort,
#           quicksort, merge sort, heapsort
# 采用递归和迭代两种形式实现算法
# 其中递归偏向于表现算法的核心思想，因而忽略空间复杂度、性能等方面
# 对于quicksort和mergesort这两种算法，递归实现则是为最常见且简单的方式

def insertion():
    def iter(lst):
        # at the beginning of each outer loop, i will be reset to the value next to the former i
        for i in range(1, len(lst)):
            t = lst[i]
            # so in the inner loop, i can be reused
            i -= 1
            while i >= 0 and lst[i] > t:
                lst[i + 1] = lst[i]
                i -= 1
            assert (i == -1 or lst[i] <= t)
            lst[i + 1] = t
        return lst

    def iter2(lst):
        # python中的for更接近于迭代器，而非C/C++中那样传统的循环结构
        # 因此无法给for增加额外的条件判断
        for i in range(1, len(lst)):
            t = lst[i]
            flag = True
            # 由于需要区分循环的终止是由for条件失败还是break所导致的
            # 因此需借助于额外的变量（即flag），与其这样还不如使用传统的循环结构while
            for i in range(i - 1, -1, -1):  # reuse i
                if lst[i] > t:
                    lst[i + 1] = lst[i]
                else:
                    lst[i + 1] = t
                    flag = False
                    break
            if flag:
                lst[0] = t
        return lst

    def recur(lst):
        def _insert(lst):
            if len(lst) < 2 or lst[-2] <= lst[-1]:
                return lst
            lst[-1], lst[-2] = lst[-2], lst[-1]
            lst[:-1] = _insert(lst[:-1])
            return lst

        if len(lst) < 2:
            return lst
        lst[:-1] = recur(lst[:-1])  # outer loop
        return _insert(lst)  # inner loop

    print '==========================================='
    print 'insertion'
    print iter(gList[:])
    print iter2(gList[:])
    print recur(gList[:])
    print '==========================================='


def shell():
    pass


def selection():
    def iter(lst):
        for i in range(0, len(lst)):
            m = i  # minimum
            for j in range(i + 1, len(lst)):
                if lst[j] < lst[m]:
                    m = j
            lst[i], lst[m] = lst[m], lst[i]
        return lst

    def iter2(lst):
        for i in range(len(lst) - 1, 0, -1):
            m = i  # maximum
            for j in range(i - 1, -1, -1):
                if lst[j] > lst[m]:
                    m = j
            lst[i], lst[m] = lst[m], lst[i]
        return lst

    def recur(lst):
        # select and store the minimum at lst[0]
        def _select(lst):
            if len(lst) < 2:
                return lst
            lst[1:] = _select(lst[1:])
            if lst[0] <= lst[1]:
                return lst
            else:
                return [lst[1], lst[0]] + lst[2:]

        if len(lst) < 2:
            return lst
        lst = _select(lst)  # inner loop
        return [lst[0]] + recur(lst[1:])  # outer loop

    print '==========================================='
    print 'selection'
    print iter(gList[:])
    print iter2(gList[:])
    print recur(gList[:])
    print '==========================================='


def bubble():
    def iter(lst):
        for i in range(len(lst) - 1, 0, -1):
            for j in range(0, i):
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
        return lst

    def recur(lst):
        # bubble up and store the maximum at arr[-1]
        def _bubble(lst):
            if len(lst) < 2:
                return lst
            if lst[0] > lst[1]:
                lst[0], lst[1] = lst[1], lst[0]
            return [lst[0]] + _bubble(lst[1:])

        if len(lst) < 2:
            return lst
        lst = _bubble(lst)  # inner loop
        return recur(lst[:-1]) + [lst[-1]]  # outer loop

    print '==========================================='
    print 'bubble'
    print iter(gList[:])
    print recur(gList[:])
    print '==========================================='


def quick():
    def recur(lst):
        # 始终以lst[0]为分割数
        def _partition(lst):
            flag = 0  # 指向小于lst[0]且索引值最大的slot
            for i in range(1, len(lst)):
                if lst[i] < lst[0]:
                    flag += 1
                    lst[i], lst[flag] = lst[flag], lst[i]
            lst[0], lst[flag] = lst[flag], lst[0]
            return flag  # in-place partition, so returns flag only

        if len(lst) < 2:
            return lst
        flag = _partition(lst)
        return recur(lst[:flag]) + [lst[flag]] + recur(lst[flag + 1:])

    print '==========================================='
    print 'quick'
    print recur(gList[:])
    print '==========================================='


def merge():
    # top-down mergesort
    def recur(lst):
        # 若不使用递归实现_merge()，简单的方式是使用一个额外的辅助数组来存储合并后的结果
        def _merge(lst1, lst2):
            if len(lst1) == 0:
                return lst2
            elif len(lst2) == 0:
                return lst1
            if lst1[0] <= lst2[0]:
                return [lst1[0]] + _merge(lst1[1:], lst2)
            else:
                return [lst2[0]] + _merge(lst1, lst2[1:])

        if len(lst) < 2:
            return lst
        mid = int(len(lst) / 2)
        return _merge(recur(lst[:mid]), recur(lst[mid:]))

    # bottom-up mergesort
    # in-place sort
    def iter(lst):
        def _merge(lst1, lst2):
            tlst = []  # auxliary space
            i, j = 0, 0
            while i < len(lst1) and j < len(lst2):
                if lst1[i] <= lst2[j]:
                    tlst.append(lst1[i])
                    i += 1
                else:
                    tlst.append(lst2[j])
                    j += 1
            if i == len(lst1):
                return tlst + lst2[j:]
            else:
                return tlst + lst1[i:]

        step = 1
        while step < len(lst):
            i = 0
            while i < len(lst):
                if i + step >= len(lst):
                    # 下次loop时，由于i变为现在的2倍
                    # 因此这些尾部剩余仍会作为独立的区间！
                    break
                elif i + step + step >= len(lst):
                    lst[i:] = _merge(lst[i:i + step], lst[i + step:])
                    break
                else:  # 以上处理边界情况
                    lst[i:i + step + step] = _merge(lst[i:i + step], lst[i + step:i + step + step])
                    i += step + step
            step *= 2
        return lst

    print '==========================================='
    print 'merge'
    print recur(gList[:])
    print iter(gList[:])
    print '==========================================='


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

if __name__ == '__main__':
    insertion()
    selection()
    bubble()
    quick()
    merge()
    heap()
    print 'done'
