# -*- coding: utf-8 -*-
# data structure: AA (Arne Andersson) tree

import bst


class AAT(bst.BBST):
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.level = 1

    def __init__(self):
        super(AAT, self).__init__()

    # 1）相比于red-black tree的三个基本操作而言，用于平衡AAT的两个基本操作
    # skew和split是复合（包含了条件判断）且递归的
    # 2）以下的删除实现方式区别于其他RBT在于，没有top-down阶段的预先准备，
    # 而仅仅在bottom-up阶段重新平衡，这就增加了balance的复杂度
    # 但由于AA树自身的特性以及skew/split的递归，恰好又使得其极易实现

    # same as RBT.rotateRight: no side-effect
    def _skew(self, aat):
        if aat:
            if aat.left and aat.level == aat.left.level:
                aat = self._rotateRight(aat)
            aat.right = self._skew(aat.right)
        return aat

    # same as RBT.rotateLeft + RBT.flipColor: side-effect of increasing height of aat subtree
    def _split(self, aat):
        if aat:
            if aat.right and aat.right.right and aat.level == aat.right.right.level:
                assert (aat.level == aat.right.level == aat.right.right.level)
                aat = self._rotateLeft(aat)
                aat.level += 1
            aat.right = self._split(aat.right)
        return aat

    def _balance(self, aat):
        assert (aat)
        # a) decrease level (only in deletion)
        # in case that one of aat.left and aat.right subtree is lower
        m = min(aat.left.level if aat.left else 0, aat.right.level if aat.right else 0) + 1
        if aat.level > m:
            aat.level = m
            if aat.right and aat.right.level > m:
                # assert aat and aat.right node were viewed as a single pseudo-node
                aat.right.level = m
        # b) go along the right path and skew
        aat = self._skew(aat)
        # c) go along the right path and split
        aat = self._split(aat)
        return aat

    def insert(self, key, value):
        def _recur(aat, key, value):
            if aat == None:
                return self.__class__.Node(key, value)
            if key < aat.key:
                aat.left = _recur(aat.left, key, value)
                aat = self._balance(aat)
            elif key > aat.key:
                aat.right = _recur(aat.right, key, value)
                aat = self._balance(aat)
            else:
                aat.value = value
            return aat

        self.root = _recur(self.root, key, value)

    def delete(self, key):
        def _recur(aat, key):
            if aat == None:
                return aat
            if key < aat.key:
                aat.left = _recur(aat.left, key)
                aat = self._balance(aat)
            elif key > aat.key:
                aat.right = _recur(aat.right, key)
                aat = self._balance(aat)
            else:
                if aat.right:
                    m = self._getMin(aat.right)
                    aat.right = _recur(aat.right, m.key)
                    aat.key = m.key
                    aat.value = m.value
                    aat = self._balance(aat)
                elif aat.left:
                    aat = aat.left
                else:
                    aat = None
            return aat

        self.root = _recur(self.root, key)

    def check(self):
        def _recur(aat):
            if aat == None:
                return
            m = _recur(aat.left)
            n = _recur(aat.right)
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

        super(AAT, self).check()
        _recur(self.root)


if __name__ == '__main__':
    test = bst.BSTTest(AAT, 400, True)
    test.new()
    #    test.deleteMaxMin()
    test.delete()
    print 'done'
