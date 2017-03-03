# -*- coding: utf-8 -*-


from tests.data_structure.tree.tree import TreeTest
from algos.data_structure.tree.binary.bst import BinarySearchTree


class BinarySearchTreeTest(TreeTest):
    def __init__(self, cls=BinarySearchTree, args={}, num=1000, time=True, check=True):
        assert issubclass(cls, BinarySearchTree)
        super().__init__(cls, args, num, time)
        self.embed_check_method(BinarySearchTree, check)

    @staticmethod
    def check(self, size):
        assert self._len(self.root) == size

    @staticmethod
    def check_root(self, tree, left=0, right=0):
        if not tree:
            return 0
        # check symmetric order property
        assert not tree.left or tree.cmp(tree.left.key) < 0
        assert not tree.right or tree.cmp(tree.right.key) > 0
        return left + right + 1  # size

    @staticmethod
    def check_tree(self, tree):
        if not tree:
            return self.check_root(tree)
        # check size consistency
        left = self.check_tree(tree.left)
        right = self.check_tree(tree.right)
        assert self._len(tree) == left + right + 1
        return self.check_root(tree, left, right)

    def embed_check_method(self, cls, check):
        rename = lambda x: x + '_'
        check = 'check_tree' if check else 'check_root'

        def _iter_(self, tree, which, find, down=None, up=None):
            def wrapper(tree):
                tree = up(tree) if callable(up) and tree else tree
                getattr(self, check)(tree)
                return tree

            return getattr(self, rename('_iter_'))(tree, which, find, down, wrapper)

        def _recur_(self, tree, which, find, miss=None, down=None, up=None):
            def wrapper(tree):
                tree = up(tree) if callable(up) and tree else tree
                getattr(self, check)(tree)
                return tree

            return getattr(self, rename('_recur_'))(tree, which, find, miss, down, wrapper)

        for m in ['_iter_', '_recur_']:
            assert hasattr(cls, m)
            if not hasattr(cls, rename(m)):
                setattr(cls, rename(m), getattr(cls, m))
                setattr(cls, m, locals()[m])
        self.cls = type('_' + self.cls.__name__ + '_', (self.cls,),
                        {'check': self.__class__.check,
                         'check_tree': self.__class__.check_tree,
                         'check_root': self.__class__.check_root})


if __name__ == '__main__':
    BinarySearchTreeTest().main()
    print('done')
