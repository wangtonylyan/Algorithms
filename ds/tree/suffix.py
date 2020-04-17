# -*- coding: utf-8 -*-
# data structure: suffix tree

from base.tree import Tree, TreeTest
from base.string import String, StringTest


class SuffixTree(Tree, String):
    def __init__(self):
        super(SuffixTree, self).__init__()


class SuffixTreeTest(TreeTest, StringTest):
    def __init__(self, num=500):
        super(SuffixTreeTest, self).__init__(SuffixTree, {}, 0, True, True)
        self.cases = self._gencase(each=1, total=num)
        print '=' * 50
        print "sample size:\t", len(self.cases)

    def _testcase(self):
        self.insert()


if __name__ == '__main__':
    SuffixTreeTest().testcase()
    print 'done'
