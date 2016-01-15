# -*- coding: utf-8 -*-

import time, random, bst


class BSTTest(object):
    def __init__(self, clsobj, num, check=False, time=True):
        assert (issubclass(clsobj, bst.BST))
        self.tcls = clsobj
        self.tree = None
        self.dic = {}
        assert (0 < num < 100000)
        for i in range(num):
            r = random.randint(0, 100000)
            self.dic[r] = r + 1
        print "dic's size: ", len(self.dic)
        self.check = check
        self.time = time
        self.start_t = 0
        self.end_t = 0

    def new(self):
        self.tree = self.tcls()
        c = 0
        if self.time:
            self.start_t = time.time()
        for i, j in self.dic.viewitems():
            self.tree.insert(i, j)
            if self.check:
                self.tree.check()
            assert (self.tree.search(i) == j)
            c += 1
            assert (self.tree.size() == c)
        if self.time:
            self.end_t = time.time()
            print 'new:\t\t', self.end_t - self.start_t
        assert (self.tree.size() == len(self.dic))

    def deleteMaxMin(self):
        def test(get, delete):
            c = s = self.tree.size()
            if self.time:
                self.start_t = time.time()
            for i in range(s):
                m = getattr(self.tree, get)()
                getattr(self.tree, delete)()
                if self.check:
                    self.tree.check()
                assert (self.tree.search(m.key) == None)
                c -= 1
                assert (self.tree.size() == c)
            if self.time:
                self.end_t = time.time()
                print delete + ':\t', self.end_t - self.start_t
            assert (self.tree.size() == 0)

        self.new()
        test('getMin', 'deleteMin')
        self.new()
        test('getMax', 'deleteMax')

    def delete(self):
        self.new()
        c = self.tree.size()
        if self.time:
            self.start_t = time.time()
        for i in self.dic:
            assert (self.tree.search(i))
            self.tree.delete(i)
            if self.check:
                self.tree.check()
            assert (self.tree.search(i) == None)
            c -= 1
            assert (self.tree.size() == c)
        if self.time:
            self.end_t = time.time()
            print 'delete:\t\t', self.end_t - self.start_t
        assert (self.tree.size() == 0)
