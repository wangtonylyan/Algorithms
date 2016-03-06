# -*- coding: utf-8 -*-
# data structure: max-heap

import random


# 1）完全二叉树存储于数组中，父与子节点之间的数值关系
# 若以0为树根索引：left=root*2+1, right=root*2+2, root=(child-1)/2
# 若以1为树根索引：left=root*2, right=root*2+1, root=child/2
# 2）最大/最小堆都基于两个核心的基本操作来维护：float()和sink()
# 因此要在最大/最小堆的基础上实现最小/最大堆只需修改上述两个函数即可
# 3）虽然最大/小堆都能实现堆排，但最有效率的还是最大堆？
class MaxHeap:
    def __init__(self, lst=[]):
        assert (isinstance(lst, list))
        self.lst = self._build(lst[:])

    @staticmethod
    def _sink(lst, hp, leaf):
        t = hp << 1 | 1
        while t < leaf:
            if t + 1 < leaf and lst[t] < lst[t + 1]:
                t += 1
            if lst[hp] >= lst[t]:
                break
            lst[hp], lst[t] = lst[t], lst[hp]
            hp = t
            t = hp << 1 | 1
        return lst

    @staticmethod
    def _float(lst, hp, root):
        t = (hp - 1) >> 1
        while t >= root:
            if lst[hp] <= lst[t]:
                break
            lst[hp], lst[t] = lst[t], lst[hp]
            hp = t
            t = (hp - 1) >> 1
        return lst

    @staticmethod
    def _check(lst):
        for i in range(0, len(lst)):
            assert (i << 1 | 1 >= len(lst) or lst[i] >= lst[i << 1 | 1])
            assert ((i + 1) << 1 >= len(lst) or lst[i] >= lst[(i + 1) << 1])

    @classmethod
    def _build(cls, lst):
        # 利用heap的两个基本操作可以在数组中原地建堆
        # 由于两个基本操作的实现是快速终止的，即while循环中的break
        # 这将影响到建堆时的遍历方式：前者效率更高
        # (a) sink从下至上或float从上至下，一次，相当于插入排序
        # (b) sink从上至下或float从下至上，多次，相当于冒泡排序
        # 其实，建堆过程本身就是一种排序
        def _by_sink(lst):
            # 将节点i的值插入至其子节点的两棵子堆中
            for i in range((len(lst) - 1) >> 1, -1, -1):
                lst = cls._sink(lst, i, len(lst))

        def _by_float(lst):
            # 将节点i的值插入至其索引之前所有节点所构成的整棵堆中
            for i in range(1, len(lst)):
                lst = cls._float(lst, i, 0)

        # 1)
        _by_sink(lst)
        cls._check(lst)
        # 2)
        _by_float(lst)
        cls._check(lst)
        return lst

    def push(self, value):
        self.lst.append(value)
        self.lst = self._float(self.lst, len(self.lst) - 1, 0)
        self._check(self.lst)

    def pop(self):
        ret = None
        if len(self.lst) > 0:
            ret = self.lst[0]
            self.lst[0] = self.lst[len(self.lst) - 1]
            self.lst.pop()
            self.lst = self._sink(self.lst, 0, len(self.lst))
        self._check(self.lst)
        return ret

    def size(self):
        return len(self.lst)

    @classmethod
    def heapsort(cls, lst):
        # 由于只能利用sink操作维护堆的性质
        # 因此推荐同样也使用sink方式建堆
        for i in range((len(lst) - 1) >> 1, -1, -1):
            lst = cls._sink(lst, i, len(lst))
        for i in range(len(lst) - 1, 0, -1):
            lst[0], lst[i] = lst[i], lst[0]
            lst = cls._sink(lst, 0, i)
        return lst


# @problem:
# Given an array of size n, where every element is at most k away from its target position,
# sorts the array in O(nLogk) time.
class SortANearlySortedArray():
    def main(self, lst, k):
        # minimum heap
        def _sink(lst, hp, leaf):
            t = hp << 1 | 1
            while t < leaf:
                if t + 1 < leaf and lst[t + 1] < lst[t]:
                    t += 1
                if lst[hp] < lst[t]:
                    break
                lst[hp], lst[t] = lst[t], lst[hp]
                hp = t
                t = hp << 1 | 1
            return lst

        # build heap
        alst = lst[:k]  # auxiliary space
        for i in range((k - 1) >> 1, -1, -1):
            alst = _sink(alst, i, k)
        # sort by heap
        for i in range(0, len(lst)):
            lst[i] = alst[0]  # heap.pop
            if i + k < len(lst):
                alst[0] = lst[i + k]  # heap.push
                alst = _sink(alst, 0, k)
            else:
                alst[0] = alst[len(alst) - 1]  # heap.push
                alst.pop()
                alst = _sink(alst, 0, len(alst))
        return lst

    def testcase(self):
        lst = [2, 6, 3, 12, 56, 8]
        ret = self.main(lst[:], 3)
        lst.sort()
        assert (ret == lst)
        print 'pass:', self.__class__


if __name__ == "__main__":
    for num in range(0, 10):
        lst = [i for i in range(num)]

        random.shuffle(lst)
        hp = MaxHeap(lst)
        for i in range(num):
            hp.pop()
        assert (hp.size() == 0)

        random.shuffle(lst)
        for v in lst:
            hp.push(v)
        assert (hp.size() == num)
        for i in range(num):
            hp.pop()
        assert (hp.size() == 0)

    SortANearlySortedArray().testcase()
    print 'done'
