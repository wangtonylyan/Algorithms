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

        def set(self, **kwargs):
            for k, v in kwargs.items():
                if hasattr(self, k):
                    setattr(self, k, v)
            return self

    def __init__(self):
        self.root = None

    def __len__(self):
        assert False

    def __str__(self):
        assert False

    def search(self, *args, **kwargs):
        assert False

    def getmax(self, *args, **kwargs):
        assert False

    def getmin(self, *args, **kwargs):
        assert False

    def insert(self, *args, **kwargs):
        assert False

    def delete(self, *args, **kwargs):
        assert False

    def delmax(self, *args, **kwargs):
        assert False

    def delmin(self, *args, **kwargs):
        assert False
