# -*- coding: utf-8 -*-
# data structure: segment tree
# 1) 线段树的构建是基于一个连续区间的
# 其叶子节点的数量等于该区间的长度，中间节点所表示的区间的选取通常都是基于二分法的
# 这样就保证了整棵树的高度与区间的长度之间的对数级关系
# 2) 线段树是一种静态的数据结构
# 因此每次查询所遍历的路径几乎是相同的，这样就延伸出了许多设计
# 如在每个节点中都维护一些额外的统计信息，以便于指导或加速后续的搜索流程
# 这也充分展现了其作为查找树的初衷，而非只关乎如何调整自身的结构
# 3) 查询操作的实现分为以下两种情况：
# 当查询信息只存储于叶子节点中时，遍历整个需求区间所覆盖到的所有叶子节点
# 当查询信息已存储于中间节点中时，访问至所有包含于需求区间的子区间即可
# 4) reference
# http://blog.csdn.net/metalseed/article/details/8039326
# e.g. HDU_1166,HDU_1394,HDU_1754,HDU_2795


from base.tree import Tree, TreeTest
from base.number import Number, NumberTest
from base.interval import Interval
import math


class SegmentTree(Tree, Number):
    # @param: list 'lst' stores values of leaves
    # @param: function 'up' assembles the values of each piece of the whole interval during bottom-up
    # it shall be compatible with the 'None' parameter
    # 即用于维护中间节点的统计信息
    def __init__(self, lst, up=lambda x, y: None):
        assert (len(lst) > 0 and callable(up))
        super(SegmentTree, self).__init__()
        self.root = None
        self.up = up
        self._build(lst)

    def __len__(self):
        return sum([1 for _ in self.root if _])

    def _build(self, lst):
        def recur(sgt, low, high):
            if high - low < 1:
                return None
            assert (sgt < len(self.root))
            if high - low == 1:
                self.root[sgt] = self.__class__.Node(Interval(low, high), lst[low])
            else:
                mid = low + (high - low + 1) / 2
                self.root[sgt] = self.__class__.Node(Interval(low, high),
                                                     self.up(recur(sgt << 1 | 1, low, mid),
                                                             recur((sgt + 1) << 1, mid, high)))
            return self.root[sgt].value

        assert (not self.root)
        self.root = [None] * (2 ** int(math.ceil(math.log(len(lst), 2)) + 1))
        recur(0, 0, len(lst))

    def search(self, low, high, up=None):
        def recur(sgt, key):
            if sgt >= len(self.root) or not self.root[sgt]:
                return None
            if callable(up):
                if key.overlap(self.root[sgt].key):  # traverse till leaves
                    if len(self.root[sgt].key) == 1:
                        assert (sgt << 1 | 1 >= len(self.root) or not self.root[sgt << 1 | 1])
                        assert ((sgt + 1) << 1 >= len(self.root) or not self.root[(sgt + 1) << 1])
                        return self.root[sgt].value
                    else:
                        return up(recur(sgt << 1 | 1, key), recur((sgt + 1) << 1, key))
                else:
                    return None
            else:
                if key.contain(self.root[sgt].key):
                    return self.root[sgt].value
                elif key.overlap(self.root[sgt].key):
                    return self.up(recur(sgt << 1 | 1, key), recur((sgt + 1) << 1, key))
                else:
                    return None

        assert (low < high)
        return recur(0, Interval(low, high))

    # lazy propagation
    # 在不依赖于队列的实现方式下，延迟更新只适用于前后多次更新的效果是可以被累积的
    # 且中间节点所维护的信息足以表达上述的累积效果，例如对某个区间内的数值同时加减
    # 当中间节点维护的是其区间内所有数值的总和时，累积效果可以被表示为子节点个数乘以每次更新操作所要求的加减值
    def update(self, low, high, up=lambda x: x):
        def recur(sgt, key):
            if sgt >= len(self.root) or not self.root[sgt]:
                return None
            if key.overlap(self.root[sgt].key):  # traverse till leaves
                if len(self.root[sgt].key) == 1:
                    assert (sgt << 1 | 1 >= len(self.root) or not self.root[sgt << 1 | 1])
                    assert ((sgt + 1) << 1 >= len(self.root) or not self.root[(sgt + 1) << 1])
                    self.root[sgt].value = up(self.root[sgt].value)
                else:
                    self.root[sgt].value = self.up(recur(sgt << 1 | 1, key), recur((sgt + 1) << 1, key))
                return self.root[sgt].value
            else:
                return None

        assert (low < high and callable(up))
        return recur(0, Interval(low, high))


class SegmentTreeTest(TreeTest, NumberTest):
    def __init__(self, num):
        assert (num > 0)
        super(SegmentTreeTest, self).__init__(SegmentTree, 0, True, True)
        self.cases = self._gencase(each=1, total=num)
        print '=' * 50
        print "sample size:\t", len(self.cases)

    def testcase(self):
        # RMQ
        def test(cases):
            def get(x, y, m):
                if x is not None and y is not None:
                    return m(x, y)
                elif x is not None:
                    return x
                elif y is not None:
                    return y
                return None

            def update(x):
                return x + 1

            for case in cases:
                t1 = self.tcls(case, up=lambda x, y: get(x, y, min))
                t2 = self.tcls(case, up=lambda x, y: get(x, y, max))
                for i in range(len(case)):
                    for j in range(i + 1, len(case) + 1):
                        assert (t1.search(i, j) == t2.search(i, j, up=lambda x, y: get(x, y, min)))

                t1.update(0, len(case), up=update)
                t3 = self.tcls(map(update, case), up=lambda x, y: get(x, y, min))
                assert (t1.search(0, len(case)) == t3.search(0, len(case)))

        map(test, self.cases)
        print 'pass:', self.__class__


if __name__ == '__main__':
    SegmentTreeTest(500).testcase()
    print 'done'
