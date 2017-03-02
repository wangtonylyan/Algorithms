# -*- coding: utf-8 -*-
# data structure: AA (Arne Andersson) tree
# AA树可被视为是一种简化版的"右倾"红黑树
# 每个节点中维护的level综合了AVL树和红黑树的特性


from algos.data_structure.tree.binary.bst import SelfBalancingBinarySearchTree


class AATree(SelfBalancingBinarySearchTree):
    class Node(SelfBalancingBinarySearchTree.Node):
        __slots__ = ['level']

        def __init__(self, key, value):
            super().__init__(key, value)
            self.level = 1

        def __str__(self):
            return super().__str__() + ', ' + f'level={str(self.level)}'

    # AA树与红黑树的区别：
    # 1) 插入和删除过程都没有top-down阶段的提前准备，仅需在bottom-up时重新平衡
    # 2) 由于'右倾'的特性，平衡算法就变得单调了，即skew+split的线性组合
    # 沿右子树的多次(单层上至多两次)skew操作首先将所有的左倾结构都转换成右倾
    # 沿右子树的多次(单层上至多两次)split操作再通过增加树的层次来消除多余的右倾

    # == rotate_right: turning 'tree.left.right' into left
    def _skew(self, tree):
        if tree.left and tree.left.level == tree.level:
            tree = self._rotate_right_(tree)
        return tree

    # == rotate_left + flip_color: increasing 'tree' level
    def _split(self, tree):
        if tree.right and tree.right.right and tree.right.right.level == tree.level:
            assert tree.level == tree.right.level == tree.right.right.level
            tree = self._rotate_left_(tree)
            tree.level += 1
        return tree

    def _balance(self, tree):
        # scenarios after insertion in one subtree:
        #          a             a
        #         / \             \
        # [left] b   c   [right]   b
        #                           \
        #                            c
        # scenarios after deletion in one subtree:
        #        a                 a
        #         \               /
        # [left]   b     [right] b
        #         / \             \
        #        c   d             c
        #         \   \
        #          e   f
        if not tree:
            return tree
        # 1) decrease 'tree' level as much as possible
        # actually it only matters during deletion in case that one subtree is lower
        m = min(tree.left.level if tree.left else 0, tree.right.level if tree.right else 0) + 1
        if tree.level > m:
            assert tree.level == m + 1
            tree.level = m
            if tree.right and tree.right.level > m:
                # 'tree' and 'tree.right' were viewed as a single pseudo-node
                tree.right.level = m
        # 2) skew+split combo along the right subtree
        tree = self._skew(tree)
        if tree.right:
            tree.right = self._skew(tree.right)
            if tree.right.right:
                tree.right.right = self._skew(tree.right.right)
        tree = self._split(tree)
        if tree.right:
            tree.right = self._split(tree.right)
        return tree
