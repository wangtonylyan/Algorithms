# -*- coding: utf-8 -*-


import random, timeit
from algos.data_structure.tree.tree import Tree


class TreeTest:
    def __init__(self, cls, args, num, time):
        assert issubclass(cls, Tree) and isinstance(args, dict) and num > 0
        self.cls = cls
        self.args = args
        self.num = num
        self.time = time

    def _create_cases(self):
        cases = {}
        for i in range(self.num):
            rand = random.randint(0, self.num * 100)
            cases[rand] = rand + 1
        return cases

    def _create_tree(self):
        return self.cls(*self.args)

    def _run_cases(self, cases, before, main, after, finish):
        for k, v in cases.items():
            r = before(k, v)
            assert r is not None
            main(k, v)
            r = after(k, v, r)
            assert r is not None
        finish()

    def insert(self):
        cases = self._create_cases()
        tree = self._create_tree()
        self._insert(tree, cases)

    def _insert(self, tree, cases):
        self._run_cases(cases,
                        before=lambda k, v: v if tree.search(k) is None else None,
                        main=lambda k, v: tree.insert(k, v),
                        after=lambda k, v, *_: v if tree.search(k) == v else None,
                        finish=lambda: tree.check(len(cases)))
        print('insert:', len(cases))

    def delete(self):
        cases = self._create_cases()
        tree = self._create_tree()
        self._insert(tree, cases)
        self._run_cases(cases,
                        before=lambda k, v: v if tree.search(k) == v else None,
                        main=lambda k, v: tree.delete(k),
                        after=lambda k, v, *_: v if tree.search(k) is None else None,
                        finish=lambda: tree.check(0))
        print('delete:', len(cases))

    def delmax(self):
        self._delmaxmin('getmax', 'delmax', lambda r, m: r < m)

    def delmin(self):
        self._delmaxmin('getmin', 'delmin', lambda r, m: r > m)

    def _delmaxmin(self, get, dlt, cmp):
        def after(k, v, m, *_):
            r = getattr(tree, get)()
            return m if r is None or cmp(r, m) else None

        cases = self._create_cases()
        tree = self._create_tree()
        self._insert(tree, cases)
        self._run_cases(cases,
                        before=lambda k, v: getattr(tree, get)(),
                        main=lambda k, v: getattr(tree, dlt)(),
                        after=after,
                        finish=lambda: tree.check(0))
        print(dlt + ':', len(cases))

    def main(self):
        print('=' * 30)
        print(self.cls.__name__)
        for f in [self.delete, self.delmax, self.delmin]:
            print('-' * 30)
            f()
        print('=' * 30)
