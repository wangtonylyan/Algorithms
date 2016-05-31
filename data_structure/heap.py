# -*- coding: utf-8 -*-
# data structure: max-heap

import random


def maxheapcheck(func):
    def f(self, *args):
        ret = func(self, *args)
        assert (self != None or hasattr(self, 'hp'))
        hp = getattr(self, 'hp')
        for i in range(0, len(hp)):
            assert (i << 1 | 1 >= len(hp) or hp[i << 1 | 1] <= hp[i])
            assert ((i + 1) << 1 >= len(hp) or hp[(i + 1) << 1] <= hp[i])
        return ret

    return f


# 1）完全二叉树存储于数组中，父与子节点之间的数值关系
# 0-based indexing：left=root*2+1, right=root*2+2, root=(child-1)/2
# 1-based indexing：left=root*2, right=root*2+1, root=child/2
# 2）堆的所有逻辑都是基于两个核心的操作：float()和sink()
# 最大/最小堆在实现上的区别也仅在于此
class MaxHeap:
    def __init__(self, lst=[]):
        assert (isinstance(lst, list))
        self.hp = self._build(lst[:])

    @staticmethod
    def _float(hp, iter, root):
        t = (iter - 1) >> 1
        while t >= root:
            if hp[t] >= hp[iter]:
                break
            hp[iter], hp[t] = hp[t], hp[iter]
            iter = t
            t = (iter - 1) >> 1
        return hp

    @staticmethod
    def _sink(hp, iter, leaf):
        t = iter << 1 | 1
        while t < leaf:
            if t + 1 < leaf and hp[t + 1] > hp[t]:
                t += 1
            if hp[t] < hp[iter]:
                break
            hp[iter], hp[t] = hp[t], hp[iter]
            iter = t
            t = iter << 1 | 1
        return hp

    # 根据heapq标准库中对于_siftup()的描述，可以如下方式优化sink的实现
    # 将目标节点视为"镂空"并用其子节点来填补，去除循环体中用于判断能否快速终止的比较操作
    # 循环直至条件失败(即访问到叶子节点)而终止，最后利用float来精确地定位目标节点的位置
    # 此优化基于的假设：在实践中新替换的数往往距离leaf更近(离root更远)
    @staticmethod
    def _sink_2(hp, iter, leaf):
        r = iter  # 限定后续float操作的根节点对于建堆过程而言是必要的
        v = hp[iter]
        t = iter << 1 | 1
        while t < leaf:
            if t + 1 < leaf and hp[t + 1] > hp[t]:
                t += 1
            hp[iter] = hp[t]  # 只需拷贝，无需交换
            iter = t
            t = iter << 1 | 1
        hp[iter] = v
        return MaxHeap._float(hp, iter, r)

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
            return lst

        def _by_float(lst):
            # 将节点i的值插入至其索引之前所有节点所构成的整棵堆中
            for i in range(1, len(lst)):
                lst = cls._float(lst, i, 0)
            return lst

        # 1)
        hp = _by_sink(lst)
        # 2)
        hp = _by_float(lst)
        return hp

    @maxheapcheck
    def push(self, value):
        self.hp.append(value)
        self.hp = self._float(self.hp, len(self.hp) - 1, 0)

    @maxheapcheck
    def pop(self):
        ret = None
        if len(self.hp) > 0:
            ret = self.hp[0]
            self.hp[0] = self.hp[len(self.hp) - 1]
            self.hp.pop()
            if len(self.hp) > 0:
                self.hp = self._sink(self.hp, 0, len(self.hp))
        return ret

    @maxheapcheck
    def size(self):
        return len(self.hp)

    def testcase(self):
        for num in range(0, 10):
            lst = [i for i in range(num)]

            random.shuffle(lst)
            hp = self.__class__(lst)
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
        print 'pass:', self.__class__

    @classmethod
    def heapsort(cls, lst):
        # 由于堆排必须利用sink操作维护堆的性质
        # 因此为简化实现也推荐使用sink方式建堆
        for i in range((len(lst) - 1) >> 1, -1, -1):
            lst = cls._sink_2(lst, i, len(lst))
        for i in range(len(lst) - 1, 0, -1):
            lst[0], lst[i] = lst[i], lst[0]
            lst = cls._sink_2(lst, 0, i)
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
    MaxHeap().testcase()
    SortANearlySortedArray().testcase()
    print 'done'
