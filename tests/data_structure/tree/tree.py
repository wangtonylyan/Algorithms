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
            r1 = before(k, v)
            r2 = main(k, v)
            after(k, v, r1, r2)
        finish()

    def insert(self):
        cases = self._create_cases()
        tree = self._create_tree()
        self._insert(tree, cases)

    def _insert(self, tree, cases):
        self._run_cases(cases,
                        before=lambda k, v: tree.search(k) is None,
                        main=lambda k, v: tree.insert(k, v),
                        after=lambda k, v, *_: tree.search(k) == v,
                        finish=lambda: tree.check(len(cases)))

    def delete(self):
        cases = self._create_cases()
        tree = self._create_tree()
        self._insert(tree, cases)
        self._run_cases(cases,
                        before=lambda k, v: tree.search(k) == v,
                        main=lambda k, v: tree.delete(k),
                        after=lambda k, v, *_: tree.search(k) is None,
                        finish=lambda: tree.check(0))

    def delmax(self):
        self._delmaxmin('getmax', 'delmax')

    def delmin(self):
        self._delmaxmin('getmin', 'delmin')

    def _delmaxmin(self, get, dlt):
        cases = self._create_cases()
        tree = self._create_tree()
        self._insert(tree, cases)
        self._run_cases(cases,
                        before=lambda k, v: getattr(tree, get)(),
                        main=lambda k, v: getattr(tree, dlt)(),
                        after=lambda k, v, m, *_: getattr(tree, get)() == m,
                        finish=lambda: tree.check(0))

    def main(self):
        self.delete()
        self.delmax()
        self.delmin()
