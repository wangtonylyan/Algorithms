# -*- coding: utf-8 -*-
# data structure: segment tree & interval tree
# Segment tree is, in principle, a static structure,
# i.e. its structure cannot be modified once it is built.
# Interval tree is used to represent a dynamic set of intervals.
# 这两种数据结构都是用于处理与区间有关的问题

import bst, rbt


# interval is represented as pair (tuple)
# interval trichotomy for two intervals i and j
# that hold exactly one of the following three properties:
# (a) i and j overlap
# (b) i is to the left of j, i.e. i.high < j.low
# (c) i is to the right of j, i.e. j.high < i.low
# 该三分法将两个区间之间的关系分为了三种，这也是随后实现中需要分类讨论的情形
def isIntervalsOverlapped((low1, high1), (low2, high2)):
    assert (low1 <= high1 and low2 <= high2)
    return (low1 <= low2 <= high1 or low1 <= high2 <= high1)


class SegmentTree(bst.BinarySearchTree):
    class Node:
        def __init__(self, low, high):
            self.left = None
            self.right = None
            assert (low <= high)
            self.itv = Interval(low, high)

    def __init__(self):
        self.root = None

    def build(self, itv):
        def _recur(low, high):
            assert (low <= high)
            sgt = self.__class__.Node(low, high)
            if sgt.low != sgt.high:
                mid = (sgt.low + sgt.high) / 2
                sgt.left = _recur(sgt.low, mid)
                sgt.right = _recur(mid + 1, sgt.high)
            return sgt

        self.root = _iter(itv.low, itv.high)


class IntervalTree(rbt.RedBlackTree):
    class Node(rbt.RedBlackTree.Node):
        def __init__(self, key, value):
            assert (key and value and isinstance(value, tuple))
            assert (key == value[0] and value[0] <= value[1])
            super(IntervalTree.Node, self).__init__(key, value)
            # maximum of self subtree
            self.max = value[1]  # high endpoint as default

    def __init__(self):
        super(IntervalTree, self).__init__()

    def _search(self, ivt, (low, high)):
        while ivt and not isIntervalsOverlapped(ivt.value, (low, high)):
            if ivt.left and ivt.left.max >= low:
                ivt = ivt.left
            elif ivt.right and ivt.right.max >= low:
                ivt = ivt.right
            else:
                ivt = None
        return ivt

    def insert(self, (low, high)):  # endpoints of interval as parameters
        assert (low <= high)
        key = low  # low endpoint as key
        value = (low, high)  # interval as value
        super(IntervalTree, self).insert(key, value)


import random, time


class IntervalSearchTreeTest(bst.BinarySearchTreeTest):
    def __init__(self, clsobj, num, check=False, time=True):
        super(IntervalSearchTreeTest, self).__init__(clsobj, num, check, time)
        self.dic = {}
        for i in range(num):
            r = random.randint(0, 100000)
            s = random.randint(0, 100000)
            self.dic[r] = r + s
        print "dic's size: ", len(self.dic)

    def new(self):
        self.tree = self.tcls()
        c = 0
        if self.time:
            self.start_t = time.time()
        for i, j in self.dic.viewitems():
            self.tree.insert((i, j))
            if self.check:
                self.tree.check()
            v = self.tree.search((i, j))
            if v == None:
                print v, (i, j)
            assert (self.tree.search((i, j)) and isIntervalsOverlapped(self.tree.search((i, j)), (i, j)))
            c += 1
            assert (self.tree.size() == c)
        if self.time:
            self.end_t = time.time()
            print 'new:\t\t', self.end_t - self.start_t
        assert (self.tree.size() == len(self.dic))

    def deleteMaxMin(self):
        def test(get, delete):
            c = s = self.tree.size()
            if self.time:
                self.start_t = time.time()
            for i in range(s):
                m = getattr(self.tree, get)()
                getattr(self.tree, delete)()
                if self.check:
                    self.tree.check()
                assert (self.tree.search(m.key) == None)
                c -= 1
                assert (self.tree.size() == c)
            if self.time:
                self.end_t = time.time()
                print delete + ':\t', self.end_t - self.start_t
            assert (self.tree.size() == 0)

        self.new()
        test('getMin', 'deleteMin')
        self.new()
        test('getMax', 'deleteMax')

    def delete(self):
        self.new()
        c = self.tree.size()
        if self.time:
            self.start_t = time.time()
        for i in self.dic:
            assert (self.tree.search(i))
            self.tree.delete(i)
            if self.check:
                self.tree.check()
            assert (self.tree.search(i) == None)
            c -= 1
            assert (self.tree.size() == c)
        if self.time:
            self.end_t = time.time()
            print 'delete:\t\t', self.end_t - self.start_t
        assert (self.tree.size() == 0)


if __name__ == '__main__':
    test = IntervalSearchTreeTest(IntervalTree, 100, True)
    test.new()
