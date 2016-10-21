# -*- coding: utf-8 -*-
# data structure: AVL (Georgy Adelson-Velsky and Evgenii Landis) tree

from bst import SelfBalancingBinarySearchTree, BinarySearchTreeTest


class AVLTree(SelfBalancingBinarySearchTree):
    class Node(SelfBalancingBinarySearchTree.Node):
        __slots__ = ['factor']

        def __init__(self, key, value):
            super(AVLTree.Node, self).__init__(key, value)
            self.factor = 0  # balance factor

    def __init__(self):
        super(AVLTree, self).__init__()

    def _rotateLeft(self, avl):
        avl = super(AVLTree, self)._rotateLeft(avl)
        avl.factor -= 1
        avl.right.factor += 1
        return avl

    def _rotateRight(self, avl):
        avl = super(AVLTree, self)._rotateRight(avl)
        avl.factor += 1
        avl.left.factor -= 1
        return avl

    def _balance(self, avl):
        assert (avl)
        return avl

    def _check(self, avl, left, right):
        if avl:
            assert (avl.factor in [-1, 0, 1])
        return super(AVLTree, self)._check(avl, left, right)


if __name__ == '__main__':
    BinarySearchTreeTest(AVLTree).testcase()
    print 'done'
