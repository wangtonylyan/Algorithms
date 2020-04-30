# -*- coding: utf-8 -*-
# data structure: binary search tree

if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))


from algorithms.utility import *
from data_structure.tree.tree import Tree


class BinarySearchTree(Tree):
    class Node(Tree.Node):
        __slots__ = ['left', 'right']

        def __init__(self, key, value):
            super().__init__(key, value)
            self.left = None
            self.right = None

        def __str__(self):
            return super().__str__() + ', ' + \
                f'left={str(self.left.key) if self.left else None}' + ', ' + \
                f'right={str(self.right.key) if self.right else None}'

        def cmp(self, key):
            return -1 if key < self.key else 1 if key > self.key else 0

    def __len__(self):
        return self._len_(self.root)

    def __str__(self):  # TODO: traverse
        return str(self.root)

    def search(self, key):
        assert key
        tree = self._search_(self.root, key)
        return tree.value if tree else None

    def getmax(self):
        tree = self._getmax_(self.root)
        return (tree.key, tree.value) if tree else None

    def getmin(self):
        tree = self._getmin_(self.root)
        return (tree.key, tree.value) if tree else None

    def insert(self, key, value):
        assert key
        self.root = self._insert_(self.root, key, value)

    def delete(self, key):
        assert key
        self.root = self._delete_(self.root, key)

    def delmax(self):
        self.root = self._delmax_(self.root)

    def delmin(self):
        self.root = self._delmin_(self.root)

    @classmethod
    def _len_(cls, tree):
        return len(cls.preorder(tree))

    @classmethod
    def _search_(cls, tree, key):
        return cls.walk(tree, lambda tree: tree.cmp(key))

    @classmethod
    def _getmax_(cls, tree):
        return cls.walk(tree, lambda tree: 1 if tree.right else 0)

    @classmethod
    def _getmin_(cls, tree):
        return cls.walk(tree, lambda tree: -1 if tree.left else 0)

    @classmethod
    def _insert_(cls, tree, key, value):
        return cls.rwalk(tree,
                         lambda tree: tree.cmp(key),
                         lambda tree: tree.set(value=value),
                         lambda: cls.Node(key, value))

    @classmethod
    def _delete_(cls, tree, key):
        def delete(tree):
            if not tree.left:
                return tree.right
            if not tree.right:
                return tree.left
            m = cls._getmax_(tree.left)
            tree.key = m.key
            tree.value = m.value
            tree.left = cls._delmax_(tree.left)
            return tree
        return cls.rwalk(tree, lambda tree: tree.cmp(key), delete)

    @classmethod
    def _delmax_(cls, tree):
        return cls.rwalk(tree,
                         lambda tree: 1 if tree.right else 0,
                         lambda tree: tree.left)

    @classmethod
    def _delmin_(cls, tree):
        return cls.rwalk(tree,
                         lambda tree: -1 if tree.left else 0,
                         lambda tree: tree.right)

    ## iterative walk
    @classmethod
    def walk(cls, tree, which, find=identity, *, down=None):
        while tree:
            if callable(down):
                tree = down(tree)
            cmp = which(tree)
            if cmp < 0:
                tree = tree.left
            elif cmp > 0:
                tree = tree.right
            else:
                tree = find(tree)
                break
        return tree

    ## recursive walk
    @classmethod
    def rwalk(cls, tree, which, find=identity, miss=None, *, down=None, up=None):
        if not tree:
            if callable(miss):
                tree = miss()
            return tree
        # 1) top-down
        if callable(down):
            tree = down(tree)
        # 2) recursion
        cmp = which(tree)
        if cmp < 0:
            tree.left = cls.rwalk(tree.left, which, find, miss, down=down, up=up)
        elif cmp > 0:
            tree.right = cls.rwalk(tree.right, which, find, miss, down=down, up=up)
        else:
            tree = find(tree)
        # 3) bottom-up
        if tree and callable(up):
            tree = up(tree)
        return tree

    ## recursive traverse
    @classmethod
    def preorder(cls, tree, find=identity):
        return [find(tree)] + cls.preorder(tree.left) + \
            cls.preorder(tree.right) if tree else []

    @classmethod
    def inorder(cls, tree, find=identity):
        return cls.inorder(tree.left) + [find(tree)] + \
            cls.inorder(tree.right) if tree else []

    @classmethod
    def postorder(cls, tree, find=identity):
        return cls.postorder(tree.left) + cls.postorder(tree.right) + \
            [find(tree)] if tree else []


class SelfAdjustingBST(BinarySearchTree):
    @classmethod
    def rotateleft(cls, tree):
        assert tree and tree.right
        return cls._rotateleft_(tree)

    @classmethod
    def rotateright(cls, tree):
        assert tree and tree.left
        return cls._rotateright_(tree)

    # 1) rotate left与rotate right这两个操作是完全对称且互为可逆的
    # 2) always holds the symmetric order property
    @staticmethod
    def _rotateleft_(tree):
        right = tree.right
        tree.right = right.left
        right.left = tree
        return right

    @staticmethod
    def _rotateright_(tree):
        left = tree.left
        tree.left = left.right
        left.right = tree
        return left


# (自)平衡树大致分为两类：height-balanced和weight-balanced
# 前者关注的是树的高度，后者关注的是树的重量(即树中节点的个数)
class SelfBalancingBST(SelfAdjustingBST):
    @classmethod
    def balance(cls, *args, **kwargs):
        assert False

    @classmethod
    def rwalk(cls, *args, **kwargs):
        if 'up' not in kwargs:
            kwargs['up'] = cls.balance
        return super().rwalk(*args, **kwargs)


if __name__ == '__main__':
    bst = BinarySearchTree()
    # bst = SelfBalancingBST()
    bst.insert(1, 2)
    bst.insert(2, 3)
    bst.insert(3, 4)
    bst.insert(4, 5)
    print(str(bst))
    print(len(bst))
    bst.delete(1)
    print(len(bst))

    print(len([None]))



# 二叉树遍历题：

# 1. 遍历

# 1.1. 镜像二叉树


# 2. 给出遍历的结果，反推二叉树

# 2.1. 给出不同的遍历结果，检查是否对应于同一课树，
# 是否构成一棵二叉树
