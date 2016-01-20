# -*- coding: utf-8 -*-
# data structure: left-leaning red-black (LLRB) tree
# 属于传统红黑树的一种变种，增加了“左倾”这一约束，
# 使得需要分类讨论的可能性变少了，因此实现上也相对地简单了

import rbt, bst


# LLRB树的实现涉及有以下几种策略上的选择：
# 选择不同的策略意味着树的表现特征会有所区别
# 【1】2-3 tree vs. 2-3-4 tree
# 前者要求在破坏树的结构后，在bottom-up阶段重新平衡树并消除4-node
# 后者要求在破坏树的结构后，在bottom-up阶段重新平衡树即可
# 实现上的区别就在于破坏结构并重新平衡后，是否仍允许4-node的存在
# 目前采用的实现方式是基于2-3树，分类讨论的情形可以略微简单点
# 【2】left-leaning vs. right-leaning
# 选择任何一种在实现和性能上都没有任何实质性的区别，且两种实现方式还是相互对称的
# 但由于倾向了“一侧”，因此对左右子树的处理可能会略有不同
# 但也可以规避，例如deleteMax()的实现，在每次递归中，总是首先将当前层由左倾转换成右倾
# 于是随后的操作就与deleteMin()中的完全对称了


class LLRB(rbt.RBT):
    def __init__(self):
        super(LLRB, self).__init__()

    # ------------------------------------------------------------------------------------

    # 相比于传统的红黑树，三个基本操作所产生的额外副作用
    # 1）_rotateLeft()：将rbt.right.left这棵左子树变成了右子树
    # 2）_rotateRight()：可能将rbt从一颗左子树变成了右子树
    # 3）_flipColor()：无
    # 注意这三个操作是同时适用于2-3和2-3-4 tree、left-和right-leaning策略的
    # 因为其没有维护这些策略的各自特征，具体实现哪种策略取决于这些操作的使用场合和组合

    # based on the left-leaning characteristic
    @classmethod
    def _balance(cls, rbt):
        # [use case] a; b+c; a+b+c(==c)
        # Taking the side-effects of the three elementary operations and
        # the use cases listed above into consideration,
        # the following sequence can not only eliminate all the side-effects,
        # but also locally re-balance the rbt tree.
        if rbt.right and rbt.right.color:  # a
            rbt = cls._rotateLeft(rbt)
        if rbt.left and rbt.left.color and rbt.left.left and rbt.left.left.color:  # b
            rbt = cls._rotateRight(rbt)
        if rbt.left and rbt.left.color and rbt.right and rbt.right.color:  # c
            rbt = cls._flipColor(rbt)
        return rbt

    # ------------------------------------------------------------------------------------

    # this insertion implementation which only useful for 2-3-4 tree is just for instance
    def insert2(self, key, value):
        # 4-node, i.e. rbt.left.color and rbt.right.color, is acceptable now
        def _balance(rbt):
            # [use case] a; b; a+b(==0)
            if rbt.right and rbt.right.color:  # a
                rbt = self._rotateLeft(rbt)
            if rbt.left and rbt.left.color and rbt.left.left and rbt.left.left.color:  # b
                rbt = self._rotateRight(rbt)
            return rbt

        # @invariant: rbt node isn't in (as a part of) a 4-node
        def _recur(rbt, key, value):
            if rbt == None:
                return self.__class__.Node(key, value)  # due to invariant, a new node can be inserted directly
            # step1) top-down: eliminate 4-node in order to meet the needs of next recursion
            # 2-3 tree: naturally no 4-node
            # 2-3-4 tree: split 4-node
            if rbt.left and rbt.left.color and rbt.right and rbt.right.color:
                rbt = self._flipColor(rbt)
            # step2) recursion
            if key < rbt.key:
                rbt.left = _recur(rbt.left, key, value)
            elif key > rbt.key:
                rbt.right = _recur(rbt.right, key, value)
            else:
                rbt.value = value
            # step3) bottom-up
            rbt = _balance(rbt)
            return rbt

        self.root = _recur(self.root, key, value)
        if self.root.color:
            assert (not (self.root.left and self.root.left.color and self.root.right and self.root.right.color))
            self.root.color = False

    # ------------------------------------------------------------------------------------

    # @what: turn rbt.left node into a 3- or 4- node, regardless of its leaning characteristic
    @classmethod
    def _makeLeftRed(cls, rbt):
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.left == None:
            return rbt
        if rbt.left.color or (rbt.left.left and rbt.left.left.color) \
                or (rbt.left.right and rbt.left.right.color):
            return rbt
        if rbt.color:
            rbt = cls._flipColor(rbt)
            if rbt.right and rbt.right.left and rbt.right.left.color:
                rbt.right = cls._rotateRight(rbt.right)  # keep the "left-leaning" characteristic of rbt.right subtree
                rbt = cls._rotateLeft(rbt)
                rbt = cls._flipColor(rbt)
        else:
            rbt = cls._rotateLeft(rbt)
        assert (rbt.left.color or (rbt.left.left and rbt.left.left.color) \
                or (rbt.left.right or rbt.left.right.color))
        return rbt

    @classmethod
    def _makeRightRed(cls, rbt):
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.right == None:
            return rbt
        if rbt.right.color or (rbt.right.left and rbt.right.left.color) \
                or (rbt.right.right and rbt.right.right.color):
            return rbt
        if rbt.color:
            rbt = cls._flipColor(rbt)
            if rbt.left and rbt.left.left and rbt.left.left.color:
                rbt = cls._rotateRight(rbt)
                rbt = cls._flipColor(rbt)
        else:
            rbt = cls._rotateRight(rbt)
        assert (rbt.right.color or (rbt.right.left and rbt.right.left.color) \
                or (rbt.right.right and rbt.right.right.color))
        return rbt

    # ------------------------------------------------------------------------------------

    def check(self):
        def _recur(rbt):
            if rbt == None:
                return
            _recur(rbt.left if rbt.left else None)
            _recur(rbt.right if rbt.right else None)
            # 1) 显式特征：来源于树的定义
            assert (not (rbt.right and rbt.right.color))  # left-leaning (1)
            # 2) 隐式特征：根据对于树的结构的变更操作可推导得出
            if rbt.left and not rbt.left.color:
                assert (rbt.right)  # left-leaning (2)
            if rbt.right:
                assert (rbt.left)  # left-leaning (3)

        super(LLRB, self).check()
        _recur(self.root)


if __name__ == '__main__':
    test = bst.BSTTest(LLRB, 500, True)
    test.deleteMaxMin()
    test.delete()
    print 'done'
