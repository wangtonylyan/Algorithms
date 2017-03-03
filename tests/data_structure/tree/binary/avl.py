# -*- coding: utf-8 -*-


from tests.data_structure.tree.binary.bst import BinarySearchTreeTest
from algos.data_structure.tree.binary.avl import AVLTree


class AVLTreeTest(BinarySearchTreeTest):
    def __init__(self, cls=AVLTree, args={}):
        assert issubclass(cls, AVLTree)
        super().__init__(cls, args)

    @staticmethod
    def check_root(self, tree, left=0, right=0):
        if tree:
            assert tree.factor in [-1, 0, 1]
        return BinarySearchTreeTest.check_root(self, tree, left, right)


if __name__ == '__main__':
    AVLTreeTest().main()
    print('done')
