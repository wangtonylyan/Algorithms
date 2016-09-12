# -*- coding: utf-8 -*-
# data structure: binary search tree

from data_structure.tree.tree import Tree, TreeTest


class BinarySearchTree(Tree):
    class Node(Tree.Node):
        __slots__ = ['left', 'right']

        def __init__(self, key, value):
            super(BinarySearchTree.Node, self).__init__(key, value)
            self.left = None
            self.right = None

    def __init__(self):
        super(BinarySearchTree, self).__init__()
        self.root = None

    def __len__(self):
        return self._len(self.root)

    def _len(self, bst):
        if bst == None:
            return 0
        return self._len(bst.left) + self._len(bst.right) + 1

    def search(self, key):
        bst = self._search(self.root, key)
        return bst.value if bst else None

    def _search(self, bst, key):
        while bst:
            if key < bst.key:
                bst = bst.left
            elif key > bst.key:
                bst = bst.right
            else:
                break
        return bst

    def getMax(self):
        return self._getMax(self.root)

    def _getMax(self, bst):
        while bst and bst.right:
            bst = bst.right
        return bst

    def getMin(self):
        return self._getMin(self.root)

    def _getMin(self, bst):
        while bst and bst.left:
            bst = bst.left
        return bst

    def preorder(self):
        def recur(bst):
            if bst == None:
                return []
            return [bst] + recur(bst.left) + recur(bst.right)

        return recur(self.root)

    def inorder(self):
        def recur(bst):
            if bst == None:
                return []
            return recur(bst.left) + [bst] + recur(bst.right)

        return recur(self.root)

    def postorder(self):
        def recur(bst):
            if bst == None:
                return []
            return recur(bst.left) + recur(bst.right) + [bst]

        return recur(self.root)

    def insert(self, key, value):
        def recur(bst, key, value):
            if bst == None:
                return self.__class__.Node(key, value)
            if key < bst.key:
                bst.left = recur(bst.left, key, value)
            elif key > bst.key:
                bst.right = recur(bst.right, key, value)
            else:
                bst.value = value
            return bst

        self.root = recur(self.root, key, value)

    def delete(self, key):
        def recur(bst, key):
            if bst == None:
                return None
            if key < bst.key:
                bst.left = recur(bst.left, key)
            elif key > bst.key:
                bst.right = recur(bst.right, key)
            else:
                if bst.left == None:
                    bst = bst.right
                elif bst.right == None:
                    bst = bst.left
                else:
                    if bst.left.right == None:
                        bst.left.right = bst.right
                        bst = bst.left
                    elif bst.right.left == None:
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

    def clean(self):
        self.root = None

    def check(self):
        def recur(bst):
            return self._check(bst, recur(bst.left), recur(bst.right)) if bst else \
                self._check(None, self._check(None, None, None), self._check(None, None, None))

        recur(self.root)

    def _check(self, bst, left, right):
        if bst == None:
            return 0
        # check symmetric order property
        if bst.left:
            assert (bst.left.key < bst.key)
        if bst.right:
            assert (bst.right.key > bst.key)
        # check size consistency
        if bst == self.root:
            assert (self._len(bst) == left + right + 1)
        return left + right + 1


class SelfAdjustingBinarySearchTree(BinarySearchTree):
    def __init__(self):
        super(SelfAdjustingBinarySearchTree, self).__init__()

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


class SelfBalancingBinarySearchTree(SelfAdjustingBinarySearchTree):
    def __init__(self):
        super(SelfBalancingBinarySearchTree, self).__init__()

    def _balance(self, bst):
        assert (False)


class BinarySearchTreeTest(TreeTest):
    def __init__(self, clsobj, num, check=True, time=True):
        assert (issubclass(clsobj, BinarySearchTree) and num > 0)
        super(BinarySearchTreeTest, self).__init__(clsobj, num, check, time)


if __name__ == '__main__':
    BinarySearchTreeTest(BinarySearchTree, 1000).testcase()
    print 'done'
