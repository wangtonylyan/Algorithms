# -*- coding: utf-8 -*-
# data structure: tree


class Tree:
    class Node:
        __slots__ = ['key', 'value']

        # as both init and copy constructor
        def __init__(self, key, value):
            super().__init__()
            self.key = key
            self.value = value

        def cmp(self, key):
            return -1 if key < self.key else 1 if key > self.key else 0

    def __init__(self):
        super().__init__()
        self.root = None

    def __len__(self):
        assert False

    def search(*args):
        assert False

    def getmax(*args):
        assert False

    def getmin(*args):
        assert False

    def insert(*args):
        assert False

    def delete(*args):
        assert False

    def delmax(*args):
        assert False

    def delmin(*args):
        assert False
