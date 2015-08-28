# -*- coding: utf-8 -*-
# data structure: left-leaning red-black (LLRB) tree

import bst

# LLRB树的实现涉及有以下几种设计上的选择：
# 【1】2-3 tree vs. 2-3-4 tree
# a)当前实现方式是在buttom-up过程中进行flip-color操作，即避免整棵树中存在4-node
#  因此该实现方式下的LLRB tree是与2-3 tree相一致的
# b)若buttom-up过程中不进行flip-color操作，即允许4-node的存在
#  那么仅基于rotate-left和rotate-right操作是无法保证红黑树特性的
#  因此需要在top-down过程中(即未新增节点之前)消除已有的4-node
#  而该实现方式下的LLRB tree则是与2-3-4 tree相一致的
# c)LLRB tree无论是以2-3 tree还是2-3-4 tree的方式实现都是允许的
# 【2】left-leaning vs. right-leaning
# 选择任何一种在实现和性能上都没有任何实质性的区别，且两种实现方式还是彼此对称的
# 但由于倾向了“一侧”，因此对左右子树的处理可能会有微小区别
# 但也可以规避，例如deleteMax()的实现，在每次递归中，总是首先将当前层由左倾转换成右倾
# 于是随后的操作就与deleteMin()中的完全对称了

class RBT(bst.BST):
    class Node:
        def __init__(self, key = None, value = None):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.color = True  # True if red else False (black)

    def __init__(self):
        self.root = None

    # the following are three elementary and atomic operations
    # which can be used to balance an unbalanced red-black tree
    # 1）rotate left
    # 不会改变rbt.color
    # 有side-effect
    # 2）rotate right
    # 不会改变rbt.color
    # 有side-effect
    # 3）flip color
    # 会改变rbt.color
    # 无side-effect
    # rotate left与rotate right这两个操作是完全对称的，且互为可逆
    # 例如，对同一颗树先后各执行一次这两个操作，该树的结构不变
    @staticmethod
    def _rotateLeft(rbt):
        assert (rbt and rbt.right)
        ret = rbt.right
        rbt.right = ret.left  # 将左子树转换成了右子树，有副作用
        ret.left = rbt
        ret.color, rbt.color = rbt.color, ret.color
        return ret

    @staticmethod
    def _rotateRight(rbt):
        assert (rbt and rbt.left)
        ret = rbt.left
        rbt.left = ret.right  # 将右子树转换成了左子树，无副作用
        ret.right = rbt  # 将左子树转换成了右子树，有副作用
        ret.color, rbt.color = rbt.color, ret.color
        return ret

    # transfer a 2-node into a 4-node, or reversely
    @staticmethod
    def _flipColor(rbt):
        assert (rbt and rbt.left and rbt.right)
        rbt.color = not rbt.color
        rbt.left.color = not rbt.left.color
        rbt.right.color = not rbt.right.color
        return rbt

    def _balance(self, rbt):
        # [use case] a; b+c; a+b+c(==c)
        # taking the side-effect of three elementary operations and
        # the use cases listed above into consideration,
        # the following sequence can not only eliminate all the side-effects,
        # but also re-balance the tree
        if rbt.right and rbt.right.color:  # a
            rbt = self._rotateLeft(rbt)
        if rbt.left and rbt.left.color and rbt.left.left and rbt.left.left.color:  # b
            rbt = self._rotateRight(rbt)
        if rbt.left and rbt.left.color and rbt.right and rbt.right.color:  # c
            rbt = self._flipColor(rbt)
        return rbt

    def insert(self, key, value):
        # @premise: rbt isn't in (as a part of) a 4-node
        # which only makes sense when insertion (i.e. in the termination of recursion)
        def _recur(rbt, key, value):
            if rbt == None:  # termination of recursion
                # because of the premise, a new node can be inserted directly
                return self.__class__.Node(key, value)
            # step1) top-down
            # make sure rbt node is not the "root" of a 4-node
            pass  # 2-3 tree naturally has no 4-node
            # step2) recursion
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
        def _balance(rbt):
            # [use case] a; b; a+b(==0)
            if rbt.right and rbt.right.color:  # a
                rbt = self._rotateLeft(rbt)
            if rbt.left and rbt.left.color and rbt.left.left and rbt.left.left.color:  # b
                rbt = self._rotateRight(rbt)
            return rbt

        def _recur(rbt, key, value):
            if rbt == None:
                return self.__class__.Node(key, value)
            # step1) top-down
            if rbt.left and rbt.left.color and rbt.right and rbt.right.color:
                rbt = self._flipColor(rbt)  # split 4-node
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
        self.root.color = False

    # @premise: rbt is neither a 2-node nor the "root" node of a 4-node, and rbt.left is a 2-node
    # @objective: makes rbt.left a 3- or 4-node
    # @method: move red from rbt or rbt.right to rbt.left
    # @invariant: rbt.right is a LLRB tree
    def _moveRedLeft(self, rbt):
        assert (rbt.color and rbt.left and rbt.right)
        assert (not rbt.left.color and not (rbt.left.left and rbt.left.left.color))
        rbt = self._flipColor(rbt)  # move red from rbt to rbt.left and rbt.right
        if rbt.right and rbt.right.left and rbt.right.left.color:  # if rbt.right is no longer a LLRB tree
            rbt.right = self._rotateRight(rbt.right)  # keep the "left-leaning" characteristic
            rbt = self._rotateLeft(rbt)  # move red from rbt.right to rbt.left instead
            rbt = self._flipColor(rbt)  # move red back to rbt
        return rbt

    # it's symmetric to _moveRedLeft(), besides the "left-leaning" characteristic
    def _moveRedRight(self, rbt):
        assert (rbt.color and rbt.left and rbt.right)
        assert (not rbt.right.color and not (rbt.right.left and rbt.right.left.color))
        rbt = self._flipColor(rbt)
        if rbt.left and rbt.left.left and rbt.left.left.color:
            rbt = self._rotateRight(rbt)
            rbt = self._flipColor(rbt)
        return rbt

    def deleteMin(self):
        if self.root:
            # make sure that the root node isn't a 2-node before recursion
            self.root.color = True
            self.root = self._deleteMin(self.root)  # recursion
            if self.root:
                self.root.color = False

    # @premise: rbt is in (as a part of) a 3- or 4-node, but not the "root" node of a 4-node
    # which only makes sense when deletion (i.e. in the termination of recursion)
    def _deleteMin(self, rbt):
        if rbt.left == None:  # termination of recursion
            assert (rbt.color and not rbt.right)  # because rbt is a left-leaning tree
            # because of the premise, rbt node can be deleted directly
            return None  # delete rbt
        # step1) top-down
        # make sure that rbt.left isn't a 2-node
        # now rbt is definitely not the node of interest
        # so the premise doesn't need to be preserved any more
        # which means you can make rbt a 2-node, as long as the premise of next recursion established
        if not rbt.left.color and not (rbt.left.left and rbt.left.left.color):
            rbt = self._moveRedLeft(rbt)
        # else: rbt is already a 3-node
        # step2) recursion
        rbt.left = self._deleteMin(rbt.left)
        # step3) bottom-up
        rbt = self._balance(rbt)
        return rbt

    def deleteMax(self):
        if self.root:
            self.root.color = True
            self.root = self._deleteMax(self.root)
            if self.root:
                self.root.color = False

    def _deleteMax(self, rbt):
        # firstly, turn rbt into a right-leaning red-black tree
        if rbt.left and rbt.left.color:
            rbt = self._rotateRight(rbt)
        # then, the following is totally symmetric to deleteMin()
        if rbt.right == None:
            assert (rbt.color and not rbt.left)
            return None
        # step1) top-down
        if not rbt.right.color and not (rbt.right.left and rbt.right.left.color):
            rbt = self._moveRedRight(rbt)
        # step2) recursion
        rbt.right = self._deleteMax(rbt.right)
        # step3) bottom-up
        rbt = self._balance(rbt)
        return rbt

    def delete(self, key):
        # @premise: as the same as _deleteMin() and _deleteMax()
        def _recur(rbt, key):
            if rbt == None:
                return rbt
            # 用左子树中的最大点还是右子树中的最小点来替换要被删除的目标点：_deleteMax(rbt.left) vs. _deleteMin(rbt.right)
            # a) "key<rbt.key"与"key==rbt.key"这两个cases可以共享top-down的逻辑
            # b) "key>rbt.key"与"key==rbt.key"这两个cases可以共享top-down的逻辑
            def _shareLeft(rbt):
                # make sure that rbt.left isn't a 2-node
                if not (rbt.left and rbt.left.color) and not (rbt.left.left and rbt.left.left.color):
                    rbt = self._moveRedLeft(rbt)
                return rbt

            def _shareRight(rbt):
                # make sure that rbt.right isn't a 2-node
                if rbt.right and rbt.right.left and rbt.right.left.color:
                    rbt.right = self._rotateRight(rbt.right)
                if not rbt.right.color and not (rbt.right.left and rbt.right.left.color):
                    rbt = self._moveRedRight(rbt)
                return rbt

            if key < rbt.key:
                # step1) top-down
                rbt = _shareLeft(rbt)
                # step2) recursion
                rbt.left = _recur(rbt.left, key)
            elif key > rbt.key:
                # step1) top-down
                rbt = _shareRight(rbt)
                # step2) recursion
                rbt.right = _recur(rbt.right, key)
            else:
                if 1:  # a
                    # step1) top-down
                    rbt = _shareLeft(rbt)
                    # step2) deletion
                    m = self._getMax(rbt.left)
                    rbt.left = self._deleteMax(rbt.left)
                    rbt.key = m.key
                    rbt.value = m.value
                else:  # b
                    # step1) top-down
                    rbt = _shareRight(rbt)
                    # step2) deletion
                    m = self._getMin(rbt.right)
                    rbt.right = self._deleteMin(rbt.right)
                    rbt.key = m.key
                    rbt.value = m.value
            # step3) bottom-up
            rbt = self._balance(rbt)
            return rbt

        if self.root:
            self.root.color = True
            self.root = _recur(self.root, key)
            if self.root:
                self.root.color = False

    def check(self):
        def _recur(rbt):
            if rbt == None:
                return
            _recur(rbt.left if rbt.left else None)
            _recur(rbt.right if rbt.right else None)
            # 注意以下这些assertion，可以便于理解及简化实现
            # 1) 显式特征：来源于树的定义
            assert (not (rbt.right and rbt.right.color))  # left-leaning
            assert (not (rbt.left and rbt.left.color and rbt.right and rbt.right.color))  # 2-3 tree
            if rbt.color:
                assert (not (rbt.left and rbt.left.color))
            else:
                assert (not (rbt.left and rbt.left.color and rbt.left.left and rbt.left.left.color))
            # 2) 隐式特征：由对于树的结构的变更操作可推导得出
            # because rbt is a left-leaning tree
            if rbt.left and not rbt.left.color:
                assert (rbt.right)
            if rbt.right:
                assert (rbt.left)

        super(RBT, self).check()
        _recur(self.root)


if __name__ == '__main__':
    test = bst.BSTTest(RBT, 500)
    # test.deleteMaxMin()
    test.delete()
    print 'done'
