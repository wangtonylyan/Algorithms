# -*- coding: utf-8 -*-
# data structure: binary search tree

from base.tree import Tree, TreeTest


class BinarySearchTree(Tree):
    class Node(Tree.Node):
        __slots__ = ['left', 'right']

        def __init__(self, key, value):
            super(BinarySearchTree.Node, self).__init__(key, value)
            self.left = None
            self.right = None

    def __init__(self, cmp):
        super(BinarySearchTree, self).__init__(cmp)

    def __len__(self):
        return self._len(self.root)

    def _len(self, bst):
        if not bst:
            return 0
        return self._len(bst.left) + self._len(bst.right) + 1

    def search(self, key):
        bst = self._search(self.root, key)
        assert (not bst or (self.cmp(bst.key, key) == 0 and bst.value is not None))
        return bst.value if bst else None

    def _search(self, bst, key):
        while bst:
            if self.cmp(key, bst.key) < 0:
                bst = bst.left
            elif self.cmp(key, bst.key) > 0:
                bst = bst.right
            else:
                break
        return bst

    def getMax(self):
        bst = self._getMax(self.root)
        assert (not bst or (bst.key is not None and bst.value is not None))
        return (bst.key, bst.value) if bst else None

    def _getMax(self, bst):
        while bst and bst.right:
            bst = bst.right
        return bst

    def getMin(self):
        bst = self._getMin(self.root)
        assert (not bst or (bst.key is not None and bst.value is not None))
        return (bst.key, bst.value) if bst else None

    def _getMin(self, bst):
        while bst and bst.left:
            bst = bst.left
        return bst

    def preorder(self):
        def recur(bst):
            if not bst:
                return []
            return [bst] + recur(bst.left) + recur(bst.right)

        return recur(self.root)

    def inorder(self):
        def recur(bst):
            if not bst:
                return []
            return recur(bst.left) + [bst] + recur(bst.right)

        return recur(self.root)

    def postorder(self):
        def recur(bst):
            if not bst:
                return []
            return recur(bst.left) + recur(bst.right) + [bst]

        return recur(self.root)

    def insert(self, key, value):
        def recur(bst, key, value):
            if not bst:
                return self.__class__.Node(key, value)
            if self.cmp(key, bst.key) < 0:
                bst.left = recur(bst.left, key, value)
            elif self.cmp(key, bst.key) > 0:
                bst.right = recur(bst.right, key, value)
            else:
                bst.value = value
            return bst

        assert (key is not None and value is not None)
        self.root = recur(self.root, key, value)

    def delete(self, key):
        def recur(bst, key):
            if not bst:
                return None
            if self.cmp(key, bst.key) < 0:
                bst.left = recur(bst.left, key)
            elif self.cmp(key, bst.key) > 0:
                bst.right = recur(bst.right, key)
            else:
                if not bst.left:
                    bst = bst.right
                elif not bst.right:
                    bst = bst.left
                else:
                    if not bst.left.right:
                        bst.left.right = bst.right
                        bst = bst.left
                    elif not bst.right.left:
                        bst.right.left = bst.left
                        bst = bst.right
                    else:
                        it = bst.left
                        while it.right.right:
                            it = it.right
                        bst.key = it.right.key
                        bst.value = it.right.value
                        it.right = it.right.left
            return bst

        self.root = recur(self.root, key)

    def deleteMax(self):
        self.root = self._deleteMax(self.root)

    def _deleteMax(self, bst):
        if bst:
            if bst.right:
                it = bst
                while it.right.right:
                    it = it.right
                it.right = it.right.left
            else:
                bst = bst.left
        return bst

    def deleteMin(self):
        self.root = self._deleteMin(self.root)

    def _deleteMin(self, bst):
        if bst:
            if bst.left:
                it = bst
                while it.left.left:
                    it = it.left
                it.left = it.left.right
            else:
                bst = bst.right
        return bst

    def check(self):
        def recur(bst):
            return self._check(bst, recur(bst.left), recur(bst.right)) if bst else \
                self._check(None, self._check(None, None, None), self._check(None, None, None))

        recur(self.root)

    def _check(self, bst, left, right):
        if not bst:
            return 0
        # check symmetric order property
        if bst.left:
            assert (self.cmp(bst.left.key, bst.key) < 0)
        if bst.right:
            assert (self.cmp(bst.right.key, bst.key) > 0)
        # check size consistency
        if bst is self.root:
            assert (self._len(bst) == left + right + 1)
        return left + right + 1


class SelfAdjustingBinarySearchTree(BinarySearchTree):
    def __init__(self, cmp):
        super(SelfAdjustingBinarySearchTree, self).__init__(cmp)

    # rotate left与rotate right这两个操作是完全对称且互为可逆的
    # always holds the symmetric order property
    def _rotateLeft(self, bst):
        if bst and bst.right:
            tmp = bst.right
            bst.right = tmp.left
            tmp.left = bst
            bst = tmp
        return bst

    def _rotateRight(self, bst):
        if bst and bst.left:
            tmp = bst.left
            bst.left = tmp.right
            tmp.right = bst
            bst = tmp
        return bst


# (自)平衡树大致分为两类：height-balanced和weight-balanced
# 前者关注的是树的高度，后者关注的是树的重量(即树中节点的个数)
class SelfBalancingBinarySearchTree(SelfAdjustingBinarySearchTree):
    def __init__(self, cmp):
        super(SelfBalancingBinarySearchTree, self).__init__(cmp)

    def _balance(self, bst):
        assert (False)


class BinarySearchTreeTest(TreeTest):
    def __init__(self, cls, args={'cmp': cmp}, num=1000, check=True, time=True):
        assert (issubclass(cls, BinarySearchTree) and isinstance(args, dict) and num > 0)
        super(BinarySearchTreeTest, self).__init__(cls, args, num, check, time)


if __name__ == '__main__':
    BinarySearchTreeTest(BinarySearchTree).testcase()
    print 'done'
