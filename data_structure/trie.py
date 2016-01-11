# -*- coding: utf-8 -*-
# data structure: trie search tree (aka. digital tree, prefix tree)
# The term "trie" comes from retrieval, which is sometimes pronounced "try" to avoid confusion with "tree".
# useful for key with string type

class TrieST(object):
    alphabet = 256  # ASCII

    class Node():
        def __init__(self):
            # self.key is a character and not necessary for implementation
            self.value = None  # indicates it's a void node by default
            self.next = [None for i in range(TrieST.alphabet)]

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        def _recur(tst, key, value):
            if tst == None:
                tst = self.__class__.Node()
            if len(key) == 0:
                tst.value = value  # find it
            else:
                tst.next[ord(key[0])] = _recur(tst.next[ord(key[0])], key[1:], value)
            return tst

        assert (key != None and isinstance(key, str) and len(key) > 0 and value != None)
        self.root = _recur(self.root, key, value)

    def delete(self, key):
        def _recur(tst, key, value):
            pass  # TODO

        _recur(self.root, key)

    def search(self, key):
        def _iter(key):
            it = self.root
            c = 0
            while it:
                if c == len(key):
                    return it.value
                it = it.next[ord(key[c])]
                c += 1
            return None

        def _iter2(key):  # 也可以通过遍历key来实现
            it = self.root
            for c in key:
                if it == None:
                    return None
                it = it.next[ord(c)]
            return it.value if it else None

        return _iter(key)

    def check(self):
        def _recur(tst):
            ret = True if tst.value else False
            for n in tst.next:
                ret |= _recur(n) if n else False  # termination
            return ret

        return _recur(self.root) if self.root else True


import time, random


class TrieSTTest():
    def __init__(self, num):
        self.tree = None
        self.dic = {}
        assert (0 < num < 100000)
        for i in range(num):
            # random string with random length
            k = str(random.sample('abcdefghijklmnopqrstuvwxyz', random.randint(1, 20)))
            v = reduce(lambda v, c: v + ord(c), k, 0)
            self.dic[k] = v
        print "dic's size: ", len(self.dic)

    def new(self):
        self.tree = TrieST()
        c = 0
        for k, v in self.dic.items():
            self.tree.insert(k, v)
            c += 1
            assert (self.tree.search(k) == v)
            assert (self.tree.check())


if __name__ == '__main__':
    tst = TrieSTTest(100)
    tst.new()
