# -*- coding: utf-8 -*-

import time, random, platform


# interface
class Tree(object):
    class Node(object):
        __slots__ = ['key', 'value']

        def __init__(self, key, value):
            self.key = key
            self.value = value

    def __init__(self):
        super(Tree, self).__init__()

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
        assert (False)

    def check(self):
        assert (False)


class TreeTest(object):
    def __init__(self, clsobj, num, check, timer):
        super(TreeTest, self).__init__()
        assert (issubclass(clsobj, Tree))
        self.tcls = clsobj
        self.dic = {}
        assert (0 <= num < 100000)
        if num > 0:
            for i in range(num):
                r = random.randint(0, 100000)
                self.dic[r] = r + 1
            print "sample size:\t", len(self.dic)
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
        tree = self.tcls()
        cost = 0.0
        cnt = 0
        for i, j in self.dic.viewitems():
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
        assert (cnt == len(tree) == len(self.dic))
        print 'insert:\t\t\t', cost
        return tree

    def deleteMaxMin(self):
        def test(tree, getFunc, delFunc):
            print '-' * 50
            cost = 0.0
            cnt = len(tree)
            while cnt > 0:
                m = getFunc()
                if callable(self.timer):
                    start_t = self.timer()
                delFunc()
                if callable(self.timer):
                    end_t = self.timer()
                    cost += (end_t - start_t) * 1000
                if self.check:
                    tree.check()
                assert (tree.search(m.key) == None)
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
        for i, j in self.dic.viewitems():
            if callable(self.timer):
                start_t = self.timer()
            tree.delete(i)
            if callable(self.timer):
                end_t = self.timer()
                cost += (end_t - start_t) * 1000
            if self.check:
                tree.check()
            assert (tree.search(i) == None)
            cnt -= 1
            assert (cnt == len(tree))
        assert (cnt == len(tree) == 0)
        print 'delete:\t\t\t', cost

    def testcase(self):
        self.deleteMaxMin()
        self.delete()
