# -*- coding: utf-8 -*-
# data structure: trie tree
# 字典树，是典型的"空间换时间"的设计
# The term "trie" comes from retrieval, which is sometimes pronounced "try" to avoid confusion with "tree".
# 用于存储字符串时，每个节点的键是character；用于存储数字时，每个节点的键则是digit或bit


from base.tree import Tree, TreeTest
from base.string import String, StringTest
from base.number import Number, NumberTest


class TrieTree(Tree):
    def __init__(self):
        super(TrieTree, self).__init__()

    def _iter(*args):
        assert (False)

    def __len__(self):
        def recur(trie):
            if not trie:
                return 0
            return sum(map(recur, trie.key)) + (1 if trie.value is not None else 0)

        return recur(self.root)

    def search(self, key):
        trie = self.root
        for k in self._iter(key):
            if not trie:
                break
            trie = trie.key[k]
        if not trie or trie.value is None:  # 这两个条件都表示该key不存在
            return None
        return trie.value

    def insert(self, key, value):
        assert (key is not None and value is not None)
        return self._insert(key, value)

    def _insert(self, key, value, *args):
        if not self.root:
            self.root = self.__class__.Node(*args)
        trie = self.root
        for k in self._iter(key):
            if not trie.key[k]:
                trie.key[k] = self.__class__.Node(*args)
            trie = trie.key[k]
        trie.value = value
        assert (self.root.value is None)

    def delete(self, key):
        self.root = self._delete(self.root, self._iter(key))

    def _delete(self, trie, key):
        try:
            k = key.next()
            if trie:
                trie.key[k] = self._delete(trie.key[k], key)
        except StopIteration:
            if trie:
                assert (trie.value is not None)
                trie.value = None  # find it
        finally:
            if trie and trie.value is None and all(not i for i in trie.key):
                return None  # delete 'trie' subtree
            return trie

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


# character partitioning
class StringTrieTree(TrieTree, String):
    class Node(TrieTree.Node):
        def __init__(self):
            super(StringTrieTree.Node, self).__init__([None] * StringTrieTree.alphabet, None)

    def __init__(self):
        super(StringTrieTree, self).__init__()

    def _iter(self, key):
        assert (isinstance(key, str) and len(key) > 0)
        for c in key:
            yield self.ord(c)
        raise StopIteration


# abstract class
class NumberTrieTree(TrieTree, Number):
    pass


# digit partitioning
class DigitTrieTree(NumberTrieTree):
    class Node(NumberTrieTree.Node):
        def __init__(self, radix):
            super(DigitTrieTree.Node, self).__init__([None] * radix, None)

    def __init__(self, radix=10):
        super(DigitTrieTree, self).__init__()
        self.radix = radix

    def _iter(self, key):
        assert (isinstance(key, int) and 0 <= key <= self.alphabet)
        yield key % self.radix  # LSD first
        key /= self.radix
        while key > 0:
            yield key % self.radix
            key /= self.radix
        raise StopIteration

    def insert(self, key, value):
        return self._insert(key, value, self.radix)


# bit partitioning
class BitTrieTree(NumberTrieTree):
    class Node(NumberTrieTree.Node):
        def __init__(self, bit):
            super(BitTrieTree.Node, self).__init__([None] * (1 << bit), None)

    def __init__(self, bit=4):
        super(BitTrieTree, self).__init__()
        self.bit = bit
        self.mask = (1 << bit) - 1

    def _iter(self, key):
        assert (isinstance(key, int) and 0 <= key <= self.alphabet)
        yield key & self.mask  # LSB first
        key >>= self.bit
        while key > 0:
            yield key & self.mask
            key >>= self.bit
        raise StopIteration

    def insert(self, key, value):
        return self._insert(key, value, self.bit)


class TrieTreeTest(TreeTest):
    def __init__(self, cls, args={}, num=1000, check=True, time=True):
        assert (issubclass(cls, TrieTree) and isinstance(args, dict) and num > 0)
        super(TrieTreeTest, self).__init__(cls, args, 0, check, time)
        self.cases = {}
        if issubclass(self.cls, StringTrieTree):
            for case in StringTest()._gencase(maxLen=20, each=1, total=num):
                c = case[0]
                self.cases[c] = reduce(lambda v, c: v + ord(c), c, 0)
        elif issubclass(self.cls, NumberTrieTree):
            cases = NumberTest()._gencase(minLen=num, maxLen=num, each=1, total=1, dup=False)
            for c in cases[0][0]:
                self.cases[c] = c + 1
        print '=' * 50
        print "sample size:\t", len(self.cases)

    def _testcase(self):
        self.delete()


if __name__ == '__main__':
    TrieTreeTest(StringTrieTree, num=300).testcase()
    TrieTreeTest(DigitTrieTree).testcase()
    TrieTreeTest(BitTrieTree).testcase()
    print 'done'
