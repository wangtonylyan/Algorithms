# -*- coding: utf-8 -*-
# data structure: segment tree
# 1) 线段树的构建是基于一个连续区间的
# 其叶子节点的数量就是该区间的长度
# 其中间节点所表示的区间的选取通常都是基于二分法的
# 这样就保证了整棵树的高度与区间的长度之间的对数级关系
# 2) 线段树是一种静态的数据结构
# 因此每次查询所遍历的路径几乎是相同的，这样就延伸出了许多设计
# 如在每个节点中都维护一些额外的信息，以便于指导或加速后续的搜索流程
# 这也充分展现了其作为查找树的初衷，并非只关乎如何调整自身的结构


from base.tree import Tree, TreeTest
from base.number import Number, NumberTest
from base.interval import Interval
import math


# 根据实际问题对于query返回值的不同需求
# 线段树有以下几种不同的实现和维护策略：
# 1) 返回值存储并维护于叶子节点中
# 需要从树根完整地遍历至（若干个）叶子节点
# 可以在bottom-up阶段重新维护中间节点的统计信息
# e.g. HDU_1166,HDU_1394,HDU_1754,HDU_2795
# 2) 返回值为遍历路径上的统计信息
# 更新操作可以采用延迟/懒惰标记，在今后更深入的遍历中更新子节点
# (a) 若该统计信息已维护于当前树中的某个中间节点
# 则只需访问至该中间节点就足以获取到所需的完整信息
# (b) 若统计信息并不存于中间节点，只能在遍历的同时进行实时统计
# http://blog.csdn.net/metalseed/article/details/8039326
class SegmentTree(Tree, Number):
    class Node(Tree.Node):
        def __init__(self, low, high, value):
            super(SegmentTree.Node, self).__init__(Interval(low, high), value)

    # @param: list 'lst' stores values of leaves
    # @param: function 'up' updates the values of internal nodes
    # @param: function 'get' retrieves the values of nodes
    def __init__(self, lst, up=lambda x, y: None, get=lambda x, y: None):
        super(SegmentTree, self).__init__()
        self.root = None
        self.up = up
        self.get = get
        self._build(lst)

    def _build(self, lst):
        def recur(sgt, low, high):
            if high - low < 1:
                return
            assert (sgt < len(self.root))
            if high - low == 1:
                self.root[sgt] = self.__class__.Node(low, high, lst[low])
            else:
                left, right = sgt << 1 | 1, (sgt + 1) << 1
                mid = low + (high - low + 1) / 2
                recur(left, low, mid)
                recur(right, mid, high)
                self.root[sgt] = self.__class__.Node(low, high,
                                                     self.up(self.root[left].value,
                                                             self.root[right].value if self.root[right] else None))

        assert (not self.root)
        self.root = [None] * (2 ** int(math.ceil(math.log(len(lst), 2)) + 1))
        recur(0, 0, len(lst))

    def search(self, low, high):
        assert (low < high)

        def recur(sgt):
            if sgt < len(self.root) and self.root[sgt]:
                if itv.contain(self.root[sgt].key):
                    return self.root[sgt].value
                else:
                    # 1) top-down
                    # 2) recursion
                    left = recur(sgt << 1 | 1)
                    right = recur((sgt + 1) << 1)
                    # 3) bottom-up
                    # self.root[sgt].value = self.up(self.root[sgt << 1 | 1].value, self.root[(sgt + 1) << 1].value)
                    return self.get(left, right)
            return None

        itv = Interval(low, high)
        return recur(0)


class SegmentTreeTest(TreeTest, NumberTest):
    def __init__(self, num):
        assert (num > 0)
        super(SegmentTreeTest, self).__init__(SegmentTree, 0, True, True)
        self.tree = None
        self.cases = self._gencase(each=1, total=num)
        print '=' * 50
        print "sample size:\t", len(self.cases)

    def testcase(self):
        # refer to rmq
        pass


if __name__ == '__main__':
    SegmentTreeTest(100).testcase()
    print 'done'
