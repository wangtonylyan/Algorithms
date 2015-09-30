# -*- coding: utf-8 -*-
# data structure: max-heap

# 最大/最小堆都基于两个核心的基本操作来维护：float()和sink()
# 因此要在最大/最小堆的基础上实现最小/最大堆只需修改上述两个函数即可
class MaxHeap:
    def __init__(self):
        # lst[0]被保留，这样i*2直接就是i的子节点了，否则还要讨论i是否等于0
        self.lst = [0]  # lst[i] is the father of lst[i*2] and lst[i*2+1]

    def _float(self, i):
        while i > 1 and self.lst[i] > self.lst[i / 2]:
            self.lst[i], self.lst[i / 2] = self.lst[i / 2], self.lst[i]
            i /= 2

    def _sink(self, i):
        while i * 2 < len(self.lst):
            j = i * 2
            if j + 1 < len(self.lst) and self.lst[j + 1] > self.lst[j]:  # get the bigger between two children
                j += 1
            if self.lst[i] >= self.lst[j]:
                break
            self.lst[i], self.lst[j] = self.lst[j], self.lst[i]
            i = j

    def insert(self, val):
        self.lst.append(val)
        self._float(len(self.lst) - 1)

    def pop(self):
        m = self.lst[1]
        self.lst[1] = self.lst[len(self.lst) - 1]
        self.lst.pop()
        self._sink(1)
        return m

    def size(self):
        return len(self.lst) - 1


if __name__ == "__main__":
    pass
