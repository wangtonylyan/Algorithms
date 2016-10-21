# -*- coding: utf-8 -*-
# data structure: size balanced tree

from bst import SelfBalancingBinarySearchTree, BinarySearchTreeTest


class SizeBalancedTree(SelfBalancingBinarySearchTree):
    class Node(SelfBalancingBinarySearchTree.Node):
        __slots__ = ['size']

        def __init__(self, key, value):
            super(SizeBalancedTree.Node, self).__init__(key, value)
            self.size = 0

    def __init__(self):
        super(SizeBalancedTree, self).__init__()


if __name__ == '__main__':
    BinarySearchTreeTest(SizeBalancedTree).testcase()
    print 'done'
