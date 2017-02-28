# -*- coding: utf-8 -*-
# data structure: binary search tree


from algos.data_structure.tree.tree import Tree


class BinarySearchTree(Tree):
    class Node(Tree.Node):
        __slots__ = ['left', 'right']

        def __init__(self, key, value, left=None, right=None):
            super().__init__(key, value)
            self.left = left
            self.right = right

    def __init__(self):
        super().__init__()

    def __len__(self):
        return self._len(self.root)

    def search(self, key):
        assert key is not None
        tree = self._search(self.root, key)
        return tree.value if tree else None

    def getmax(self):
        tree = self._getmax(self.root)
        return (tree.key, tree.value) if tree else None

    def getmin(self):
        tree = self._getmin(self.root)
        return (tree.key, tree.value) if tree else None

    def insert(self, key, value):
        assert key is not None
        self.root = self._insert(self.root, key, value)

    def delete(self, key):
        assert key is not None
        self.root = self._delete(self.root, key)

    def delmax(self):
        self.root = self._delmax(self.root)

    def delmin(self):
        self.root = self._delmin(self.root)

    def _len(self, tree):
        return self._len(tree.left) + self._len(tree.right) + 1 if tree else 0

    def _search(self, tree, key):
        return self._iter_(tree,
                           which=lambda tree: tree.left if tree.cmp(key) < 0 else tree.right,
                           find=lambda tree: tree.cmp(key) == 0)

    def _getmax(self, tree):
        return self._iter_(tree,
                           which=lambda tree: tree.right,
                           find=lambda tree: not tree.right)

    def _getmin(self, tree):
        return self._iter_(tree,
                           which=lambda tree: tree.left,
                           find=lambda tree: not tree.left)

    def _insert(self, tree, key, value):
        return self._recur_(tree,
                            which=lambda tree: tree.cmp(key),
                            find=lambda tree: self.__class__.Node(tree.key, value, tree.left, tree.right),
                            miss=lambda: self.__class__.Node(key, value))

    def _delete(self, tree, key):
        def find(tree):
            if not tree.left:
                return tree.right
            if not tree.right:
                return tree.left
            m = self._getmax(tree.left)
            tree.key = m.key
            tree.value = m.value
            tree.left = self._delmax(tree.left)
            return tree

        return self._recur_(tree,
                            which=lambda tree: tree.cmp(key),
                            find=find)

    def _delmax(self, tree):
        return self._recur_(tree,
                            which=lambda tree: 1 if tree.right else 0,
                            find=lambda tree: tree.left)

    def _delmin(self, tree):
        return self._recur_(tree,
                            which=lambda tree: -1 if tree.left else 0,
                            find=lambda tree: tree.right)

    def _iter_(self, tree, which, find, down=None, up=None):
        # 2) iteration: traversal
        while tree:
            # 1) top-down
            tree = down(tree) if callable(down) else tree
            if find(tree):
                # 3) bottom-up
                tree = up(tree) if callable(up) else tree
                break
            tree = which(tree)
        return tree

    def _recur_(self, tree, which, find, miss=None, down=None, up=None):
        if tree:
            # 1) top-down
            tree = down(tree) if callable(down) else tree
            # 2) recursion: traversal
            cmp = which(tree)
            if cmp < 0:
                tree.left = self._recur_(tree.left, which, find, miss, down, up)
            elif cmp > 0:
                tree.right = self._recur_(tree.right, which, find, miss, down, up)
            else:
                tree = find(tree)
            # 3) bottom-up
            tree = up(tree) if callable(up) else tree
        else:
            tree = miss() if callable(miss) else tree
        return tree


class SelfAdjustingBinarySearchTree(BinarySearchTree):
    def __init__(self):
        super().__init__()

    def _rotate_left(self, tree):
        if tree and tree.right:
            tree = self._rotate_left_(tree)
        return tree

    def _rotate_right(self, tree):
        if tree and tree.left:
            tree = self._rotate_right_(tree)
        return tree

    # 1) rotate left与rotate right这两个操作是完全对称且互为可逆的
    # 2) always holds the symmetric order property
    def _rotate_left_(self, tree):
        right = tree.right
        tree.right = right.left
        right.left = tree
        return right

    def _rotate_right_(self, tree):
        left = tree.left
        tree.left = left.right
        left.right = tree
        return left


# (自)平衡树大致分为两类：height-balanced和weight-balanced
# 前者关注的是树的高度，后者关注的是树的重量(即树中节点的个数)
class SelfBalancingBinarySearchTree(SelfAdjustingBinarySearchTree):
    def __init__(self):
        super().__init__()

    def _balance(*args):
        assert False
