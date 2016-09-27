# -*- coding: utf-8 -*-
# data structure: suffix tree

from base.tree import Tree, TreeTest
from base.string import String, StringTest


class SuffixTree(String, Tree):
    def __init__(self):
        super(SuffixTree, self).__init__()


class SuffixTreeTest(StringTest, TreeTest):
    def __init__(self):
        super(SuffixTreeTest, self).__init__()


if __name__ == '__main__':
    SuffixTreeTest(500).testcase()
    print 'done'
