# -*- coding: utf-8 -*-
# data structure: tree


class Tree:
    class Node:
        __slots__ = ['key', 'value']

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __str__(self):
            return f'key={str(self.key)}, value={str(self.value)}'

        def cmp(self, key):
            return -1 if key < self.key else 1 if key > self.key else 0

        def set(self, **kwargs):
            for k, v in kwargs.items():
                if hasattr(self, k):
                    setattr(self, k, v)
            return self

    def __init__(self):
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
