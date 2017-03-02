# -*- coding: utf-8 -*-


from tests.data_structure.tree.binary.bst import BinarySearchTreeTest
from algos.data_structure.tree.binary.aat import AATree


class AATreeTest(BinarySearchTreeTest):
    def __init__(self, cls=AATree, args={}):
        assert issubclass(cls, AATree)
        super().__init__(cls, args)

    @staticmethod
    def check_root(self, tree, left=0, right=0):
        if tree:
            if tree.left:
                # level of a left child is strictly less than that of its parent
                assert tree.left.level < tree.level
            if tree.right:
                # level of a right child is less than or equal to that of its parent
                assert tree.right.level <= tree.level
                if tree.right.right:
                    # level of a right grandchild is strictly less than that of its grandparent
                    assert tree.right.right.level < tree.level
            if not tree.left and not tree.right:
                # level of a leaf node is one
                assert tree.level == 1
            if tree.level > 1:
                # 隐式特征: every node of level greater than one must have two children
                assert tree.left and tree.right
        # 无需像红黑树那样统计左右子树的高度，因为level就已经对其约束了
        return BinarySearchTreeTest.check_root(self, tree, left, right)


if __name__ == '__main__':
    AATreeTest().main()
    print('done')
