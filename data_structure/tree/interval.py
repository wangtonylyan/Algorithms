# -*- coding: utf-8 -*-
# data structure: segment tree & interval tree
# Segment tree is, in principle, a static structure,
# i.e. its structure cannot be modified once it is built.
# Interval tree is used to represent a dynamic set of intervals.
# 这两种数据结构都是用于处理与区间有关的问题
# 对于输入集为互不重叠的区间，使用普通的二叉树或线段树即可
# 但当区间彼此之间大量重叠时，就往往需要更为灵活而复杂的区间树了

import bst, rbt


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


# 1）整棵线段树的构建是基于一个连续的区间
# 2）所有叶子节点的数量就是构建这棵树的区间的长度
# 3）中间节点所表示的区间通常都是通过二分法得到的
# 这样就保证了树的高度与区间的长度之间的关系是对数级
# 4）线段树本质上仍旧是一棵查找树，通过在每个节点中维护额外的信息
# 可以高效率地实现很多与区间相关的查找问题
class SegmentTree(bst.BinarySearchTree):
    class Node:
        def __init__(self, low, high):
            assert (low <= high)
            self.low = low
            self.high = high
            # 每个节点所维护的额外信息在具体问题中会不尽相同
            self.value = 0  # 此处只是举例

    def __init__(self, total=10000):
        super(SegmentTree, self).__init__()
        self.total = total + 1  # start from index 1
        # 线段树是一颗接近完全的二叉树，因此使用数组来存储整棵树
        self.root = [None for i in range(self.total)]

    def build(self, (low, high)):
        def _recur(sgt, (low, high)):
            # 在创建节点的同时初始化其value
            self.root[sgt] = self.__class__.Node(low, high)
            if self.root[sgt].low != self.root[sgt].high:
                mid = (self.root[sgt].low + self.root[sgt].high) >> 1
                _recur(sgt << 1, (low, mid))
                _recur(sgt << 1 | 1, (mid + 1, high))

        assert (low <= high)
        _recur(1, (low, high))

    def query(self, (low, high)):
        def _recur(sgt, (low, high)):
            if self.root[sgt]:
                if self.root[sgt].low == low and self.root[sgt].high == high:
                    # e.g. 更新当前节点的value
                    return self.root[sgt].value
                # 1) top-down
                pass
                # 2) recursion
                lval, rval = 0, 0
                if ifIntervalsOverlapped((low, high), (self.root[sgt << 1].low, self.root[sgt << 1].high)):
                    lval = _recur(sgt << 1, (low, high))  # travserse left subtree
                if ifIntervalsOverlapped((low, high), (self.root[sgt << 1 | 1].low, self.root[sgt << 1 | 1].high)):
                    rval = _recur(sgt << 1 | 1, (low, high))  # traverse right subtree
                # 3) bottom-up
                # e.g. 基于子节点变更后的value来更新当前节点的value
                return lval + rval

        assert (low <= high)
        _recur(1, (low, high))


if __name__ == '__main__':
    t = SegmentTree()
    t.build((1, 5))


# test = IntervalSearchTreeTest(IntervalTree, 10000, True)
#    test.new()










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

    # maintain additional information
    # 可以在维护树结构平衡的同时进行维护
    # 此处只是用来着重体现其可基于红黑树来实现的特性
    # 删除等操作也完全类似，实现略
    def _maintain(self):
        def _recur(ivt):
            if ivt == None:
                return 0
            ivt.max = max(_recur(ivt.left), _recur(ivt.right), ivt.value[1])
            return ivt.max

        _recur(self.root)

    def insert(self, (low, high)):  # endpoints of interval as parameters
        assert (low <= high)
        key = low  # low endpoint as key
        value = (low, high)  # interval as value
        super(IntervalTree, self).insert(key, value)
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
        assert (ivt.max == max(ivt.left.max if ivt.left else 0, \
                               ivt.right.max if ivt.right else 0, \
                               ivt.value[1]))
        return ret


import random, time


class IntervalSearchTreeTest(bst.BinarySearchTreeTest):
    def __init__(self, clsobj, num, check=False, time=True):
        assert (issubclass(clsobj, IntervalTree))
        super(IntervalSearchTreeTest, self).__init__(clsobj, num, check, time)
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
