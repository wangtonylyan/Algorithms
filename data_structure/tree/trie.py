# -*- coding: utf-8 -*-
# data structure: trie tree
# 字典树，典型的"空间换时间"的设计，多适用于字符串相关问题
# The term "trie" comes from retrieval, which is sometimes pronounced "try" to avoid confusion with "tree".


from base.tree import Tree, TreeTest
from base.string import String, StringTest


class TrieTree(Tree, String):
    class Node(Tree.Node):
        def __init__(self):  # initialized as a void node
            # key is a character as the index of 'self.key' array
            super(TrieTree.Node, self).__init__([None] * TrieTree.alphabet, None)

    def __init__(self):
        super(TrieTree, self).__init__()

    def __len__(self):
        def recur(trie):
            if not trie:
                return 0
            return sum(map(recur, trie.key)) + (1 if trie.value is not None else 0)

        return recur(self.root)

    def search(self, key):
        trie = self.root
        for c in key:
            if not trie:
                break
            trie = trie.key[self.ord(c)]
        if not trie or trie.value is None:  # 这两个条件都表示该字符串不存在
            return None
        return trie.value

    def insert(self, key, value):
        assert (isinstance(key, str) and len(key) > 0 and value is not None)
        if not self.root:
            self.root = self.__class__.Node()
        trie = self.root
        for c in key:
            if not trie.key[self.ord(c)]:
                trie.key[self.ord(c)] = self.__class__.Node()
            trie = trie.key[self.ord(c)]
        trie.value = value
        assert (self.root.value is None)
        return

    def delete(self, key):
        def recur(trie, ind):
            if not trie:
                return None
            if ind == len(key):
                assert (trie.value is not None)
                trie.value = None  # find it
            else:
                trie.key[self.ord(key[ind])] = recur(trie.key[self.ord(key[ind])], ind + 1)
            if trie.value is None and all(not i for i in trie.key):
                return None  # delete the 'trie' subtree
            return trie

        self.root = recur(self.root, 0)

    def check(self):
        def recur(trie):
            if not trie:
                return 0
            cnt = 0
            flg = True
            for t in trie.key:
                if t:
                    assert (isinstance(t, self.__class__.Node))
                    cnt += recur(t)
                    flg = False
            if flg:
                assert (trie.value is not None)
                assert (cnt == 0)
            if trie.value is not None:
                cnt += 1
            return cnt

        assert (recur(self.root) == len(self))
        assert (not self.root or self.root.value is None)


class TrieTreeTest(TreeTest, StringTest):
    def __init__(self, num=500):
        assert (num > 0)
        super(TrieTreeTest, self).__init__(TrieTree, {}, 0, True, True)
        self.cases = {}
        for case in self._gencase(each=1, total=num):
            s = case[0]
            self.cases[s] = reduce(lambda v, c: v + ord(c), s, 0)
        print '=' * 50
        print "sample size:\t", len(self.cases)

    def _testcase(self):
        self.delete()


if __name__ == '__main__':
    TrieTreeTest().testcase()
    print 'done'
