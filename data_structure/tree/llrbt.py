# -*- coding: utf-8 -*-
# data structure: left-leaning red-black (LLRB) tree
# 属于传统红黑树的一种变种，增加了"左倾"这一约束
# 使得需要分类讨论的可能性变少了，因此实现上也相对地简单了


from bst import BinarySearchTreeTest
from rbt import RedBlackTree


# LLRB树的实现涉及有以下几种策略上的选择：
# 选择不同的策略意味着树的表现特征会有所区别
# 1) 2-3 tree vs. 2-3-4 tree
# 前者要求在破坏树的结构后，在bottom-up阶段重新平衡树并消除4-node
# 后者要求在破坏树的结构后，在bottom-up阶段重新平衡树即可
# 实现上的区别就在于破坏结构并重新平衡后，是否仍允许4-node的存在
# 目前采用的实现方式是基于2-3树，分类讨论的情形可以略微简单点
# 2) left-leaning vs. right-leaning
# 选择任何一种在实现和性能上都没有任何实质性的区别，且两种实现方式还是相互对称的
# 只是由于倾向了一侧，所以对左右子树的处理可能会略有不同
# 但也可以规避，例如delete()的实现，在每次递归中，总是首先将当前层由左倾转换成右倾
# 即在top-down阶段破坏左倾的特性，于是随后的操作就完全对称了
class LeftLeaningRedBlackTree(RedBlackTree):
    def __init__(self):
        super(LeftLeaningRedBlackTree, self).__init__()

    # ------------------------------------------------------------------------------------

    # 相比于传统的红黑树，三个基本操作所产生的额外副作用
    # 1) rotateLeft()：将rbt.right.left这棵左子树变成了右子树
    # 2) rotateRight()：可能将rbt从一颗左子树变成了右子树
    # 3) flipColor()：无
    # 注意这三个操作是同时适用于2-3和2-3-4 tree、left-和right-leaning策略的
    # 因为其没有维护这些策略的各自特征，具体实现哪种策略取决于这些操作之间的组合

    # based on the left-leaning characteristic
    def _balance(self, rbt):
        assert (rbt)
        # @case: a; b+c; a+b+c(==c)
        if rbt.right and rbt.right.color:  # a
            rbt = self._rotateLeft(rbt)
        if rbt.left and rbt.left.color and rbt.left.left and rbt.left.left.color:  # b
            rbt = self._rotateRight(rbt)
        if rbt.left and rbt.left.color and rbt.right and rbt.right.color:  # c
            rbt = self._flipColor(rbt)
        return rbt

    # ------------------------------------------------------------------------------------

    # this implementation only useful for 2-3-4 tree is just for instance here
    def insert2(self, key, value):
        # 4-node, i.e. rbt.left.color and rbt.right.color, is now acceptable
        def _balance(rbt):
            # @case: a; b; a+b(==0)
            if rbt.right and rbt.right.color:  # a
                rbt = self._rotateLeft(rbt)
            if rbt.left and rbt.left.color and rbt.left.left and rbt.left.left.color:  # b
                rbt = self._rotateRight(rbt)
            return rbt

        # @invariant: rbt node isn't in (as a part of) a 4-node
        def recur(rbt, key, value):
            if rbt == None:
                return self.__class__.Node(key, value)  # due to invariant, a new node can be inserted directly
            # 1) top-down: eliminate 4-node in order to meet the needs of next recursion
            # 2-3 tree: naturally without 4-node
            # 2-3-4 tree: split 4-node
            if rbt.left and rbt.left.color and rbt.right and rbt.right.color:
                rbt = self._flipColor(rbt)
            # 2) recursion
            if key < rbt.key:
                rbt.left = recur(rbt.left, key, value)
            elif key > rbt.key:
                rbt.right = recur(rbt.right, key, value)
            else:
                rbt.value = value
            # 3) bottom-up
            rbt = _balance(rbt)
            return rbt

        self.root = recur(self.root, key, value)
        if self.root.color:
            assert (not (self.root.left and self.root.left.color and self.root.right and self.root.right.color))
            self.root.color = False

    # ------------------------------------------------------------------------------------

    # @what: turn rbt.left node into a 3- or 4- node, regardless of its leaning characteristic
    def _makeLeftRed(self, rbt):
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.left == None:
            return rbt
        if rbt.left.color or (rbt.left.left and rbt.left.left.color) \
                or (rbt.left.right and rbt.left.right.color):
            return rbt
        if rbt.color:
            rbt = self._flipColor(rbt)
            if rbt.right and rbt.right.left and rbt.right.left.color:
                rbt.right = self._rotateRight(rbt.right)  # keep the "left-leaning" characteristic of rbt.right subtree
                rbt = self._rotateLeft(rbt)
                rbt = self._flipColor(rbt)
        else:
            rbt = self._rotateLeft(rbt)
        assert (rbt.left.color or (rbt.left.left and rbt.left.left.color) \
                or (rbt.left.right or rbt.left.right.color))
        return rbt

    def _makeRightRed(self, rbt):
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.right == None:
            return rbt
        if rbt.right.color or (rbt.right.left and rbt.right.left.color) \
                or (rbt.right.right and rbt.right.right.color):
            return rbt
        if rbt.color:
            rbt = self._flipColor(rbt)
            if rbt.left and rbt.left.left and rbt.left.left.color:
                rbt = self._rotateRight(rbt)
                rbt = self._flipColor(rbt)
        else:
            rbt = self._rotateRight(rbt)
        assert (rbt.right.color or (rbt.right.left and rbt.right.left.color) \
                or (rbt.right.right and rbt.right.right.color))
        return rbt

    # ------------------------------------------------------------------------------------

    def _check(self, rbt, left, right):
        ret = super(LeftLeaningRedBlackTree, self)._check(rbt, left, right)
        if rbt:
            # 1) 显式特征：来源于树的定义
            assert (not (rbt.right and rbt.right.color))  # left-leaning (1)
            # 2) 隐式特征：根据对于树结构的变更操作可推导得出
            if rbt.left and not rbt.left.color:
                assert (rbt.right)  # left-leaning (2)
            if rbt.right:
                assert (rbt.left)  # left-leaning (3)
        return ret


if __name__ == '__main__':
    BinarySearchTreeTest(LeftLeaningRedBlackTree, 500).testcase()
    print 'done'
