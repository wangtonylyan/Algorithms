# -*- coding: utf-8 -*-
# data structure: binary search tree

import bst_test


class BST(object):
    class Node:
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        def _recur(bst, key, value):
            if bst == None:
                return self.__class__.Node(key, value)
            if key < bst.key:
                bst.left = _recur(bst.left, key, value)
            elif key > bst.key:
                bst.right = _recur(bst.right, key, value)
            else:
                bst.value = value
            return bst

        self.root = _recur(self.root, key, value)

    def deleteMin(self):
        if self.root == None:
            return
        elif self.root.left == None:
            self.root = self.root.right
            return
        it = self.root
        while it.left.left:
            it = it.left
        it.left = it.left.right

    def deleteMax(self):
        if self.root == None:
            return
        elif self.root.right == None:
            self.root = self.root.left
            return
        it = self.root
        while it.right.right:
            it = it.right
        it.right = it.right.left

    def delete(self, key):
        def _recur(bst, key):
            if bst == None:
                return None
            if key < bst.key:
                bst.left = _recur(bst.left, key)
            elif key > bst.key:
                bst.right = _recur(bst.right, key)
            else:  # bst就是需要被删除的节点
                if bst.left == None:
                    bst = bst.right
                elif bst.right == None:
                    bst = bst.left
                else:  # 将bst节点替换为其左子树中的最大节点或右子树中的最小节点
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

        self.root = _recur(self.root, key)

    def search(self, key):
        return self._search(self.root, key)

    @staticmethod
    def _search(bst, key):
        it = bst
        while it:
            if key < it.key:
                it = it.left
            elif key > it.key:
                it = it.right
            else:
                break
        return it.value if it else None

    def getMax(self):
        return self._getMax(self.root)

    @staticmethod
    def _getMax(bst):
        it = bst
        while it and it.right:
            it = it.right
        return it

    def getMin(self):
        return self._getMin(self.root)

    @staticmethod
    def _getMin(bst):
        it = bst
        while it and it.left:
            it = it.left
        return it

    def size(self):
        def _recur(bst):
            if bst == None:
                return 0
            return _recur(bst.left) + _recur(bst.right) + 1

        return _recur(self.root)

    def clean(self):
        self.root = None

    def check(self):
        def _recur(bst):
            if bst == None:
                return
            _recur(bst.left)
            _recur(bst.right)
            if bst.left:
                assert (bst.left.value < bst.value)
            if bst.right:
                assert (bst.right.value > bst.value)

        _recur(self.root)


if __name__ == '__main__':
    test = bst_test.BSTTest(BST, 1000)
    test.deleteMaxMin()
    test.delete()
    print 'done'
