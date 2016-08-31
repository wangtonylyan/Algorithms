# -*- coding: utf-8 -*-
# data structure: trie search tree (aka. digital tree)
# The term "trie" comes from retrieval, which is sometimes pronounced "try" to avoid confusion with "tree".


from string.string import String
import time


class TrieSearchTree(String):
    class Node(object):
        def __init__(self):
            # 'key' is a character as the index of 'self.next' array
            self.next = [None] * TrieSearchTree.alphabet
            self.value = None  # initialized as a void node

    def __init__(self):
        super(TrieSearchTree, self).__init__()
        self.root = None

    def insert(self, key, value):
        assert (len(key) > 0 and value != None)
        if self.root == None:
            self.root = self.__class__.Node()
        trie = self.root
        for c in key:
            if trie.next[self.ord(c)] == None:
                trie.next[self.ord(c)] = self.__class__.Node()
            trie = trie.next[self.ord(c)]
        trie.value = value
        return

    def delete(self, key):
        def recur(trie, ind):
            if trie == None:
                return None
            if ind == len(key):
                assert (trie.value != None)
                trie.value = None  # find it
            else:
                trie.next[self.ord(key[ind])] = recur(trie.next[self.ord(key[ind])], ind + 1)
            if trie.value == None and all(i == None for i in trie.next):
                return None  # delete the 'trie' subtree
            return trie

        self.root = recur(self.root, 0)

    def search(self, key):
        trie = self.root
        for c in key:
            if trie == None:
                break
            trie = trie.next[self.ord(c)]
        return trie.value if trie else None

    def __len__(self):
        def recur(trie):
            if trie == None:
                return 0
            return sum(recur(t) if t else 0 for t in trie.next) + (1 if trie.value else 0)

        return recur(self.root)

    def check(self):
        def recur(trie):
            if trie == None:
                return
            flg = True
            for t in trie.next:
                if t != None:
                    assert (isinstance(t, self.__class__.Node))
                    recur(t)
                    flg = False
            if flg:
                assert (trie.value)

        recur(self.root)


class TrieSearchTreeTest(String):
    def __init__(self, num):
        self.tree = None
        self.dic = {}
        cases = self._gencase(each=1, total=num)
        for case in cases:
            s = case[0]
            self.dic[s] = reduce(lambda v, c: v + ord(c), s, 0)
        print "dic's size: ", len(self.dic)

    def new(self):
        self.tree = TrieSearchTree()
        c = 0
        cost = 0
        assert (len(self.tree) == 0)
        for k, v in self.dic.items():
            start = time.time()
            self.tree.insert(k, v)
            end = time.time()
            cost += end - start
            self.tree.check()
            c += 1
            assert (self.tree.search(k) == v)
            assert (len(self.tree) == c)
        assert (c == len(self.dic) == len(self.dic))
        print 'pass: new() -', cost

    def delete(self):
        self.new()
        c = len(self.dic)
        cost = 0
        assert (len(self.tree) == len(self.dic))
        for k, v in self.dic.items():
            assert (self.tree.search(k) == v)
            start = time.time()
            self.tree.delete(k)
            end = time.time()
            cost += end - start
            self.tree.check()
            c -= 1
            assert (self.tree.search(k) == None)
            assert (len(self.tree) == c)
        assert (c == len(self.tree) == 0)
        print 'pass: delete() -', cost


if __name__ == '__main__':
    tst = TrieSearchTreeTest(200)
    tst.delete()
    print 'done'
