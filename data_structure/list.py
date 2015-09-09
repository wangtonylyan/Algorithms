# -*- coding: utf-8 -*-

def car(lst):
    return lst[0]

def cdr(lst):
    return lst[1:]

class List(object):
    class Node():
        def __init__(self):
            self.value = None
            self.next = None

    def __init__(self):
        self.head = None


