# -*- coding: utf-8 -*-
# data structure: segment tree
# Segment tree is, in principle, a static structure,
# i.e. its structure cannot be modified once it is built.
# 1）整棵线段树的构建是基于一个连续的区间
# 2）所有叶子节点的数量就是构建这棵树的区间的长度
# 3）中间节点所表示的区间通常都是通过二分法得到的
# 这样就保证了树的高度与区间的长度之间的关系是对数级
# 4）线段树的静态结构意味着每次查询所遍历的路径几乎是相似的
# 通过在每个节点中维护额外的信息，来应对不同的实际问题
# 通常叶子节点维护的是真实信息，中间节点维护的是统计信息
# 以便从上至下搜索时的遍历决策
# 这充分展现了其作为查找树的初衷（并非只关乎如何调整结构）

from binary import bst


# 根据实际问题对于query返回值的不同需求
# 线段树有以下几种不同的实现和维护策略：
# 1）返回值存储并维护于叶子节点中
# 需要从树根完整地遍历至（若干个）叶子节点
# 可以在bottom-up阶段重新维护中间节点的统计信息
# e.g. HDU_1166,HDU_1394,HDU_1754,HDU_2795
# 2）返回值为遍历路径上的统计信息
# 更新操作可以采用延迟/懒惰标记，在今后更深入的遍历中更新子节点
# (a) 若该统计信息已维护于当前树中的某个中间节点
# 则只需访问至该中间节点就足以获取到所需的完整信息
# (b) 若统计信息并不存于中间节点，只能在遍历的同时进行实时统计
# http://blog.csdn.net/metalseed/article/details/8039326
class SegmentTree(bst.BinarySearchTree):
    class Node:
        def __init__(self, low, high, value=0):
            assert (low <= high)
            self.low = low
            self.high = high
            self.value = value  # 该信息没有实际意义，只是举例

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
                    # e.g. 更新或返回当前节点的value
                    return
                # 1) top-down
                pass
                # 2) recursion
                left, right = 0, 0
                if ifIntervalsOverlapped((low, high), (self.root[sgt << 1].low, self.root[sgt << 1].high)):
                    # travserse left subtree
                    lval = _recur(sgt << 1, (low, high))  # 子树的遍历中可以选择性地将传入的区间范围缩小至仅与子树重叠的部分
                if ifIntervalsOverlapped((low, high), (self.root[sgt << 1 | 1].low, self.root[sgt << 1 | 1].high)):
                    # traverse right subtree
                    rval = _recur(sgt << 1 | 1, (low, high))
                # 3) bottom-up
                # e.g. 基于子节点变更后的value来更新或返回当前节点的value
                return

        assert (low <= high)
        return _recur(1, (low, high))


if __name__ == '__main__':
    t = SegmentTree()
    t.build((1, 5))
