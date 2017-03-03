# -*- coding: utf-8 -*-
# data structure: AVL (Georgy Adelson-Velsky and Evgenii Landis) tree


from algos.data_structure.tree.binary.bst import SelfBalancingBinarySearchTree


class AVLTree(SelfBalancingBinarySearchTree):
    class Node(SelfBalancingBinarySearchTree.Node):
        __slots__ = ['factor']

        def __init__(self, key, value):
            super().__init__(key, value)
            # 有两种实现上的策略
            # 1) 维护balance信息，即左右子树的高度差，在平衡树的过程中。随着增删节点、左右旋转操作同步地调整该值
            self.factor = 0  # balance factor = tree.right.height - tree.left.height
            # 2) 维护height信息，即以当前节点为根节点的子树的高度，平衡树的过程中需要实时计算balance信息
            # 前者的优点是树的平衡被破坏后，只需重新维护局部子树中的信息，而后者需要沿遍历路径向上维护至整棵树的根节点
            # 后者的优点是使得统计树高度操作的时间复杂度变成了O(1)
            # self.height = 0

        def __str__(self):
            return super().__str__() + ', ' + f'factor={str(self.factor)}'

    def _rotate_left(self, tree):
        assert tree and tree.right
        tree = self._rotate_left_(tree)
        tree.factor -= 1
        tree.left.factor -= 1
        return tree

    def _rotate_right(self, tree):
        assert tree and tree.left
        tree = self._rotate_right_(tree)
        tree.factor = 1
        tree.right.factor += 1
        return tree

    def _balance(self, tree):
        if tree:
            pass
        return tree
