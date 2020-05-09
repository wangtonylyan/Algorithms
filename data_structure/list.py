## data structure: linked list

if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))


from algorithms.utility import *


class List:
    class Node:
        __slots__ = ['value', 'next']

        def __init__(self, value=None, next=None):
            self.value = None
            self.next = next

    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size  # len(lst)

    def index(self, index):
        n = index if index >= 0 else abs(index) - 1
        i = self.head

        # 当index非负时，直接寻找第index个节点
        # 当index为负时，预先寻找第|index|-1个节点
        while n > 0 and i:
            n -= 1
            i = i.next

        if index >= 0 or not i:
            return i

        # 由于i与j之间的距离为|index|-1
        # 因此当i位于lst[-1]时，j将位于lst[index]
        j = self.head
        while i.next:
            i, j = i.next, j.next
        return j

    def search(self, value):
        return  # lst.index(value)

    def insert(self, index, value):
        pass  # lst[:index] + [value] + lst[index:]

    def delete(self, value):
        pass  # del lst[lst.index(value)]

    # 实现栈的逻辑，默认在头节点执行插入/删除效率高
    def push(self, value, head=True):
        if head or not self.head:
            self.head = self.Node(value, self.head)
            return

        tail = self.head
        while tail.next:
            tail = tail.next
        tail.next = self.Node(value)

    def pop(self, head=True):
        if not self.head:
            return

        if head or not self.head.next:
            node, self.head = self.head, self.head.next
            return self.Node(node.value)

        tail = self.head
        while tail.next.next:
            tail = tail.next
        node, tail.next = tail.next, None
        return self.Node(node.value)

    def append(self, lst):
        assert isinstance(lst, List)

        if not lst.head:
            return
        if not self.head:
            self.head = lst.head
            return

        tail = self.head
        while tail.next:
            tail = tail.next
        tail.next = lst.head

    # 对于有环的链表而言，以下算法仅反转了整个环
    # 不属于环的部分，在经过两次反转后，又恢复了原样
    # 但这恰恰是合理的，因为有环的链表并没有终点
    # 而反转则要求将链表的终点作为起点，因此也就无法整体地反转了
    def reverse(self):
        if not self.head:
            return self

        i, j = self.head, self.head.next
        i.next = None

        while j:
            k, j.next = j.next, i
            i, j = j, k

        lst.head = i

    ## 判断链表中是否有环
    # 1. 标记遍历到的每个节点，并对每个遍历到的节点进行判断
    # 2. 将遍历到的每个节点，都与已遍历到的节点进行比较
    #    已遍历到的节点可以存储在哈希表等数据结构中
    # 3. Floyd's cycle-finding algorithm, aka. tortoise and hare algorithm
    #    基于该算法，还可进一步判断环中的入口节点和节点数量
    def iscyclic(self):
        if not self.head:
            return

        # 令环中节点个数为n，快慢指针分别为fast和slow
        # 1. 假设链表中存在有环，则为何fast与slow总能相遇？
        #    首先，fast和slow最终都将进入环内
        #    其次，虽然fast会以两个节点的速度前进，即略过fast.next节点
        #    但fast与slow之间的距离，最多只有{0,1,...,n-1}这n种可能
        #    而最重要的是，slow每前进一次，其与fast的距离都将增加一个节点
        #    因此在slow前进n及其以内个节点，其与fast的距离必然会增加至n，亦即相遇
        # 2. 上述段落也解释了，对于fast与slow，
        #    为何两者在第一次相遇时，slow必定没有遍历完整个链表
        #    为何两者在第一次相遇后，继续遍历，将始终相遇于同一个节点
        #    为何两者在先后相遇两次的过程中，slow所遍历的节点个数就是环中的节点个数
        # 3. 对于链表的长度，若将其划分为以下三个部分
        #    a = [链表头节点, 环入口节点]
        #    b = [环入口节点, 环中相遇节点]
        #    c = [环中相遇节点, 环入口节点]
        #    则有以下两个等式关系
        #    len(lst) = a + b + c
        #    2 * slow = 2 * (a + b) = a + b + n * (b + c) = fast
        #    由后者可得，fast与slow相遇时，两者遍历的节点个数之差，是环中节点个数的整数倍
        #    换言之，两者的区别仅在于，fast比slow在环中多绕了几圈
        #    此外，由等式a = n * (b + c) - b，即可得到以下求环入口节点的算法
        i, j = self.head, self.head.next

        while j and j.next:
            if i == j:
                break
            i, j = i.next, j.next.next

        if i != j:  # 链表中没有环
            return

        n = 1  # 两者始终相遇于同一个节点，因此只需计入起点，而无需计入终点
        i, j = i.next, j.next.next  # 先各自前进一次，以避免以下while条件
        while i != j:
            n += 1
            i, j = i.next, j.next.next

        # 以下两者的相遇节点就是环入口节点，其各自遍历了a和n(b+c)-b个节点
        i = self.head
        while i != j:
            i, j = i.next, j.next

        return n, i


if __name__ == '__main__':
    Problem.testsuit([
    ])

# TODO
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
