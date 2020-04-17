# -*- coding: utf-8 -*-
# data structure: list
# 线性表：顺序表(数组)，静态链表，链表
# 链表：单/双向链表，单/双向循环链表
# 1) 单向链表 & 双向链表
# 即单向与双向遍历
# 2) 单向循环链表 & 双向循环链表
# 空间使用上，两者分别等同于
# 单向链表+一个尾节点指针变量
# 双向链表+一对头/尾节点指针变量
# 3) 有头节点 & 无头节点
# 仅对于单向循环链表"删除第一个节点"的操作而言
# 存在O(1)与O(n)的区别


class List:
    class Node:
        def __init__(self, value=None, next=None):
            self.value = value
            self.next = next

    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.__class__.Iterator(self)

    def insert(self, value):
        self.head = self.__class__.Node(value, self.head)

    def remove(self):


    class Iterator():
        def __init__(self, list):
            self.list = list
            # self.iter = None

        def __iter__(self):
            return self

        def __next__(self):
            if not self.list:
                raise StopIteration

            if self.iter:
                self.iter = self.list.next
            else:
                self.iter = self.list.head

            if self.iter:
                return self.iter

            raise StopIteration


class List2(object):

    def add(self, key, value):
        if self.head:
            iter = self.head
            while iter.next and iter.next.key != key:
                iter = iter.next
            if iter.next:
                iter.next.value = value
            else:
                iter.next = self.__class__.Node(key, value)

    def append(self, key, value):
        pass

    # @problem: 判断一个链表是否有循环，从头开始遍历
    # 1) 标记已遍历到的每个节点，每次遍历到一个节点时都需判断是否已被标记
    # 缺点是需要在节点中维护额外变量，并在遍历时修改链表
    # 2) 将当前遍历到的节点与其之前遍历到的节点进行比较，判断是否有相同节点
    # 可以原地比较，也可以利用一个额外的数据结构存储已遍历到的节点，但两者的比较次数相同
    # 3) Floyd's cycle-finding algorithm, aka. tortoise and hare algorithm
    def checkCyclic(self):
        if self.head:
            hare = self.head.next
            tortoise = self.head
            while hare and tortoise:
                if not hare.next or not hare.next.next:
                    return False
                if hare == tortoise:
                    return True
                hare = hare.next.next
                tortoise = tortoise.next
        return False

    # @problem: 判断两个无环的单向链表是否有共同的节点
    # solution: 两个链表都走到底，比较最后一个节点是否相同

    # @problem: reverse

    def reverse(self):
        iter = self.head
        self.head = None
        while iter != None:
            next = iter.next
            iter.next = self.head
            self.head = iter
            iter = next


if __name__ == '__main__':
    lst = List()
    lst.add(1, 1)
    for i in lst:
        print(i)
