# -*- coding: utf-8 -*-
# data structure: interval tree
# 1) Interval tree is used to represent a dynamic set of intervals.
# @reference: <Introduction to Algorithm> Augmenting Data Structures
# 2) 多应用于区域查询类的问题，例如
# 找到一个区间集合中与某个指定区间相重叠的所有区间
# to find all roads on a computerized map inside a rectangular viewport
# to find all visible elements inside a three-dimensional scene
# 3) 区间树的实现不仅限于增强的平衡二叉搜索树，还可基于多叉树


from data_structure.tree.binary.rbt import RedBlackTree
from base.number import Number, NumberTest
from base.interval import Interval
from base.tree import TreeTest


class IntervalTreeAugmented(RedBlackTree, Number):
    class Node(RedBlackTree.Node):
        # a whole interval as the value, whose low endpoint as the key
        def __init__(self, key, value):
            assert (isinstance(value, Interval))
            super(IntervalTreeAugmented.Node, self).__init__(key, value)
            self.max = value.high  # maximum of high endpoints of subtrees

    def __init__(self):
        super(IntervalTreeAugmented, self).__init__()

    # 增强型树结构中对于additional information的维护应随着树的遍历而同步进行
    # 但由于现有实现普遍都不支持augment，因此暂仅以以下实现方式为例
    def _maintain(self, ivt):
        if not ivt:
            return None
        # 'max' is compatible with None
        ivt.max = max(ivt.value.high, self._maintain(ivt.left), self._maintain(ivt.right))
        assert (ivt.max is not None)
        return ivt.max

    def insert(self, low, high):
        assert (low <= high)
        super(IntervalTreeAugmented, self).insert(low, Interval(low, high))
        self._maintain(self.root)

    def search(self, low, high):
        def recur(ivt, key):
            assert (ivt and key)
            ret = []
            if key.overlap(ivt.value):
                ret.append((ivt.value.low, ivt.value.high))
            if ivt.left and ivt.left.max > key.low:  # check the necessity of traversal of left subtree
                ret += recur(ivt.left, key)
            if ivt.right and ivt.key < key.high:  # check the necessity of traversal of right subtree
                ret += recur(ivt.right, key)
            return ret

        return recur(self.root, Interval(low, high)) if self.root else []

    def _check(self, ivt, left, right):
        ret = super(IntervalTreeAugmented, self)._check(ivt, left, right)
        if ivt:
            assert (ivt.max == max(ivt.value.high,
                                   ivt.left.max if ivt.left else None,
                                   ivt.right.max if ivt.right else None))
        return ret


class IntervalTreeTest(TreeTest, NumberTest):
    def __init__(self, clsobj, num):
        assert (num > 0)
        assert (issubclass(clsobj, IntervalTreeAugmented))
        super(IntervalTreeTest, self).__init__(clsobj, 0, True, False)
        self.cases = {}
        print '=' * 50
        print "sample size:\t", len(self.cases)

    def search(self):
        tree = self.tcls()
        c = 0
        for i, j in self.cases.viewitems():
            tree.insert(i, j)
            if self.check:
                tree.check()
            lst = tree.search(i, j)
            assert (all(Interval(i, j).overlap(Interval(x, y)) for x, y in lst))
            c += 1
            assert (len(tree) == c)
        assert (len(tree) == len(self.cases))

    def testcase(self):
        self.search()


if __name__ == '__main__':
    IntervalTreeTest(IntervalTreeAugmented, 1000).testcase()
    print 'done'
