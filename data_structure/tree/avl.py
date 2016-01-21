# -*- coding: utf-8 -*-
# data structure: AVL (Georgy Adelson-Velsky and Evgenii Landis) tree

import bst


class AVL(bst.BBST):
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.factor = 0

    def __init__(self):
        self.root = None


if __name__ == '__main__':
    test = bst.BSTTest(AVL, 200)
    test.deleteMaxMin()
    test.delete()
    print 'done'
