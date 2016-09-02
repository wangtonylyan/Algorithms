# -*- coding: utf-8 -*-
# data structure: AA (Arne Andersson) tree
# AA树可被视为是一种简化版的"右倾"红黑树
# 每个节点中维护的level综合了AVL树和红黑树的特性

from bst import BalancedBinarySearchTree, BinarySearchTreeTest


class AATree(BalancedBinarySearchTree):
    class Node():
        def __init__(self, key, value):
            self.left = None
            self.right = None
            self.key = key
            self.value = value
            self.level = 1

    def __init__(self):
        super(AATree, self).__init__()

    # ------------------------------------------------------------------------------------

    # AA树相对于红黑树而言的几点区别：
    # 1) 用于平衡AA树的两个基本操作skew和split的当前实现是复合且递归的
    # 虽然实际情况下，真正有效的递归深度都很浅，详见于_balance()，但执行上仍会递归至叶子节点
    # 2) 删除过程中，没有top-down的预先准备，而仅仅在bottom-up时重新平衡
    # 这会增加balance操作的复杂度，详见于_balance_insert()和_balance_delete()
    # 但实现上若基于递归版本的skew和split操作，则又恰好能有效地避免之，详见于_balance()

    # == rotateRight: no side-effect
    def _skew(self, aat):
        if aat:
            if aat.left and aat.left.level == aat.level:
                aat = self._rotateRight(aat)  # results in the side-effect of turning 'aat.left.right' into left
            aat.right = self._skew(aat.right)  # recursion will eliminate the side-effect
        return aat

    # == rotateLeft + flipColor: increasing level of 'aat' subtree
    def _split(self, aat):
        if aat:
            if aat.right and aat.right.right and aat.level == aat.right.right.level:
                assert (aat.level == aat.right.level == aat.right.right.level)
                aat = self._rotateLeft(aat)
                aat.level += 1
            aat.right = self._split(aat.right)
        return aat

    def _balance(self, aat):
        # b+c组合之所以能重新平衡结构被破坏了的AA树在于：
        # 递归的skew操作使得所有左倾结构都被转换成了右倾
        # 递归的split操作又通过增加树的层次来消除多余的右倾
        # 实际上，skew的有效递归至多三次，split的有效递归至多两次
        # 即在deletion操作中，存在如下最坏情况（6个节点全在相同层次上）
        #   a
        #    \
        #     b
        #    / \
        #   c   d
        #    \   \
        #     e   f
        # a的左子树由于降低了层次，使得节点a和b也同时降低层次
        # 且原本c与e、d与f就在同一个层次上
        assert (aat)
        # a) decrease 'aat' level as much as possible
        # actually it's only useful for deletion in case that one of aat subtrees is lower
        m = min(aat.left.level if aat.left else 0, aat.right.level if aat.right else 0) + 1
        if aat.level > m:
            assert (aat.level == m + 1)
            aat.level = m
            if aat.right and aat.right.level > m:
                # 'aat' and 'aat.right' were viewed as a single pseudo-node
                aat.right.level = m
        # b) go along the right path and skew
        aat = self._skew(aat)
        # c) go along the right path and split
        aat = self._split(aat)
        return aat

    # ------------------------------------------------------------------------------------

    # worst case scenario:
    #    a    a
    #   / \    \
    #  b   c    b
    #            \
    #             c
    def _balance_insert(self, aat):
        assert (aat)
        if aat.left and aat.left.level == aat.level:
            aat = self._rotateRight(aat)
            assert (aat.level == aat.right.level)
        if aat.right and aat.right.right and aat.right.right.level == aat.level:
            assert (aat.level == aat.right.level == aat.right.right.level)
            aat = self._rotateLeft(aat)
            assert (aat.level == aat.left.level == aat.right.level)
            aat.level += 1
        return aat

    def insert(self, key, value):
        def recur(aat, key, value):
            if aat == None:
                return self.__class__.Node(key, value)
            if key < aat.key:
                aat.left = recur(aat.left, key, value)
                # aat = self._balance(aat)  # or
                aat = self._balance_insert(aat)
            elif key > aat.key:
                aat.right = recur(aat.right, key, value)
                # aat = self._balance(aat)  # or
                aat = self._balance_insert(aat)
            else:
                aat.value = value
            return aat

        self.root = recur(self.root, key, value)

    # ------------------------------------------------------------------------------------

    def _balance_delete(self, aat):
        assert (aat)
        if aat.left and aat.level - aat.left.level > 1:  # deleted from left subtree
            aat.level -= 1
            if aat.right and aat.right.level > aat.level:
                aat.right.level -= 1
            assert (aat.level == aat.right.level)
        elif aat.right and aat.level - aat.right.level > 1:  # deleted from right subtree
            aat.level -= 1
            assert (aat.level == aat.left.level)
        # TODO
        return aat

    def _deleteMax(self, aat):
        if aat:
            if aat.right:
                aat.right = self._deleteMax(aat.right)
                # aat = self._balance(aat)  # or
                aat = self._balance_delete(aat)
            else:
                aat = aat.left
        return aat

    def _deleteMin(self, aat):
        if aat:
            if aat.left:
                aat.left = self._deleteMin(aat.left)
                # aat = self._balance(aat)  # or
                aat = self._balance_delete(aat)
            else:
                aat = aat.right
        return aat

    def delete(self, key):
        def _recur(aat, key):
            if aat == None:
                return aat
            if key < aat.key:
                aat.left = _recur(aat.left, key)
                # aat = self._balance(aat)  # or
                aat = self._balance_delete(aat)
            elif key > aat.key:
                aat.right = _recur(aat.right, key)
                # aat = self._balance(aat)  # or
                aat = self._balance_delete(aat)
            else:
                if aat.right:
                    m = self._getMin(aat.right)
                    aat.right = self._deleteMin(aat.right)
                    assert (not self._search(aat.right, m.key))
                    aat.key = m.key
                    aat.value = m.value
                    # aat = self._balance(aat)  # or
                    aat = self._balance_delete(aat)
                elif aat.left:
                    aat = aat.left
                else:
                    assert (aat.level == 1)
                    aat = None
            return aat

        self.root = _recur(self.root, key)

    # ------------------------------------------------------------------------------------

    def _check(self, aat, left, right):
        if aat:
            if aat.left:
                # level of a left child is strictly less than that of its parent
                assert (aat.left.level < aat.level)
            if aat.right:
                # level of a right child is less than or equal to that of its parent
                assert (aat.right.level <= aat.level)
                if aat.right.right:
                    # level of a right grandchild is strictly less than that of its grandparent
                    assert (aat.right.right.level < aat.level)
            if aat.left == None and aat.right == None:
                # level of a leaf node is one
                assert (aat.level == 1)
            if aat.level > 1:
                # 隐式特征: every node of level greater than one must have two children
                assert (aat.left and aat.right)
        # 无需像红黑树那样统计左右子树的black height，因为level信息就已包含了
        return super(AATree, self)._check(aat, left, right)


if __name__ == '__main__':
    BinarySearchTreeTest(AATree, 2000).testcase()
    print 'done'
