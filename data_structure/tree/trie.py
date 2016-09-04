# -*- coding: utf-8 -*-
# data structure: trie tree (aka. digital tree, prefix tree, or radix tree)
# 字典树，典型的"空间换时间"的设计，多适用于字符串相关问题
# The term "trie" comes from retrieval, which is sometimes pronounced "try" to avoid confusion with "tree".


from tree import Tree, TreeTest
from string.string import String


class TrieTree(Tree, String):
    class Node(object):
        __slots__ = ['next', 'value']

        def __init__(self):
            # 'key' is a character as the index of 'self.next' array
            self.next = [None] * TrieTree.alphabet
            self.value = None  # initialized as a void node

    def __init__(self):
        super(TrieTree, self).__init__()
        self.root = None

    def __len__(self):
        def recur(trie):
            if trie == None:
                return 0
            return sum(recur(t) if t else 0 for t in trie.next) + (1 if trie.value else 0)

        return recur(self.root)

    def search(self, key):
        trie = self.root
        for c in key:
            if trie == None:
                break
            trie = trie.next[self.ord(c)]
        if trie == None or trie.value == None:  # 这两个条件都表示该字符串不存在
            return None
        return trie.value

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
        assert (self.root.value == None)
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

    def check(self):
        def recur(trie):
            if trie == None:
                return 0
            cnt = 0
            flg = True
            for t in trie.next:
                if t != None:
                    assert (isinstance(t, self.__class__.Node))
                    cnt += recur(t)
                    flg = False
            if flg:
                assert (trie.value)
                assert (cnt == 0)
            if trie.value:
                cnt += 1
            return cnt

        assert (recur(self.root) == len(self))
        assert (self.root == None or self.root.value == None)


class TrieTreeTest(TreeTest, String):
    def __init__(self, num):
        assert (num > 0)
        TreeTest.__init__(self, TrieTree, 0, True, True)
        self.tree = None
        self.dic = {}
        cases = self._gencase(each=1, total=num)
        for case in cases:
            s = case[0]
            self.dic[s] = reduce(lambda v, c: v + ord(c), s, 0)
        print "sample size:\t", len(self.dic)

    def deleteMaxMin(self):
        assert (False)

    def testcase(self):
        self.delete()


if __name__ == '__main__':
    TrieTreeTest(500).testcase()
    print 'done'
