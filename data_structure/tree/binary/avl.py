# -*- coding: utf-8 -*-
# data structure: AVL (Georgy Adelson-Velsky and Evgenii Landis) tree

from bst import SelfBalancingBinarySearchTree, BinarySearchTreeTest


class AVLTree(SelfBalancingBinarySearchTree):
    class Node(SelfBalancingBinarySearchTree.Node):
        __slots__ = ['factor']

        def __init__(self, key, value):
            super(AVLTree.Node, self).__init__(key, value)
            self.factor = 0

    def __init__(self):
        super(AVLTree, self).__init__()

    def _check(self, avl, left, right):
        return super(AVLTree, self)._check(avl, left, right)


if __name__ == '__main__':
    BinarySearchTreeTest(AVLTree, 200).testcase()
    print 'done'