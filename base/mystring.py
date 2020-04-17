# -*- coding: utf-8 -*-

import random
from test import Test


class String(object):
    # 256  # number of legal characters by ASCII, [0,255]
    alphabet = ord('z') - ord('a') + 1
    def ord(self, x): return ord(x) - ord('a')


class StringTest(Test):
    def __init__(self):
        super(StringTest, self).__init__()

    @classmethod
    def _testcase(cls, test, cases):
        map(test, cases)
        # print 'pass:', cls, '-', len(cases)

    @classmethod
    def _gencase(cls, fixed=False, maxLen=40, each=50, total=100):
        cases = []
        for _ in range(total):
            case = []
            width = random.randint(1, maxLen) if fixed else None
            for _ in range(each):
                width = width if fixed else random.randint(1, maxLen)
                case.append(
                    ''.join([chr(random.randint(ord('a'), ord('z'))) for _ in range(width)]))
            cases.append(case)
        return cases


if __name__ == '__main__':
    cases = StringTest()._gencase()
    for case in cases:
        # print case
        assert (isinstance(case, list) and len(case) > 0)
        assert (all(isinstance(i, str) and len(i) > 0 for i in case))
    # print len(cases)
    # print 'done'

    class Node:
        def __init__(self, key, left=None, right=None):
            self.key = key
            self.left = left
            self.right = right

    class Tree:
        def __init__(self):
            self.root = Node(0, Node(-1), Node(1))
            self.iter = self.root

        def __iter__(self):
            return self

        def __next__(self):
            if self.iter == self.root:
                self.iter = self.root.left
                return self.root
            elif self.iter == self.root.left:
                self.iter = self.root.right
                return self.root.left
            elif self.iter == self.root.right:
                self.iter = None
                return self.root.right
            raise StopIteration

    class TreeIterator:
        def __init__(self, tree):
            self.iter = None
            self.tree

        def __next__(self):


    t = Tree()
    print([n.key for n in t])
