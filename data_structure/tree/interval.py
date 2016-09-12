# -*- coding: utf-8 -*-
# data structure: interval tree
# Interval tree is used to represent a dynamic set of intervals.

from data_structure.tree.binary import bst, rbt


# interval is represented as pair (tuple datatype)
# interval trichotomy for two intervals i and j
# that hold exactly one of the following three properties:
# (a) i and j overlap
# (b) i is to the left of j, i.e. i.high < j.low
# (c) i is to the right of j, i.e. j.high < i.low
def ifIntervalsOverlapped((low1, high1), (low2, high2)):
    assert (low1 <= high1 and low2 <= high2)
    return (high1 >= low2 and high2 >= low1)
    return (max(high1, high2) - min(low1, low2) <= high1 - low1 + high2 - low2)  # closed interval


# 区间树的实现不仅限于增强平衡二叉树，还可以用多叉树来实现
# implementing by argumenting red-black tree
class IntervalTree(rbt.RedBlackTree):
    class Node(rbt.RedBlackTree.Node):
        def __init__(self, key, value):
            assert (key and isinstance(key, int))
            assert (value and isinstance(value, tuple))
            assert (key == value[0] and value[0] <= value[1])
            super(IntervalTree.Node, self).__init__(key, value)
            # maximum of self subtree
            self.max = value[1]  # high endpoint as default

    def __init__(self):
        super(IntervalTree, self).__init__()

    # maintain additional information，可以在遍历的同时执行
    # 此处单独维护只是为了便于调用父类红黑树的接口
    # 从而体现当前增强红黑树的实现方案
    # 删除等操作也完全类似，实现略
    def _maintain(self):
        def _recur(ivt):
            if not ivt:
                return 0
            ivt.max = max(_recur(ivt.left), _recur(ivt.right), ivt.value[1])
            return ivt.max

        _recur(self.root)

    def insert(self, (low, high)):  # endpoints of interval as parameters
        assert (low <= high)
        # low endpoint of interval as key, whole interval as value
        super(IntervalTree, self).insert(low, (low, high))
        self._maintain()

    # find all nodes overlap with (low,high) interval
    def search(self, (low, high)):
        def _recur(ivt):
            lst = []
            if ivt:
                if ifIntervalsOverlapped(ivt.value, (low, high)):
                    lst.append(ivt.value)
                if ivt.left and ivt.left.max >= low:  # 检查遍历子树的必要性
                    lst += _recur(ivt.left)
                if ivt.right and ifIntervalsOverlapped((ivt.key, ivt.right.max), (low, high)):
                    lst += _recur(ivt.right)
            return lst

        return _recur(self.root)

    def _check(self, ivt, left, right):
        ret = super(IntervalTree, self)._check(ivt, left, right)
        assert (ivt.max == max(ivt.left.max if ivt.left else 0,
                               ivt.right.max if ivt.right else 0,
                               ivt.value[1]))
        return ret


import random, time


class IntervalTreeTest(bst.BinarySearchTreeTest):
    def __init__(self, clsobj, num, check=False, time=True):
        assert (issubclass(clsobj, IntervalTree))
        super(IntervalTreeTest, self).__init__(clsobj, num, check, time)
        self.dic = {}
        for i in range(num):
            r = random.randint(0, 100000)
            s = random.randint(0, 100000)
            self.dic[r] = r + s
        print "dic's size again: ", len(self.dic)

    def new(self):
        self.tree = self.tcls()
        c = 0
        if self.time:
            self.start_t = time.time()
        for i, j in self.dic.viewitems():
            self.tree.insert((i, j))
            if self.check:
                self.tree.check()
            lst = self.tree.search((i, j))
            assert (reduce(lambda x, y: x and ifIntervalsOverlapped(y, (i, j)), lst, True))
            assert (reduce(lambda x, y: x or y == (i, j), lst, False))
            c += 1
            assert (self.tree.size() == c)
        if self.time:
            self.end_t = time.time()
            print 'new:\t\t', self.end_t - self.start_t
        assert (self.tree.size() == len(self.dic))


if __name__ == '__main__':
    test = IntervalTreeTest(IntervalTree, 100, True)
    test.new()
