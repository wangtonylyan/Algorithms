# -*- coding: utf-8 -*-

import time
import random
import platform
from test import Test


# abstract class
class Tree(object):
    class Node(object):
        __slots__ = ['key', 'value']

        def __init__(self, key, value):
            self.key = key
            self.value = value

    def __init__(self):
        super(Tree, self).__init__()
        self.root = None

    def __len__(self):
        assert (False)

    def search(self, *args):
        assert (False)

    def getMax(self, *args):
        assert (False)

    def getMin(self, *args):
        assert (False)

    def insert(self, *args):
        assert (False)

    def delete(self, *args):
        assert (False)

    def deleteMax(self, *args):
        assert (False)

    def deleteMin(self, *args):
        assert (False)

    def clean(self):
        self.root = None

    def check(self):
        assert (False)


class TreeTest(Test):
    def __init__(self, cls, args, num, check, timer):
        assert (issubclass(cls, Tree) and isinstance(args, dict) and num >= 0)
        super(TreeTest, self).__init__()
        self.cls = cls
        self.args = args
        self.cases = {}
        assert (0 <= num < 100000)
        if num > 0:
            for i in range(num):
                r = random.randint(0, 100000)
                self.cases[r] = r + 1
            print '=' * 50
            print "sample size:\t", len(self.cases)
        self.check = check
        if timer:
            if platform.system() == 'Windows':
                self.timer = time.clock
            else:
                self.timer = time.time
        else:
            self.timer = None

    def insert(self):
        print '-' * 50
        tree = self.cls(**self.args)
        cost = 0.0
        cnt = 0
        for i, j in self.cases.viewitems():
            if callable(self.timer):
                start_t = self.timer()
            tree.insert(i, j)
            if callable(self.timer):
                end_t = self.timer()
                cost += (end_t - start_t) * 1000
            if self.check:
                tree.check()
            assert (tree.search(i) == j)
            cnt += 1
            assert (cnt == len(tree))
        assert (cnt == len(tree) == len(self.cases))
        print 'insert:\t\t\t', cost
        return tree

    def deleteMaxMin(self):
        def test(tree, getFunc, delFunc):
            print '-' * 50
            cost = 0.0
            cnt = len(tree)
            while cnt > 0:
                m = getFunc()
                assert (isinstance(m, tuple) and len(m) == 2)
                if callable(self.timer):
                    start_t = self.timer()
                delFunc()
                if callable(self.timer):
                    end_t = self.timer()
                    cost += (end_t - start_t) * 1000
                if self.check:
                    tree.check()
                assert (tree.search(m[0]) is None)
                cnt -= 1
                assert (cnt == len(tree))
            assert (cnt == len(tree) == 0)
            print 'deleteMaxMin:\t', cost

        tree = self.insert()
        test(tree, tree.getMax, tree.deleteMax)
        tree = self.insert()
        test(tree, tree.getMin, tree.deleteMin)

    def delete(self):
        tree = self.insert()
        print '-' * 50
        cost = 0.0
        cnt = len(tree)
        for i, j in self.cases.viewitems():
            if callable(self.timer):
                start_t = self.timer()
            tree.delete(i)
            if callable(self.timer):
                end_t = self.timer()
                cost += (end_t - start_t) * 1000
            if self.check:
                tree.check()
            assert (tree.search(i) is None)
            cnt -= 1
            assert (cnt == len(tree))
        assert (cnt == len(tree) == 0)
        print 'delete:\t\t\t', cost

    def testcase(self):
        self._testcase()
        print 'pass:', self.cls

    def _testcase(self):
        self.deleteMaxMin()
        self.delete()
