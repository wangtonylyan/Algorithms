# -*- coding: utf-8 -*-
# data structure: red-black tree
# 红黑树属于2-3树的一种变种

import bst


class RBT(bst.BBST):
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            # default color of a new leaf node is red
            self.color = True  # True if red else False (black)

    def __init__(self):
        super(RBT, self).__init__()

    # ------------------------------------------------------------------------------------

    # 1）rotate left：no side-effect
    # 2）rotate right：no side-effect
    # 3）flip color：change of height of rbt subtree

    # @invariant: rbt subtree is a red-black tree
    def _rotateLeft(self, rbt):
        assert (rbt and rbt.right)
        rbt = super(RBT, self)._rotateLeft(rbt)
        assert (rbt.left)
        rbt.color, rbt.left.color = rbt.left.color, rbt.color
        return rbt

    # @invariant: rbt subtree is a red-black tree
    def _rotateRight(self, rbt):
        assert (rbt and rbt.left)
        rbt = super(RBT, self)._rotateRight(rbt)
        assert (rbt.right)
        rbt.color, rbt.right.color = rbt.right.color, rbt.color
        return rbt

    # @invariant: rbt subtree is a relaxed red-black tree
    # @what: turn rbt node from a 2-node into a 4-node, or reversely
    def _flipColor(self, rbt):
        assert (rbt and rbt.left and rbt.right)
        rbt.color = not rbt.color
        rbt.left.color = not rbt.left.color
        rbt.right.color = not rbt.right.color
        return rbt

    # ------------------------------------------------------------------------------------

    # @what: re-balance rbt subtree
    def _balance(self, rbt):
        assert (rbt)
        if rbt.left and rbt.left.color:
            if rbt.left.left and rbt.left.left.color:
                rbt = self._rotateRight(rbt)
            elif rbt.left.right and rbt.left.right.color:
                rbt.left = self._rotateLeft(rbt.left)
                rbt = self._rotateRight(rbt)
        elif rbt.right and rbt.right.color:
            if rbt.right.left and rbt.right.left.color:
                rbt.right = self._rotateRight(rbt.right)
                rbt = self._rotateLeft(rbt)
            elif rbt.right.right and rbt.right.right.color:
                rbt = self._rotateLeft(rbt)
        if rbt.left and rbt.left.color and rbt.right and rbt.right.color:
            rbt = self._flipColor(rbt)
        return rbt

    # ------------------------------------------------------------------------------------

    def insert(self, key, value):
        # @invariant: rbt subtree is a red-black tree
        def _recur(rbt, key, value):
            if rbt == None:  # termination of recursion
                return self.__class__.Node(key, value)  # insertion
            # step1) top-down
            # step2) recursion: traverse
            if key < rbt.key:
                rbt.left = _recur(rbt.left, key, value)
            elif key > rbt.key:
                rbt.right = _recur(rbt.right, key, value)
            else:
                rbt.value = value  # override
            # step3) bottom-up: re-balance in order to maintain invariant
            rbt = self._balance(rbt)
            return rbt

        self.root = _recur(self.root, key, value)
        if self.root.color:
            assert (not (self.root.left and self.root.left.color and self.root.right and self.root.right.color))
            self.root.color = False

    # ------------------------------------------------------------------------------------

    # the following are two elementary and atomic operations for deletion only in top-down step
    # @premise: rbt node is a 3-node
    # @invariant: rbt.right subtree is always a balanced red-black tree, and won't be traversed after return
    # @what: turn rbt.left node into a 3-node
    # @how: move red from rbt or rbt.right node to rbt.left node
    # @when: before traversing the rbt.left subtree
    def _makeLeftRed(self, rbt):
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.left == None:
            return rbt  # rbt.left node doesn't exist
        if rbt.left.color or (rbt.left.left and rbt.left.left.color) \
                or (rbt.left.right and rbt.left.right.color):
            return rbt  # rbt.left node is already a 3-node
        if rbt.color:
            rbt = self._flipColor(rbt)  # move red from rbt node to rbt.left and rbt.right node
            # if rbt.right subtree is no longer a red-black tree
            if rbt.right and ((rbt.right.left and rbt.right.left.color) \
                                      or (rbt.right.right and rbt.right.right.color)):
                if rbt.right.left and rbt.right.left.color:
                    rbt.right = self._rotateRight(rbt.right)
                rbt = self._rotateLeft(rbt)
                rbt = self._flipColor(rbt)
                assert (rbt.left.left.color)  # color of the original rbt.left node is already red
        else:  # if rbt.right.color
            rbt = self._rotateLeft(rbt)  # move red from rbt.right node to rbt.left node
        assert (rbt.left.color or (rbt.left.left and rbt.left.left.color) \
                or (rbt.left.right or rbt.left.right.color))
        return rbt

    # it's completely symmetric to _makeLeftRed()
    def _makeRightRed(self, rbt):
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.right == None:
            return rbt
        if rbt.right.color or (rbt.right.left and rbt.right.left.color) \
                or (rbt.right.right and rbt.right.right.color):
            return rbt
        if rbt.color:
            rbt = self._flipColor(rbt)
            if rbt.left and ((rbt.left.left and rbt.left.left.color) \
                                     or (rbt.left.right and rbt.left.right.color)):
                if rbt.left.right and rbt.left.right.color:
                    rbt.left = self._rotateLeft(rbt.left)
                rbt = self._rotateRight(rbt)
                rbt = self._flipColor(rbt)
                assert (rbt.right.right.color)
        else:
            rbt = self._rotateRight(rbt)
        assert (rbt.right.color or (rbt.right.left and rbt.right.left.color) \
                or (rbt.right.right and rbt.right.right.color))
        return rbt

    # ------------------------------------------------------------------------------------

    # used by deleteMax, deleteMin, delete
    def _deletePattern(self, recur, *args):
        if self.root:
            if not (self.root.left and self.root.left.color) and not (self.root.right and self.root.right.color):
                # make sure that the root node isn't a 2-node before recursion
                self.root.color = True
            self.root = recur(self.root) if len(args) == 0 else recur(self.root, *args)  # start recursion
            if self.root and self.root.color:
                assert (not (self.root.left and self.root.left.color and self.root.right and self.root.right.color))
                self.root.color = False

    def deleteMax(self):
        self._deletePattern(self._deleteMax)

    def deleteMin(self):
        self._deletePattern(self._deleteMin)

    def delete(self, key):
        self._deletePattern(self._delete, key)

    # @premise: rbt node is a 3-node
    # @invariant: rbt subtree is a relaxed red-black tree
    def _deleteMax(self, rbt):
        assert (rbt)
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.right == None:
            if rbt.left:
                rbt.left.color = rbt.color
            return rbt.left
        rbt = self._makeRightRed(rbt)
        rbt.right = self._deleteMax(rbt.right)
        rbt = self._balance(rbt)
        return rbt

    def _deleteMin(self, rbt):
        assert (rbt)
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.left == None:  # termination of recursion
            if rbt.right:
                rbt.right.color = rbt.color
            return rbt.right  # deletion
        # step1) top-down
        rbt = self._makeLeftRed(rbt)
        # step2) recursion
        rbt.left = self._deleteMin(rbt.left)
        # step3) bottom-up
        rbt = self._balance(rbt)
        return rbt

    def _delete(self, rbt, key):
        if rbt == None:  # termination of recursion
            return rbt  # deletion failed
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if key < rbt.key:
            # step1) top-down
            rbt = self._makeLeftRed(rbt)
            # step2) recursion
            rbt.left = self._delete(rbt.left, key)
            # step3) bottom-up
            rbt = self._balance(rbt)
        elif key > rbt.key:
            rbt = self._makeRightRed(rbt)
            rbt.right = self._delete(rbt.right, key)
            rbt = self._balance(rbt)
        else:  # if rbt node is the target
            # 用左子树中的最大点还是右子树中的最小点来替换要被删除的目标点：_deleteMax(rbt.left) vs. _deleteMin(rbt.right)
            # 两种策略的实现方式是完全对称的，但对于LLRB树而言，由于其左倾的特性，选择后者效率会更高
            if rbt.right:
                # step1) top-down
                rbt = self._makeRightRed(rbt)
                # step2) deletion or traversal
                if rbt.key != key:  # if rbt node is no longer the one before _makeRightRed
                    rbt.right = self._delete(rbt.right, key)  # go on traverse
                else:
                    m = self._getMin(rbt.right)
                    rbt.right = self._deleteMin(rbt.right)  # deletion
                    rbt.key = m.key
                    rbt.value = m.value
                # step3) bottom-up
                rbt = self._balance(rbt)
            elif rbt.left:
                rbt.left.color = rbt.color
                rbt = rbt.left  # deletion
                # no need to re-balance due to premise
            else:
                rbt = None  # deletion
        return rbt

    # ------------------------------------------------------------------------------------

    def check(self):
        def _recur(rbt):
            if rbt == None:
                return 0
            m = _recur(rbt.left if rbt.left else None)
            n = _recur(rbt.right if rbt.right else None)
            assert (m == n)  # left and right subtree hold the same black-height
            assert (not (rbt.left and rbt.left.color and rbt.right and rbt.right.color))
            if rbt.color:
                assert (not (rbt.left and rbt.left.color) and not (rbt.right and rbt.right.color))
                return m
            return m + 1

        super(RBT, self).check()
        _recur(self.root)
        assert (not (self.root and self.root.color))  # not necessary for a relaxed red-black tree


if __name__ == '__main__':
    test = bst.BSTTest(RBT, 500, True)
    test.deleteMaxMin()
    test.delete()
    print 'done'
