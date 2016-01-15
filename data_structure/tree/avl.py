# -*- coding: utf-8 -*-
# data structure: AVL (Georgy Adelson-Velsky and Evgenii Landis) tree

import bst, bst_test


class AVL(bst.BST):
    class Node:
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.factor = 0

    def __init__(self):
        self.root = None


if __name__ == '__main__':
    test = bst_test.BSTTest(AVL, 200)
    print 'done'
