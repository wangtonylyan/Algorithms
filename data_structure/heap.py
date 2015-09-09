# -*- coding: utf-8 -*-
# data structure: max-heap

#最大/最小堆都基于两个核心的基本操作来维护：float()和sink()
#因此要在最大/最小堆的基础上实现最小/最大堆只需修改上述两个函数即可
class MaxHeap:
    def __init__(self):
        self.arr = [0] #arr[i]是arr[i*2]和arr[i*2+1]的父节点

    def _float(self, i):
        while i > 1 and self.arr[i] > self.arr[i/2]:
            self.arr[i],self.arr[i/2] = self.arr[i/2],self.arr[i]
            i = i/2

    def _sink(self, i):
        while i*2 < len(self.arr):
            j = i*2
            if j+1 < len(self.arr) and self.arr[j] < self.arr[j+1]:
                j += 1
            if self.arr[i] >= self.arr[j]:
                break
            self.arr[i],self.arr[j] = self.arr[j],self.arr[i]
            i = j

    def insert(self, val):
        self.arr.append(val)
        self._float(len(self.arr)-1)

    def pop(self):
        m = self.arr[1]
        self.arr[1] = self.arr[len(self.arr)-1]
        self.arr.pop()
        self._sink(1)
        return m

    def size(self):
        return len(self.arr)-1


if __name__ == "__main__":
    pass
