# -*- coding: utf-8 -*-
# data structure: AA (Arne Andersson) tree

import bst

# invariant:
# 1) the level of a leaf node is one
# 2) the level of a left child is strictly less than that of its parent
# 3) the level of a right child is less than or equal to that of its parent
# 4) the level of a right grandchild is strictly less than that of its grandparent
# 5) every node of level greater than one must have two children

class AAT(bst.BST):
    class Node:
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.level = False

    def __init__(self):
        self.root = None

    def check(self):
        pass


if __name__ == '__main__':
    test = bst.BSTTest(AAT, 1000)
    print 'done'
