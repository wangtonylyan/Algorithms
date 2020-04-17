# -*- coding: utf-8 -*-
# data structure: persistent vector
# 1) reference
# http://www.hypirion.com/musings/understanding-persistent-vector-pt-1
# http://www.hypirion.com/musings/understanding-persistent-vector-pt-2
# http://www.hypirion.com/musings/understanding-persistent-vector-pt-3


from data_structure.tree.trie import BitTrieTree, TrieTreeTest
import math


class PersistentVector(object):
    # 所有数据都存储于叶子节点，中间节点不存储数据
    class InternalBitTrie(BitTrieTree):
        def __init__(self, num, bit=1):
            assert (0 < num <= self.alphabet + 1)
            super(PersistentVector.InternalBitTrie, self).__init__(bit)
            self.height = int(math.ceil(math.log(num, 1 << bit)))  # the leaf level should hold 'num' elements
            self.shift = (self.height - 1) * self.bit  # maximum/initial shift

        def _iter(self, key):
            assert (isinstance(key, int) and 0 <= key <= self.alphabet)
            shift = self.shift
            while shift >= 0:
                yield (key >> shift) & self.mask  # MSB first
                shift -= self.bit
            raise StopIteration

    def __init__(self):
        super(PersistentVector, self).__init__()
        self.head = None
        self.size = 0


if __name__ == '__main__':
    TrieTreeTest(PersistentVector.InternalBitTrie, args={'num': 1000}, num=1000).testcase()
    print 'done'
