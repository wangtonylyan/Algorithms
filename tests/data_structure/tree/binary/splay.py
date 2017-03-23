# -*- coding: utf-8 -*-


from tests.data_structure.tree.binary.bst import BinarySearchTreeTest
from algos.data_structure.tree.binary.splay import SplayTree, SplayTreeTopDown, SplayTreeBottomUp


class SplayTreeTest(BinarySearchTreeTest):
    def __init__(self, cls, args={}):
        assert issubclass(cls, SplayTree)
        super().__init__(cls, args)

    def embed_check_method(self, check, rename):
        def _splay_(self, tree, key):
            tree = getattr(self, rename('_splay_'))(tree, key)
            getattr(self, check)(tree)
            return tree

        def _splay_max_(self, tree):
            tree = getattr(self, rename('_splay_max_'))(tree)
            getattr(self, check)(tree)
            return tree

        def _splay_min_(self, tree):
            tree = getattr(self, rename('_splay_min_'))(tree)
            getattr(self, check)(tree)
            return tree

        base = self.cls
        for m in ['_splay_', '_splay_max_', '_splay_min_']:
            assert hasattr(base, m)
            if not hasattr(base, rename(m)):
                setattr(base, rename(m), getattr(base, m))
                setattr(base, m, locals()[m])
        self.cls = type('_' + self.cls.__name__ + '_', (self.cls,),
                        {'check': self.__class__.check,
                         'check_tree': self.__class__.check_tree,
                         'check_root': self.__class__.check_root})


if __name__ == '__main__':
    SplayTreeTest(SplayTreeTopDown).main()
    SplayTreeTest(SplayTreeBottomUp).main()
    print('done')
