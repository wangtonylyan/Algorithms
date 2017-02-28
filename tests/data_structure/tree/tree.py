# -*- coding: utf-8 -*-


import random, timeit
from algos.data_structure.tree.tree import Tree


class TreeTest:
    def __init__(self, cls, args, num, time):
        assert issubclass(cls, Tree) and isinstance(args, dict) and num > 0
        self.cls = cls
