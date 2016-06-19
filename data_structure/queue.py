# -*- coding: utf-8 -*-
# data structure: queue (FIFO)

from list import List


class Queue(List):
    def __init__(self):
        super(Queue, self).__init__()

    def push(self, value):
        que = self.__class__.Node(value)
        if self.head:
            it = self.head
            while it.next:
                it = it.next
            it.next = que
        else:
            self.head = que
        self.count += 1

    def pop(self):
        ret = None
        if self.head:
            ret = self.head.key
            self.head = self.head.next
            self.count -= 1
        return ret

    def testcase(self):
        q = self.__class__()

        for i in range(10):
            q.push(i)
            assert (len(q) == i + 1)
        for i in range(12):
            q.pop()
            assert (len(q) == (10 - i - 1 if i < 10 else 0))
        assert (len(q) == 0)

        print 'pass:', self.__class__


if __name__ == '__main__':
    Queue().testcase()
