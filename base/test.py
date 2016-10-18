# -*- coding: utf-8 -*-


class Test(object):
    def __init__(self):
        super(Test, self).__init__()

    def testcase(self, *args):
        assert (False)

    def _testcase(self, *args):
        assert (False)

    def _gencase(self, *args):
        assert (False)
