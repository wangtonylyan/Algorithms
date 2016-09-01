# -*- coding: utf-8 -*-
# data structure: trie search tree (aka. digital tree)
# The term "trie" comes from retrieval, which is sometimes pronounced "try" to avoid confusion with "tree".


from tree import Tree, TreeTest
from string.string import String


class TrieSearchTree(Tree, String):
    class Node():
        def __init__(self):
            # 'key' is a character as the index of 'self.next' array
            self.next = [None] * TrieSearchTree.alphabet
            self.value = None  # initialized as a void node

    def __init__(self):
        super(TrieSearchTree, self).__init__()
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
        return trie.value if trie else None

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


class TrieSearchTreeTest(TreeTest, String):
    def __init__(self, num):
        assert (num > 0)
        TreeTest.__init__(self, TrieSearchTree, 0, True, True)
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
    TrieSearchTreeTest(200).testcase()
    print 'done'
