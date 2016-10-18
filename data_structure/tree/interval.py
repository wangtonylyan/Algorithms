# -*- coding: utf-8 -*-
# data structure: interval tree
# 1) Interval tree is used to represent a dynamic set of intervals.
# @reference: <Introduction to Algorithm> Augmenting Data Structures
# 2) 多应用于区域查询类的问题，例如
# 找到一个区间集合中与某个指定区间相重叠的所有区间
# to find all roads on a computerized map inside a rectangular viewport
# to find all visible elements inside a three-dimensional scene
# 3) 区间树的实现不仅限于增强的平衡二叉搜索树，还可使用多叉树


from binary.rbt import RedBlackTree
from base.interval import Interval, IntervalTest
from base.tree import TreeTest


# abstract class
class IntervalTree(object):
    def __init__(self):
        super(IntervalTree, self).__init__()


class IntervalTreeAugmented(RedBlackTree, IntervalTree):
    class Node(RedBlackTree.Node):
        # a whole interval as the value, whose low endpoint as the key
        # 目前实现的缺陷是不支持存在多个low endpoint相同的区间
        def __init__(self, key, value):
            assert (isinstance(value, Interval))
            super(IntervalTreeAugmented.Node, self).__init__(key, value)
            self.max = value.high  # maximum of high endpoints of subtrees

    def __init__(self):
        super(IntervalTreeAugmented, self).__init__(cmp)

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
        if ivt:
            assert (ivt.max == max(ivt.value.high,
                                   ivt.left.max if ivt.left else None,
                                   ivt.right.max if ivt.right else None))
        return super(IntervalTreeAugmented, self)._check(ivt, left, right)


class IntervalTreeTest(TreeTest, IntervalTest):
    def __init__(self, cls, args={}, num=500):
        assert (issubclass(cls, IntervalTree) and isinstance(args, dict) and num > 0)
        super(IntervalTreeTest, self).__init__(cls, args, 0, True, False)
        self.cases = self._gencase(maxLen=100, each=1, total=num)
        print '=' * 50
        print "sample size:\t", len(self.cases)

    def search(self):
        def test(cases):
            for case in cases:
                tree = self.cls(**self.args)
                for low, high in case:
                    tree.insert(low, high)
                    if self.check:
                        tree.check()
                    assert (all(Interval(low, high).overlap(Interval(x, y)) for x, y in tree.search(low, high)))
                assert (len(tree) <= len(case))

        map(test, self.cases)

    def _testcase(self):
        self.search()


if __name__ == '__main__':
    IntervalTreeTest(IntervalTreeAugmented).testcase()
    print 'done'
