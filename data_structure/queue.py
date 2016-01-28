# -*- coding: utf-8 -*-
# data structure: queue (FIFO)

class Queue():
    class Node():
        def __init__(self, value):
            self.next = None
            self.value = value

    def __init__(self):
        self.head = None
        self.count = 0

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
            ret = self.head.value
            self.head = self.head.next
            self.count -= 1
        return ret

    def size(self):
        return self.count

    def clean(self):
        self.head = None
        self.count = 0


if __name__ == '__main__':
    q = Queue()
    for i in range(10):
        q.push(i)
    for i in range(12):
        print q.pop(),
        assert (q.size() == (10 - i - 1 if i < 10 else 0))
    assert (q.size() == 0)
