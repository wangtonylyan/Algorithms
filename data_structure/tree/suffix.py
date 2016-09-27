# -*- coding: utf-8 -*-
# data structure: suffix tree

from base.tree import Tree, TreeTest
from base.string import String, StringTest


class SuffixTree(Tree, String):
    def __init__(self):
        super(SuffixTree, self).__init__()


class SuffixTreeTest(TreeTest, StringTest):
    pass


if __name__ == '__main__':
    print 'done'
