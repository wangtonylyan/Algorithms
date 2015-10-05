# -*- coding: utf-8 -*-
# data structure: stack (FILO)

class Stack():
    class Node():
        def __init__(self, val = None):
            self.value = val
            self.next = None

    def __init__(self):
        self.head = None
        self.count = 0

    def push(self, val):
        stk = self.__class__.Node(val)
        stk.next = self.head
        self.head = stk
        self.count += 1

    def pop(self):
        if self.head:
            ret = self.head.value
            self.head = self.head.next
            self.count -= 1
            return ret
        return None

    def size(self):
        return self.count

    def clean(self):
        self.head = None
        self.count = 0


if __name__ == '__main__':
    s = Stack()
    for i in range(10):
        s.push(i)
    for i in range(12):
        print s.pop(),
        assert (s.size() == (10 - i - 1 if i < 10 else 0))
    assert (s.size() == 0)
