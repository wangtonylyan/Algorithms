# -*- coding: utf-8 -*-
# data structure: binary heap
# 1) 完全二叉树存储于数组中，父与子节点之间的数值关系
# 0-based indexing：left=root*2+1, right=root*2+2, root=(child-1)/2
# 1-based indexing：left=root*2, right=root*2+1, root=child/2
# 2) 堆的所有逻辑都是基于两个核心的操作：float()和sink()
# 最大/最小堆在实现上的区别也仅在于此

from base.number import NumberTest


class BinaryHeap(object):
    def __init__(self, lst, key, cmp):
        assert (isinstance(lst, list) and len(lst) >= 0)
        super(BinaryHeap, self).__init__()
        self.hp = lst[:]
        self.key = key
        self.cmp = cmp
        self._build()

    def __len__(self):
        return len(self.hp)

    def _float(self, iter, root):
        t = (iter - 1) >> 1
        while t >= root:
            if self.cmp(self.key(self.hp[t]), self.key(self.hp[iter])):
                break
            self.hp[iter], self.hp[t] = self.hp[t], self.hp[iter]
            iter = t
            t = (iter - 1) >> 1

    def _sink(self, iter, leaf):
        t = iter << 1 | 1
        while t < leaf:
            if t + 1 < leaf and self.cmp(self.key(self.hp[t + 1]), self.key(self.hp[t])):
                t += 1
            if self.cmp(self.key(self.hp[iter]), self.key(self.hp[t])):
                break
            self.hp[iter], self.hp[t] = self.hp[t], self.hp[iter]
            iter = t
            t = iter << 1 | 1

    # 根据heapq标准库中对于_siftup()的描述，可以如下方式优化sink的实现
    # 将目标节点视为"镂空"并用其子节点来填补，去除循环体中用于判断能否快速终止的比较操作
    # 循环直至条件失败(即访问到叶子节点)而终止，最后利用float来精确地定位目标节点的位置
    # 此优化基于的假设：在实践中新替换的数往往距离leaf更近(离root更远)
    def _sink_opt(self, iter, leaf):
        r, v = iter, self.hp[iter]
        t = iter << 1 | 1
        while t < leaf:
            if t + 1 < leaf and self.cmp(self.key(self.hp[t + 1]), self.key(self.hp[t])):
                t += 1
            self.hp[iter] = self.hp[t]  # just copy, no swap
            iter = t
            t = iter << 1 | 1
        self.hp[iter] = v
        self._float(iter, r)  # 限定float的根节点对于建堆过程而言是必要的

    def _build(self):
        # 利用float()或sink()就可以在数组中原地建堆
        # 由于两个基本操作的实现是快速终止的，即while循环中的break
        # 这将影响到建堆时的遍历方式：前者效率更高
        # (a) sink从下至上或float从上至下，一次，相当于插入排序
        # (b) sink从上至下或float从下至上，多次，相当于冒泡排序
        # 其实，建堆过程本身就是一种排序

        # a.1) 将节点i的值插入至其子节点的两棵子堆中
        for i in range((len(self.hp) >> 1) - 1, -1, -1):
            self._sink(i, len(self.hp))

        # a.2) 将节点i的值插入至其索引之前所有节点所构成的整棵堆中
        for i in range(1, len(self.hp)):
            self._float(i, 0)

    def push(self, value):
        self.hp.append(value)
        self._float(len(self.hp) - 1, 0)

    def pop(self):
        if len(self.hp) == 0:
            return None
        self.hp[0], self.hp[-1] = self.hp[-1], self.hp[0]
        ret = self.hp.pop()
        if len(self.hp) > 1:
            self._sink(0, len(self.hp))
        return ret

    def replace(self, old, new):
        for i in range(len(self.hp)):
            if self.key(self.hp[i]) == self.key(old):
                self.hp[i] = new
                if self.cmp(self.key(old), self.key(new)):
                    self._sink(i, len(self.hp))
                else:
                    self._float(i, 0)
                return True
        return False

    def check(self):
        assert (isinstance(self.hp, list))
        for i in range(len(self.hp) >> 1):
            if i << 1 | 1 < len(self.hp):
                assert (self.cmp(self.key(self.hp[i]), self.key(self.hp[i << 1 | 1])))
            if (i + 1) << 1 < len(self.hp):
                assert (self.cmp(self.key(self.hp[i]), self.key(self.hp[(i + 1) << 1])))


class MaxBinaryHeap(BinaryHeap):
    def __init__(self, lst=[], key=lambda x: x):
        super(MaxBinaryHeap, self).__init__(lst, key, cmp=lambda x, y: x >= y)
        assert (len(self.hp) == len(lst))

    @classmethod
    def heapsort(cls, lst):
        # 由于堆排必须利用sink操作维护堆的性质
        # 因此为简化实现也推荐使用sink方式建堆
        hp = cls(lst)
        for i in range((len(lst) >> 1) - 1, -1, -1):
            hp._sink_opt(i, len(lst))
        for i in range(len(lst) - 1, 0, -1):
            hp.hp[0], hp.hp[i] = hp.hp[i], hp.hp[0]
            hp._sink_opt(0, i)
        return hp.hp


class MinBinaryHeap(BinaryHeap):
    def __init__(self, lst=[], key=lambda x: x):
        super(MinBinaryHeap, self).__init__(lst, key, cmp=lambda x, y: x <= y)
        assert (len(self.hp) == len(lst))


class BinaryHeapTest(NumberTest):
    def __init__(self, cls):
        assert (issubclass(cls, BinaryHeap))
        super(BinaryHeapTest, self).__init__()
        self.cls = cls

    def testcase(self):
        def test(cases):
            for case in cases:
                hp = self.cls(case)
                hp.check()
                assert (len(hp) == len(case))
                for i in case:
                    hp.replace(i, i + 1)
                    hp.check()
                assert (len(hp) == len(case))
                for i in range(len(case)):
                    hp.pop()
                    hp.check()
                assert (len(hp) == 0)

        map(test, self._gencase(maxLen=100, each=1, total=200))
        print 'pass:', self.cls


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
        tmp = lst[:k]  # auxiliary space
        for i in range((k - 1) >> 1, -1, -1):
            tmp = _sink(tmp, i, k)
        # sort by heap
        for i in range(0, len(lst)):
            lst[i] = tmp[0]  # heap.pop
            if i + k < len(lst):
                tmp[0] = lst[i + k]  # heap.push
                tmp = _sink(tmp, 0, k)
            else:
                tmp[0] = tmp[len(tmp) - 1]  # heap.push
                tmp.pop()
                tmp = _sink(tmp, 0, len(tmp))
        return lst

    def testcase(self):
        lst = [2, 6, 3, 12, 56, 8]
        ret = self.main(lst[:], 3)
        lst.sort()
        assert (ret == lst)
        print 'pass:', self.__class__


if __name__ == "__main__":
    BinaryHeapTest(MaxBinaryHeap).testcase()
    BinaryHeapTest(MinBinaryHeap).testcase()

    SortANearlySortedArray().testcase()
    print 'done'
