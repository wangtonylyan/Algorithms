# -*- coding: utf-8 -*-
# data structure: trie search tree (aka. digital tree, prefix tree)
# The term "trie" comes from retrieval, which is sometimes pronounced "try" to avoid confusion with "tree".
# useful for key with string type

class TrieSearchTree(object):
    alphabet = 128  # ASCII

    class Node(object):
        def __init__(self):
            self.next = [None for i in range(TrieSearchTree.alphabet)]
            # self.key is a character and not necessary for maintaining
            self.value = None  # indicates it's a void node by default

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

        assert (key != None and isinstance(key, str))
        assert (len(key) > 0 and value != None)
        self.root = _recur(self.root, key, value)

    def delete(self, key):
        def _recur(tst, key):
            if tst == None:
                return tst
            if len(key) == 0:
                tst.value = None  # find it
            else:
                tst.next[ord(key[0])] = _recur(tst.next[ord(key[0])], key[1:])
            for n in tst.next:
                if n != None:
                    return tst
            return None  # delete tst subtree

        assert (key != None and isinstance(key, str))
        self.root = _recur(self.root, key)

    def search(self, key):
        assert (key != None and isinstance(key, str))
        it = self.root
        for c in key:
            if it == None:
                break
            it = it.next[ord(c)]
        return it.value if it else None

    def size(self):
        def _recur(tst):
            ret = 0
            if tst:
                ret = reduce(lambda x, y: x + (_recur(y) if y else 0), tst.next, 0)
                ret += 1 if tst.value else 0
            return ret

        return _recur(self.root)

    def check(self):
        def _recur(tst):
            if tst == None:
                return
            flag = True
            for n in tst.next:
                if n != None:
                    assert (isinstance(n, self.__class__.Node))
                    _recur(n)
                    flag = False
            if flag:
                assert (tst.value)

        _recur(self.root)


import time, random


class TrieSearchTreeTest():
    def __init__(self, num):
        assert (0 < num < 100000)
        self.tree = None
        self.dic = {}
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        for i in range(num):
            # random string with random length
            k = str(random.sample(alphabet, random.randint(1, len(alphabet) >> 1)))
            v = reduce(lambda v, c: v + ord(c), k, 0)
            self.dic[k] = v
        print "dic's size: ", len(self.dic)

    def new(self):
        self.tree = TrieSearchTree()
        c = 0
        for k, v in self.dic.items():
            self.tree.insert(k, v)
            self.tree.check()
            c += 1
            assert (self.tree.search(k) == v)
            assert (self.tree.size() == c)
        assert (c == len(self.dic))
        print 'test new() done'

    def delete(self):
        self.new()
        c = len(self.dic)
        for k, v in self.dic.items():
            self.tree.delete(k)
            self.tree.check()
            c -= 1
            assert (self.tree.search(k) == None)
            assert (self.tree.size() == c)
        assert (c == 0)
        print 'test delete() done'


if __name__ == '__main__':
    tst = TrieSearchTreeTest(100)
    tst.delete()
    print 'done'
