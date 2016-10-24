# -*- coding: utf-8 -*-
# data structure: red-black tree
# 红黑树属于2-3(-4)树的一种变种


from bst import SelfBalancingBinarySearchTree, BinarySearchTreeTest, AugmentedBinarySearchTreeWrapper


class RedBlackTree(SelfBalancingBinarySearchTree):
    class Node(SelfBalancingBinarySearchTree.Node):
        __slots__ = ['color']

        def __init__(self, key, value):
            super(RedBlackTree.Node, self).__init__(key, value)
            # default color of a new leaf node is red
            self.color = True  # True if red else False (black)

    def __init__(self):
        super(RedBlackTree, self).__init__()

    # ------------------------------------------------------------------------------------

    # 1) rotate left：no side-effect
    # 2) rotate right：no side-effect
    # 3) flip color：change subtree's height

    # @invariant: 'rbt' is a red-black tree
    def _rotateLeft(self, rbt):
        assert (rbt and rbt.right)
        rbt = self._rotateLeft_(rbt)
        assert (rbt.left)
        # concerning the augment
        clr = rbt.left.color
        rbt.left.color = rbt.color
        rbt.color = clr
        return rbt

    # @invariant: 'rbt' is a red-black tree
    def _rotateRight(self, rbt):
        assert (rbt and rbt.left)
        rbt = self._rotateRight_(rbt)
        assert (rbt.right)
        clr = rbt.right.color
        rbt.right.color = rbt.color
        rbt.color = clr
        return rbt

    # @invariant: 'rbt' is a relaxed red-black tree
    # @what: turn 'rbt' from a 2-node into a 4-node, or reversely
    def _flipColor(self, rbt):
        assert (rbt and rbt.left and rbt.right)
        rbt.left.color = not rbt.left.color
        rbt.right.color = not rbt.right.color
        rbt.color = not rbt.color
        return rbt

    # ------------------------------------------------------------------------------------

    # @premise: at most one of 'rbt', 'rbt.left' and 'rbt.right' is a 4-node
    # @what: eliminate 4-node, resulting in the balance of 'rbt' subtree
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
        assert (key is not None and value is not None)
        self.root = self._insert(self.root, key, value)
        if self.root.color:
            assert (not (self.root.left and self.root.left.color and self.root.right and self.root.right.color))
            self.root.color = False

    # @invariant: 'rbt' is a red-black tree
    def _insert(self, rbt, key, value):
        if not rbt:  # termination of recursion
            return self.__class__.Node(key, value)  # insertion
        # 1) top-down
        pass  # naturally no 4-node
        # 2) recursion: traverse
        if key < rbt.key:
            rbt.left = self._insert(rbt.left, key, value)
        elif key > rbt.key:
            rbt.right = self._insert(rbt.right, key, value)
        else:
            rbt.value = value  # override
        # 3) bottom-up: re-balance in order to maintain invariant
        rbt = self._balance(rbt)
        return rbt

    # ------------------------------------------------------------------------------------

    # the following are two primitives for deletion only in top-down step
    # @premise: 'rbt' is a 3-node
    # @invariant: 'rbt.right' is a balanced red-black tree,
    # which will neither be traversed after return nor need to be balanced
    # @what: turn 'rbt.left' into a 3-node
    # @how: move red from 'rbt' or 'rbt.right' node to 'rbt.left' node
    # @when: before traversing the 'rbt.left' subtree
    def _makeLeftRed(self, rbt):
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if not rbt.left:
            return rbt  # 'rbt.left' doesn't exist
        if rbt.left.color or (rbt.left.left and rbt.left.left.color) \
                or (rbt.left.right and rbt.left.right.color):
            return rbt  # 'rbt.left' is already a 3-node
        if rbt.color:
            rbt = self._flipColor(rbt)  # move red from 'rbt' node to 'rbt.left' and 'rbt.right' node
            # if 'rbt.right' is no longer a red-black tree
            if rbt.right and ((rbt.right.left and rbt.right.left.color)
                              or (rbt.right.right and rbt.right.right.color)):
                if rbt.right.left and rbt.right.left.color:
                    rbt.right = self._rotateRight(rbt.right)
                rbt = self._rotateLeft(rbt)
                rbt = self._flipColor(rbt)
                assert (rbt.left.left.color)  # color of the original 'rbt.left' node is already red
        else:
            assert (rbt.right.color)
            rbt = self._rotateLeft(rbt)  # move red from 'rbt.right' node to 'rbt.left' node
        assert (rbt.left.color or (rbt.left.left and rbt.left.left.color)
                or (rbt.left.right or rbt.left.right.color))
        return rbt

    # it's completely symmetric to _makeLeftRed()
    def _makeRightRed(self, rbt):
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if not rbt.right:
            return rbt
        if rbt.right.color or (rbt.right.left and rbt.right.left.color) \
                or (rbt.right.right and rbt.right.right.color):
            return rbt
        if rbt.color:
            rbt = self._flipColor(rbt)
            if rbt.left and ((rbt.left.left and rbt.left.left.color)
                             or (rbt.left.right and rbt.left.right.color)):
                if rbt.left.right and rbt.left.right.color:
                    rbt.left = self._rotateLeft(rbt.left)
                rbt = self._rotateRight(rbt)
                rbt = self._flipColor(rbt)
                assert (rbt.right.right.color)
        else:
            assert (rbt.left.color)
            rbt = self._rotateRight(rbt)
        assert (rbt.right.color or (rbt.right.left and rbt.right.left.color)
                or (rbt.right.right and rbt.right.right.color))
        return rbt

    # ------------------------------------------------------------------------------------

    # used by deleteMax, deleteMin, delete
    def _deletePattern(self, func, *args):
        assert (callable(func))
        if self.root:
            if not (self.root.left and self.root.left.color) and not (self.root.right and self.root.right.color):
                # make sure that 'root' isn't a 2-node before recursion
                self.root.color = True
            self.root = func(self.root, *args)  # start recursion
            if self.root and self.root.color:
                assert (not (self.root.left and self.root.left.color and self.root.right and self.root.right.color))
                self.root.color = False

    def delete(self, key):
        self._deletePattern(self._delete, key)

    def _delete(self, rbt, key):
        if not rbt:  # termination of recursion
            return rbt  # deletion failed
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if key < rbt.key:
            # 1) top-down
            rbt = self._makeLeftRed(rbt)
            # 2) recursion
            rbt.left = self._delete(rbt.left, key)
            # 3) bottom-up
            rbt = self._balance(rbt)
        elif key > rbt.key:
            rbt = self._makeRightRed(rbt)
            rbt.right = self._delete(rbt.right, key)
            rbt = self._balance(rbt)
        else:  # if 'rbt' node is the target
            # 用左子树中的最大点还是右子树中的最小点来替换要被删除的目标点：_deleteMax(rbt.left) vs. _deleteMin(rbt.right)
            # 两种策略的实现方式是完全对称的，但对于LLRB树而言，由于其左倾的特性，选择后者效率会更高
            if rbt.right:
                # 1) top-down
                rbt = self._makeRightRed(rbt)
                # 2) deletion or traversal
                if rbt.key != key:  # if 'rbt' node is no longer the one before _makeRightRed()
                    rbt.right = self._delete(rbt.right, key)  # go on traverse
                else:
                    m = self._getMin(rbt.right)
                    rbt.right = self._deleteMin(rbt.right)  # deletion
                    assert (self._search(rbt.right, m.key) is None)
                    rbt.key = m.key
                    rbt.value = m.value
                # 3) bottom-up
                rbt = self._balance(rbt)
            elif rbt.left:
                rbt.left.color = rbt.color
                rbt = rbt.left  # deletion
                # no need to re-balance due to premise
            else:
                rbt = None  # deletion
        return rbt

    def deleteMax(self):
        self._deletePattern(self._deleteMax)

    # @premise: 'rbt' is a 3-node
    # @invariant: 'rbt' is a relaxed red-black tree
    def _deleteMax(self, rbt):
        assert (rbt)
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.right:
            # 1) top-down
            rbt = self._makeRightRed(rbt)
            # 2) recursion
            rbt.right = self._deleteMax(rbt.right)
            # 3) bottom-up
            rbt = self._balance(rbt)
        else:
            if rbt.left:
                rbt.left.color = rbt.color
            rbt = rbt.left
        return rbt

    def deleteMin(self):
        self._deletePattern(self._deleteMin)

    def _deleteMin(self, rbt):
        assert (rbt)
        assert (rbt.color or (rbt.left and rbt.left.color) or (rbt.right and rbt.right.color))
        if rbt.left:
            rbt = self._makeLeftRed(rbt)
            rbt.left = self._deleteMin(rbt.left)
            rbt = self._balance(rbt)
        else:
            if rbt.right:
                rbt.right.color = rbt.color
            rbt = rbt.right
        return rbt

    # ------------------------------------------------------------------------------------

    # @return: black-height
    def _check(self, rbt, left, right):
        if not rbt:
            return 0
        if rbt.left:
            assert (rbt.key > rbt.left.key)
        if rbt.right:
            assert (rbt.key < rbt.right.key)
        assert (left == right)  # left and right subtree hold the same black-height
        assert (not (rbt.left and rbt.left.color and rbt.right and rbt.right.color))
        if rbt is self.root:
            assert (not (self.root and self.root.color))  # not necessary for a relaxed red-black tree
        if rbt.color:
            assert (not (rbt.left and rbt.left.color) and not (rbt.right and rbt.right.color))
            return left
        return left + 1


class AugmentedRedBlackTree(AugmentedBinarySearchTreeWrapper, RedBlackTree):
    def __init__(self):
        super(AugmentedRedBlackTree, self).__init__()


if __name__ == '__main__':
    BinarySearchTreeTest(RedBlackTree).testcase()
    print 'done'
