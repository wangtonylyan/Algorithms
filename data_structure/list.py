# -*- coding: utf-8 -*-

def car(lst):
    return lst[0]

def cdr(lst):
    return lst[1:]



#判断一个链表是否有循环，从头开始遍历
#1)标记已遍历到的每个节点，每次遍历到一个节点时都需判断是否已被标记
# 缺点是需要在节点中维护额外变量，并在遍历时修改链表
#2)将当前遍历到的节点与其之前遍历到的节点进行比较，判断是否有相同节点
#可以原地比较，也可以利用一个额外的数据结构存储已遍历到的节点，但两者的比较次数相同
#3)Floyd's cycle-finding algorithm, aka. tortoise and hare algorithm
class List(object):
    class Node():
        def __init__(self):
            self.value = None
            self.next = None

    def __init__(self):
        self.head = None

