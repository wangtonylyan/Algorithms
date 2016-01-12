# -*- coding: utf-8 -*-
# data structure: red-black tree

import bst


class RBT(bst.BST):
    class Node:
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.color = False

    def __init__(self):
        self.root = None


if __name__ == '__main__':
    test = bst.BSTTest(RBT, 200)
    print 'done'
