# -*- coding: utf-8 -*-
# data structure: stack (FILO)

from list import List


class Stack(List):
    def __init__(self):
        super(Stack, self).__init__()

    def push(self, value):
        stk = self.__class__.Node(value)
        stk.next = self.head
        self.head = stk
        self.count += 1

    def pop(self):
        ret = None
        if self.head:
            ret = self.head.key
            self.head = self.head.next
            self.count -= 1
        return ret

    def testcase(self):
        s = self.__class__()

        for i in range(10):
            s.push(i)
            assert (len(s) == i + 1)
        for i in range(12):
            s.pop()
            assert (len(s) == (10 - i - 1 if i < 10 else 0))
        assert (len(s) == 0)

        print 'pass:', self.__class__


if __name__ == '__main__':
    Stack().testcase()
