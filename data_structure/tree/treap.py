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
        # 利用该数组来维护priority的唯一性，也有算法在实现上会利用哈希表
        self.prioritySet = [0 for i in range(self.total)]

    def _balance(self, tp):
        assert (tp)
        if tp.left and tp.left.priority < tp.priority:
            tp = self._rotateRight(tp)
        elif tp.right and tp.right.priority < tp.priority:
            tp = self._rotateLeft(tp)
        return tp

    def insert(self, key, value):
        def _recur(tp, key, value):
            if tp == None:
                priority = random.randint(0, self.total)
                while self.prioritySet[priority]:
                    # 不能直接搜索prioritySet数组，并使用下一个未被标识的数
                    # 因为这样不够随机
                    priority = random.randint(0, self.total)
                self.prioritySet[priority] = 1
                return self.__class__.Node(key, value, priority)  # insertion
            if key < tp.key:
                tp.left = _recur(tp.left, key, value)
                tp = self._balance(tp)
            elif key > tp.key:
                tp.right = _recur(tp.right, key, value)
                tp = self._balance(tp)
            else:
                tp.value = value
            return tp

        self.root = _recur(self.root, key, value)

    # 删除操作只需在top-down阶段不断地将目标节点进行旋转
    # 直至其成为叶子节点，并删除即可
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
                elif tp.left.priority < tp.right.priority:  # 维护最小堆的性质
                    tp = self._rotateRight(tp)
                    tp.right = _recur(tp.right, key)
                else:
                    assert (tp.left.priority > tp.right.priority)
                    tp = self._rotateLeft(tp)
                    tp.left = _recur(tp.left, key)
            return tp

        self.root = _recur(self.root, key)

    def _check(self, tp, left, right):
        super(Treap, self)._check(tp, left, right)
        # check heap order property
        if tp.left:
            assert (tp.priority < tp.left.priority)
        if tp.right:
            assert (tp.priority < tp.right.priority)


if __name__ == '__main__':
    test = bst.BinarySearchTreeTest(Treap, 1000, True)
    test.deleteMaxMin()
    test.delete()
    print 'done'
