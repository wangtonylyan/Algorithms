# -*- coding: utf-8 -*-
# data structure: left-leaning red-black (LLRB) tree

import bst

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


class LLRB(bst.BST):
    class Node:
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.color = True  # True if red else False (black)

    def __init__(self):
        self.root = None

    # ------------------------------------------------------------------------------------

    # the following are three elementary and "atomic" operations
    # which can be used to balance an unbalanced red-black tree
    # 1）rotate left：不会改变rbt.color，但有其他side-effect
    # 2）rotate right：不会改变rbt.color，但有其他side-effect
    # 3）flip color：会改变rbt.color，但无其他side-effect
    # rotate left与rotate right这两个操作是完全对称的，且互为可逆
    # 例如，对同一颗树先后各执行一次这两个操作，该树的结构不变
    # 注意这三个操作是同时适用于2-3和2-3-4 tree、left-和right-leaning策略的
    # 因为其没有维护这些策略的各自特征，具体实现哪种策略取决于这些操作的使用场合和组合
    @staticmethod
    def _rotateLeft(rbt):
        assert (rbt and rbt.right)
        ret = rbt.right
        rbt.right = ret.left  # turn a left tree into a right tree, with side-effect
        ret.left = rbt
        ret.color, rbt.color = rbt.color, ret.color
        return ret

    @staticmethod
    def _rotateRight(rbt):
        assert (rbt and rbt.left)
        ret = rbt.left
        rbt.left = ret.right  # turn a right tree into a left tree
        ret.right = rbt  # maybe turn a left tree into a right tree, with side-effect
        ret.color, rbt.color = rbt.color, ret.color
        return ret

    # turn a 2-node into a 4-node, or reversely
    @staticmethod
    def _flipColor(rbt):
        assert (rbt and rbt.left and rbt.right)
        rbt.color = not rbt.color
        rbt.left.color = not rbt.left.color
        rbt.right.color = not rbt.right.color
        return rbt

    # ------------------------------------------------------------------------------------

    # based on the left-leaning characteristic
    def _balance(self, rbt):
        # [use case] a; b+c; a+b+c(==c)
        # Taking the side-effects of the three elementary operations and
        # the use cases listed above into consideration,
        # the following sequence can not only eliminate all the side-effects,
        # but also locally re-balance the rbt tree.
        if rbt.right and rbt.right.color:  # a
            rbt = self._rotateLeft(rbt)
        if rbt.left and rbt.left.color and rbt.left.left and rbt.left.left.color:  # b
            rbt = self._rotateRight(rbt)
        if rbt.left and rbt.left.color and rbt.right and rbt.right.color:  # c
            rbt = self._flipColor(rbt)
        return rbt

    def insert(self, key, value):
        # @premise: rbt isn't in (as a part of) a 4-node
        # which only makes sense when insertion (i.e. in the termination)
        def _recur(rbt, key, value):
            if rbt == None:  # termination of recursion
                # because of the premise, a new node can be inserted directly
                return self.__class__.Node(key, value)  # insert a new leaf node
            # step1) top-down
            # Because now rbt becomes the node of no interest,
            # the current premise doesn't need to be kept any more,
            # which means ,for example, you can make rbt a 2-node.
            # But this is exactly where the preparation for the establishment
            # of the premise of the next recursion should take place,
            # so make sure rbt node is not the "root" of a 4-node.
            pass  # 2-3 tree naturally has no 4-node
            # step2) traversal
            if key < rbt.key:
                rbt.left = _recur(rbt.left, key, value)
            elif key > rbt.key:
                rbt.right = _recur(rbt.right, key, value)
            else:
                rbt.value = value
            # step3) bottom-up
            rbt = self._balance(rbt)
            return rbt

        self.root = _recur(self.root, key, value)
        self.root.color = False

    # 2-3-4 tree, just for example
    def insert2(self, key, value):
        # 4-node, i.e. rbt.left.color and rbt.right.color, is acceptable now
        def _balance2(rbt):
            # [use case] a; b; a+b(==0)
            if rbt.right and rbt.right.color:  # a
                rbt = self._rotateLeft(rbt)
            if rbt.left and rbt.left.color and rbt.left.left and rbt.left.left.color:  # b
                rbt = self._rotateRight(rbt)
            return rbt

        # @premise: the same as insert._recur()
        def _recur(rbt, key, value):
            if rbt == None:
                return self.__class__.Node(key, value)
            # step1) top-down
            if rbt.left and rbt.left.color and rbt.right and rbt.right.color:
                rbt = self._flipColor(rbt)  # split 4-node
            # step2) traversal
            if key < rbt.key:
                rbt.left = _recur(rbt.left, key, value)
            elif key > rbt.key:
                rbt.right = _recur(rbt.right, key, value)
            else:
                rbt.value = value
            # step3) bottom-up
            rbt = _balance2(rbt)
            return rbt

        self.root = _recur(self.root, key, value)
        self.root.color = False

    # ------------------------------------------------------------------------------------

    # the following are two elementary and "atomic" operations for deletion only
    # @premise: rbt isn't a 2-node
    # @what: turn rbt.left into a 3- or 4- node, regardless of its leaning characteristic
    # @how: move red from rbt or rbt.right to rbt.left
    # @when: before traversing the rbt.left tree
    # @invariant: rbt.right is always a LLRB tree, and won't be traversed after return
    @classmethod
    def _makeLeftRed(cls, rbt):
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.left == None:
            return rbt  # rbt.left doesn't exist
        if rbt.left.color or (rbt.left.left and rbt.left.left.color) \
                or (rbt.left.right and rbt.left.right.color):
            return rbt  # rbt.left is already not a 2-node
        if rbt.color:
            rbt = cls._flipColor(rbt)  # move red from rbt to rbt.left and rbt.right
            if rbt.right and rbt.right.left and rbt.right.left.color:  # if rbt.right is no longer a LLRB tree
                rbt.right = cls._rotateRight(rbt.right)  # keep the "left-leaning" characteristic of rbt.right
                rbt = cls._rotateLeft(rbt)  # move red from rbt.right to rbt.left instead
                rbt = cls._flipColor(rbt)  # move red back to rbt
        else:  # if rbt.right.color
            rbt = cls._rotateLeft(rbt)
        assert (rbt.left.color or (rbt.left.left and rbt.left.left.color) \
                or (rbt.left.right or rbt.left.right.color))
        return rbt

    # it's basically symmetric to _makeLeftRed()
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
        else:  # if rbt.left.color
            rbt = cls._rotateRight(rbt)
        assert (rbt.right.color or (rbt.right.left and rbt.right.left.color) \
                or (rbt.right.right and rbt.right.right.color))
        return rbt

    # ------------------------------------------------------------------------------------

    def deleteMin(self):
        if self.root:
            # make sure that the root node isn't a 2-node before recursion
            self.root.color = True if not (self.root.left and self.root.left.color) else False
            self.root = self._deleteMin(self.root)  # start recursion
            if self.root:
                self.root.color = False

    # @premise: rbt is in (as a part of) a 3- or 4-node (but not the "root" node of a 4-node),
    # regardless of its leaning characteristic
    # which only makes sense when deletion (i.e. in the termination)
    def _deleteMin(self, rbt):
        # Because of the disregard for the leaning characteristic by _makeLeft/RightRed() operation,
        assert (rbt.color or (rbt.left and rbt.left.color) \
                or (rbt.right and rbt.right.color))  # firstly, this happens,
        if rbt.left == None:  # termination of recursion
            # and secondly, here are two cases needed discussion:
            if rbt.right:
                # This doesn't happen in a left-leaning red-black tree
                # in which the "red" minimum node must have no right subtree.
                rbt.right.color = rbt.color
                rbt = rbt.right
            else:
                assert (rbt.color and not rbt.right)  # left-leaning
                rbt = None
            return rbt
        # step1) top-down
        rbt = self._makeLeftRed(rbt)
        # step2) traversal
        rbt.left = self._deleteMin(rbt.left)
        # step3) bottom-up
        rbt = self._balance(rbt)
        return rbt

    def deleteMax(self):
        if self.root:
            self.root.color = True if not (self.root.left and self.root.left.color) else False
            self.root = self._deleteMax(self.root)
            if self.root:
                self.root.color = False

    def _deleteMax(self, rbt):
        assert (rbt.color or (rbt.left and rbt.left.color) \
                or (rbt.right and rbt.right.color))
        if rbt.right == None:
            if rbt.left:
                # This doesn't happen in a right-leaning red-black tree
                # in which the "red" maximum node must have no left subtree.
                rbt.left.color = rbt.color
                rbt = rbt.left
            else:
                assert (rbt.color and not rbt.left)  # right-leaning
                rbt = None
            return rbt
        # step1) top-down
        rbt = self._makeRightRed(rbt)
        # step2) traversal
        rbt.right = self._deleteMax(rbt.right)
        # step3) bottom-up
        rbt = self._balance(rbt)
        return rbt

    def delete(self, key):
        # @premise: the same as _deleteMin() and _deleteMax()
        def _recur(rbt, key):
            if rbt == None:
                return rbt
            if key < rbt.key:
                # step1) top-down
                rbt = self._makeLeftRed(rbt)
                # step2) traversal
                rbt.left = _recur(rbt.left, key)
                # step3) bottom-up
                rbt = self._balance(rbt)
            elif key > rbt.key:
                # step1) top-down
                rbt = self._makeRightRed(rbt)
                # step2) traversal
                rbt.right = _recur(rbt.right, key)
                # step3) bottom-up
                rbt = self._balance(rbt)
            else:  # if rbt is the target
                # 用左子树中的最大点还是右子树中的最小点来替换要被删除的目标点：_deleteMax(rbt.left) vs. _deleteMin(rbt.right)
                # 两种策略的实现方式是完全对称的，但由于左倾的特性，选择后者效率更高
                if rbt.right:
                    # step1) top-down
                    rbt = self._makeRightRed(rbt)
                    # step2) deletion or traversal
                    if rbt.key != key:  # if rbt is no longer the original one
                        assert (key > rbt.key)
                        rbt.right = _recur(rbt.right, key)  # go on traversing
                    else:
                        m = self._getMin(rbt.right)
                        rbt.right = self._deleteMin(rbt.right)
                        rbt.key = m.key
                        rbt.value = m.value
                    # step3) bottom-up
                    rbt = self._balance(rbt)
                elif rbt.left:
                    rbt.left.color = rbt.color
                    rbt = rbt.left
                else:
                    rbt = None
            return rbt

        if self.root:
            self.root.color = True if not (self.root.left and self.root.left.color) else False
            self.root = _recur(self.root, key)
            if self.root:
                self.root.color = False

    # ------------------------------------------------------------------------------------

    def check(self):
        def _recur(rbt):
            if rbt == None:
                return
            _recur(rbt.left if rbt.left else None)
            _recur(rbt.right if rbt.right else None)
            # 注意以下这些assertion，可以便于理解及简化实现
            # 1) 显式特征：来源于树的定义
            assert (not (rbt.right and rbt.right.color))  # left-leaning (1)
            assert (not (rbt.left and rbt.left.color and rbt.right and rbt.right.color))  # 2-3 tree (1)
            assert (not (rbt.color and rbt.left and rbt.left.color))  # 2-3 tree (2)
            # 2) 隐式特征：根据对于树的结构的变更操作可推导得出
            if rbt.left and not rbt.left.color:
                assert (rbt.right)  # left-leaning (2)
            if rbt.right:
                assert (rbt.left)  # left-leaning (3)

        super(LLRB, self).check()
        _recur(self.root)


if __name__ == '__main__':
    test = bst.BSTTest(LLRB, 1000)
    test.deleteMaxMin()
    test.delete()
    print 'done'
