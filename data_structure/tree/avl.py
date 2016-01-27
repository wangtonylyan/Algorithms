# -*- coding: utf-8 -*-
# data structure: AVL (Georgy Adelson-Velsky and Evgenii Landis) tree

import bst


class AVLTree(bst.BalancedBinarySearchTree):
    class Node(object):
        def __init__(self, key, value):
            self.left = None
            self.right = None
            self.key = key
            self.value = value
            self.factor = 0

    def __init__(self):
        super(AVLTree, self).__init__()


    def _check(self, avl, left, right):
        super(AVLTree, self)._check(avl, left, right)


if __name__ == '__main__':
    test = bst.BinarySearchTreeTest(AVLTree, 200)
    test.deleteMaxMin()
    test.delete()
    print 'done'
