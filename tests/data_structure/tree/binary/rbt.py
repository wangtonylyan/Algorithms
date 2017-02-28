# -*- coding: utf-8 -*-


from tests.data_structure.tree.binary.bst import BinarySearchTreeTest
from algos.data_structure.tree.binary.rbt import RedBlackTree


class RedBlackTreeTest(BinarySearchTreeTest):
    def __init__(self, cls=RedBlackTree, args={}, num=1000, time=True, check=True):
        assert issubclass(cls, RedBlackTree)
        super().__init__(cls, args, num, time, check)

    @staticmethod
    def check(self, size):
        # BinarySearchTreeTest.check(self, size)
        assert not (root and root.color)

    @staticmethod
    def check_root(self, tree, left=0, right=0):
        # BinarySearchTreeTest.check_root(self, tree, left, right)
        if not tree:
            return 0
        # the following assertions cover the same cases as the black-height invariant, just for illustration
        assert not (tree.left and tree.left.color and tree.right and tree.right.color)
        assert not (not tree.left and tree.right and not tree.right.color)
        assert not (not tree.right and tree.left and not tree.left.color)
        # black-height invariant: the left and right subtree should hold the same black-height.
        assert left == right
        # Because this check method is called after each balance operation
        # and the 'tree' node will probably be modified by the next balance,
        # the meaning of the return value is not as intuitive as it appears to be.
        # First, due to the invariant that black-height is preserved in rotation operation,
        # the black-height of 'tree' is added by at most 1 only after its color has been flipped.
        # Therefore, if a red 'tree' doesn't count into the black-height for the first time,
        # after the next balance, if its parent is flipped, considering the most complicated scenario,
        # the 'tree' and its parent must then be black resulting in the increase of
        # the black-height of the parent, which takes both of them into count.
        # Second, whenever a new leaf is inserted as its parent's only child, its black-height should be 0,
        # otherwise the black-height of the left and right subtree of its parent would be 0 and 1.
        return left if tree.color else left + 1  # black-height

    @staticmethod
    def check_tree(self, tree):
        if not tree:
            return self.check_root(tree)
        # check size consistency
        left = self.check_tree(tree.left)
        right = self.check_tree(tree.right)
        return self.check_root(tree, left, right)


if __name__ == '__main__':
    bst = RedBlackTreeTest()
    bst = bst.cls()
    print(dir(bst))
    for i in range(10):
        bst.insert(1, 'ha' + str(i))

    print(len(bst))

    #    for i in range(10):
    #        bst.delmax()
    print(len(bst))

    print('done')
