# -*- coding: utf-8 -*-
# data structure: red-black tree
# 红黑树属于2-3(-4)树的一种变种


from algos.data_structure.tree.binary.bst import SelfBalancingBinarySearchTree


class RedBlackTree(SelfBalancingBinarySearchTree):
    class Node(SelfBalancingBinarySearchTree.Node):
        __slots__ = ['color']

        def __init__(self, key, value):
            super().__init__(key, value)
            # True if red else (black) False
            self.color = True  # default color of a new leaf node is red

        def __str__(self):
            return super().__str__() + ', ' + f'color={str(self.color)}'

    # 1) top-down: naturally no 4-node
    # 2) recursion: insert or override
    # 3) bottom-up: rebalance
    def insert(self, key, value):
        assert key is not None
        self.root = self._insert(self.root, key, value)
        if self.root.color:
            self.root.color = False

    def _apply_del_func(self, func, *args, **kwargs):
        if self.root:
            # make sure that 'root' isn't a 2-node before recursion
            if not (self.root.left and self.root.left.color) and not (self.root.right and self.root.right.color):
                self.root.color = True
            self.root = func(self.root, *args, **kwargs)
            if self.root and self.root.color:
                self.root.color = False

    def delete(self, key):
        assert key is not None
        self._apply_del_func(self._delete, key)

    def delmax(self):
        self._apply_del_func(self._delmax)

    def delmin(self):
        self._apply_del_func(self._delmin)

    # 1) top-down: make 'tree.left' or 'tree.right' a 3-node
    # 2) recursion: delete or fail
    # 3) buttom-up: rebalance
    def _delete(self, tree, key):
        def find(tree):
            if not tree.left:
                if tree.right:
                    tree.right.color = tree.color
                return tree.right  # delete without necessity of rebalancing
            if not tree.right:
                if tree.left:
                    tree.left.color = tree.color
                return tree.left
            # 用左子树中的最大节点或右子树中的最小节点来替换要被删除的目标节点：_delmax(tree.left) vs. _delmin(tree.right)
            # 两种策略的实现方式是完全对称的，但对于LLRB树而言，由于其左倾的特性，选择后者效率会略高
            tree = self._make_right_red(tree)
            if key != tree.key:  # if 'tree' node is no longer the one before _make_right_red()
                tree.right = self._delete(tree.right, key)  # continue traversing
            else:
                m = self._getmin(tree.right)
                tree.key = m.key
                tree.value = m.value
                tree.right = self._delmin(tree.right)  # delete
            return tree

        def down(tree):
            cmp = tree.cmp(key)
            if cmp < 0:
                tree = self._make_left_red(tree)
            elif cmp > 0:
                tree = self._make_right_red(tree)
            return tree

        return self._recur_(tree, which=lambda tree: tree.cmp(key), find=find, down=down)

    def _delmax(self, tree):
        def find(tree):
            if tree.left:
                tree.left.color = tree.color
            return tree.left

        return self._recur_(tree, which=lambda tree: 1 if tree.right else 0, find=find, down=self._make_right_red)

    def _delmin(self, tree):
        def find(tree):
            if tree.right:
                tree.right.color = tree.color
            return tree.right

        return self._recur_(tree, which=lambda tree: -1 if tree.left else 0, find=find, down=self._make_left_red)

    # 1) rotate left：no side-effect
    # 2) rotate right：no side-effect
    # 3) flip color：increase or decrease tree's height by one

    # @invariant: 'tree' is a red-black tree
    def _rotate_left(self, tree):
        assert tree and tree.right
        tree = self._rotate_left_(tree)
        # concerning the augment
        tree.color, tree.left.color = tree.left.color, tree.color
        return tree

    def _rotate_right(self, tree):
        assert tree and tree.left
        tree = self._rotate_right_(tree)
        tree.color, tree.right.color = tree.right.color, tree.color
        return tree

    # @invariant: 'tree' is a relaxed red-black tree
    # @what: turn 'tree' from a 2-node into a 4-node, or reversely
    def _flip_color(self, tree):
        assert tree and tree.left and tree.right
        tree.left.color = not tree.left.color
        tree.right.color = not tree.right.color
        tree.color = not tree.color
        return tree

    # @premise: at most one of 'tree', 'tree.left' and 'tree.right' is a 4-node
    # @what: eliminate 4-node, resulting in the balance of 'tree'
    def _balance(self, tree):
        if not tree:
            return tree
        if tree.left and tree.left.color:
            if tree.left.right and tree.left.right.color:
                tree.left = self._rotate_left(tree.left)
            if tree.left.left and tree.left.left.color:
                tree = self._rotate_right(tree)
        elif tree.right and tree.right.color:
            if tree.right.left and tree.right.left.color:
                tree.right = self._rotate_right(tree.right)
            if tree.right.right and tree.right.right.color:
                tree = self._rotate_left(tree)
        if tree.left and tree.left.color and tree.right and tree.right.color:
            tree = self._flip_color(tree)
        return tree

    # @premise: 'tree' is a 3-node
    # @invariant: 'tree.right' is a balanced red-black tree, which will be neither traversed nor rebalanced after return
    # @what: turn 'tree.left' into a 3-node
    # @how: move red from 'tree' or 'tree.right' node to 'tree.left' node
    # @when: before traversal of the 'tree.left' subtree
    def _make_left_red(self, tree):
        if not tree or not tree.left:
            return tree
        assert tree.color or tree.left.color or (tree.right and tree.right.color)
        if tree.left.color or \
                (tree.left.left and tree.left.left.color) or \
                (tree.left.right and tree.left.right.color):
            return tree
        assert tree.right  # black-height invariant
        if tree.color:
            tree = self._flip_color(tree)  # move red from 'tree' node to its children
            if tree.right.left and tree.right.left.color:  # 'tree.right' subtree is no longer balanced
                tree.right = self._rotate_right(tree.right)
            if tree.right.right and tree.right.right.color:
                tree = self._rotate_left(tree)
                tree = self._flip_color(tree)
        else:
            assert tree.right.color
            tree = self._rotate_left(tree)  # move red from 'tree.right' node to 'tree.left' node
        assert tree.left.color or \
               (tree.left.left and tree.left.left.color) or \
               (tree.left.right and tree.left.right.color)
        return tree

    def _make_right_red(self, tree):
        if not tree or not tree.right:
            return tree
        assert tree.color or tree.right.color or (tree.left and tree.left.color)
        if tree.right.color or \
                (tree.right.left and tree.right.left.color) or \
                (tree.right.right and tree.right.right.color):
            return tree
        assert tree.left
        if tree.color:
            tree = self._flip_color(tree)
            if tree.left.right and tree.left.right.color:
                tree.left = self._rotate_left(tree.left)
            if tree.left.left and tree.left.left.color:
                tree = self._rotate_right(tree)
                tree = self._flip_color(tree)
        else:
            assert tree.left.color
            tree = self._rotate_right(tree)
        assert tree.right.color or \
               (tree.right.left and tree.right.left.color) or \
               (tree.right.right and tree.right.right.color)
        return tree
