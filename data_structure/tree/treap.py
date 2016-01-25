# -*- coding: utf-8 -*-
# data structure: treap
# treap is the portmanteau of "tree" and "heap"
# The heap and binary search tree properties together ensure that,
# once the key and priority for each node are defined,
# the shape of the Treap is completely determined.
# 根据key属性维护的最小堆的性质，使得树根节点必定是priority最小的节点
# 根据property属性维护的BST的性质，决定了每个节点位于其父节点的左还是右子树


import bst, random


class Treap(bst.BalancedBinarySearchTree):
    class Node(object):
        def __init__(self, key, value, priority):
            self.left = None
            self.right = None
            self.key = key
            self.value = value
            self.priority = priority

    def __init__(self, total=10000):
        super(Treap, self).__init__()
        self.total = total * 5
        # 利用该数组来维护property的唯一性，也有算法在实现上会利用哈希表
        self.prioritySet = [0 for i in range(self.total)]

    def insert(self, key, value):
        def _recur(tp, key, value):
            if tp == None:
                priority = random.randint(0, self.total)
                while self.prioritySet[priority]:
                    # 不能简单地搜索prioritySet数组，并使用下一个未被标识的数
                    priority = random.randint(0, self.total)
                self.prioritySet[priority] = 1
                return self.__class__.Node(key, value, priority)  # insertion
            if key < tp.key:
                tp.left = _recur(tp.left, key, value)
                if tp.left.priority < tp.priority:
                    tp = self._rotateRight(tp)
            elif key > tp.key:
                tp.right = _recur(tp.right, key, value)
                if tp.right.priority < tp.priority:
                    tp = self._rotateLeft(tp)
            else:
                tp.value = value
            return tp

        self.root = _recur(self.root, key, value)

    def delete(self, key):
        def _recur(tp, key):
            if tp == None:
                return tp  # deletion failed
            if key < tp.key:
                tp.left = _recur(tp.left, key)
            elif key > tp.key:
                tp.right = _recur(tp.right, key)
            else:
                if tp.left == None and tp.right == None:
                    self.prioritySet[tp.priority] = 0
                    return None  # deletion
                elif tp.left == None:
                    tp = self._rotateLeft(tp)
                    tp.left = _recur(tp.left, key)
                elif tp.right == None:
                    tp = self._rotateRight(tp)
                    tp.right = _recur(tp.right, key)
                elif tp.left.priority < tp.right.priority:
                    tp = self._rotateRight(tp)
                    tp.right = _recur(tp.right, key)
                else:
                    assert (tp.left.priority > tp.right.priority)
                    tp = self._rotateLeft(tp)
                    tp.left = _recur(tp.left, key)
            return tp

        self.root = _recur(self.root, key)

    def check(self):
        def _recur(tp):
            if tp == None:
                return
            if tp.left:
                assert (tp.priority < tp.left.priority)
            if tp.right:
                assert (tp.priority < tp.right.priority)

        super(Treap, self).check()
        _recur(self.root)


if __name__ == '__main__':
    test = bst.BinarySearchTreeTest(Treap, 1000, True)
    test.deleteMaxMin()
    test.delete()
    print 'done'
