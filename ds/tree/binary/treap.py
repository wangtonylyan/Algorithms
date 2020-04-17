# -*- coding: utf-8 -*-
# data structure: treap
# treap is the portmanteau of "tree" and "heap"
# The heap and binary search tree properties together ensure that,
# once the key and priority for each node are defined,
# the shape of the Treap is completely determined.
# 对于任意子树而言，其中优先级最小的节点必定就是根节点
# 由于在普通的二叉树中，较早插入的节点一定是作为较晚节点的树根
# 换言之，树堆就好比是在二叉树操作的基础上，随机化了输入集
# 然后根据优先级从小至大先后执行插入，从而构建出整棵二叉树
# 总之，树堆实现简单、效率快、支持多数操作，性价比很高
# 树堆的设计思想就是：randomized BST是趋向于平衡的


import random
from bst import SelfBalancingBinarySearchTree, BinarySearchTreeTest


class Treap(SelfBalancingBinarySearchTree):
    class Node(SelfBalancingBinarySearchTree.Node):
        __slots__ = ['priority']

        def __init__(self, key, value, priority):
            super(Treap.Node, self).__init__(key, value)
            self.priority = priority

    def __init__(self, total=1000):
        super(Treap, self).__init__()
        self.total = total * 5
        # 利用该数组来维护priority的唯一性，有的实现也会利用哈希表
        self.prioritySet = [0] * self.total

    def _balance(self, trp):
        assert (trp)
        # binary search tree + minimum heap
        if trp.left and trp.left.priority < trp.priority:
            trp = self._rotateRight_(trp)
        elif trp.right and trp.right.priority < trp.priority:
            trp = self._rotateLeft_(trp)
        return trp

    def insert(self, key, value):
        def recur(trp, key, value):
            if not trp:
                priority = random.randint(0, self.total - 1)
                while self.prioritySet[priority]:
                    # 不能直接搜索prioritySet数组，并使用下一个未被标识的数
                    # 因为这样不够随机
                    priority = random.randint(0, self.total - 1)
                self.prioritySet[priority] = 1
                return self.__class__.Node(key, value, priority)  # insertion
            if key < trp.key:
                trp.left = recur(trp.left, key, value)
                trp = self._balance(trp)
            elif key > trp.key:
                trp.right = recur(trp.right, key, value)
                trp = self._balance(trp)
            else:
                trp.value = value
            return trp

        assert (key is not None and value is not None)
        self.root = recur(self.root, key, value)

    # delete的过程可被视为是与insert互逆的：在top-down阶段将目标节点旋转至叶子节点，再直接删除
    def delete(self, key):
        def recur(trp, key):
            if not trp:
                return trp  # deletion fails
            if key < trp.key:
                trp.left = recur(trp.left, key)
            elif key > trp.key:
                trp.right = recur(trp.right, key)
            else:  # == Heap.sink
                if not trp.left and not trp.right:
                    self.prioritySet[trp.priority] = 0
                    trp = None  # deletion
                elif not trp.left:
                    trp = self._rotateLeft_(trp)
                    trp.left = recur(trp.left, key)
                elif not trp.right:
                    trp = self._rotateRight_(trp)
                    trp.right = recur(trp.right, key)
                else:
                    if trp.left.priority < trp.right.priority:
                        trp = self._rotateRight_(trp)
                        trp.right = recur(trp.right, key)
                    else:
                        assert (trp.left.priority > trp.right.priority)
                        trp = self._rotateLeft_(trp)
                        trp.left = recur(trp.left, key)
            return trp

        self.root = recur(self.root, key)

    def deleteMax(self):
        trp = self._getMax(self.root)
        if trp:
            super(Treap, self).deleteMax()
            assert (self.prioritySet[trp.priority] == 1)
            self.prioritySet[trp.priority] = 0

    def deleteMin(self):
        trp = self._getMin(self.root)
        if trp:
            super(Treap, self).deleteMin()
            assert (self.prioritySet[trp.priority] == 1)
            self.prioritySet[trp.priority] = 0

    def clean(self):
        assert (len(self.prioritySet) == self.total)
        self.prioritySet = [0] * self.total
        super(Treap, self).clean()

    def _check(self, trp, left, right):
        if trp:
            # check heap order property
            if trp.left:
                assert (trp.priority < trp.left.priority)
            if trp.right:
                assert (trp.priority < trp.right.priority)
            if trp is self.root:
                assert (left + right + 1 == sum(self.prioritySet))
        return super(Treap, self)._check(trp, left, right)


if __name__ == '__main__':
    BinarySearchTreeTest(Treap).testcase()
    print 'done'
