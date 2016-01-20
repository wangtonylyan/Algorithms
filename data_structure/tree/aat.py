# -*- coding: utf-8 -*-
# data structure: AA (Arne Andersson) tree

import bst


class AAT(bst.BST):
    class Node:
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.level = 1

    def __init__(self):
        super(AAT, self).__init__()

    # 相比于red-black tree的rotateLeft、rotateRight和flipColor三个基本操作而言
    # 用于平衡AAT的两个基本操作skew和split是复合的，包含了条件判断
    # 该AAT的删除实现区别于其他RBT在于，没有在top-down阶段预先准备，
    # 而是在bottom-up阶段重新平衡，这就对balance函数的实现要求更高

    # no side-effect
    @staticmethod
    def _skew(aat):
        assert (aat)
        if aat.left and aat.level == aat.left.level:
            # == RBT._rotateRight
            ret = aat.left
            aat.left = ret.right
            ret.right = aat
            aat = ret
        return aat

    # side-effect: increase height of aat subtree
    @staticmethod
    def _split(aat):
        assert (aat)
        if aat.right and aat.right.right and aat.level == aat.right.right.level:
            # == RBT._rotateLeft + RBT._flipColor
            assert (aat.level == aat.right.level == aat.right.right.level)
            ret = aat.right
            aat.right = ret.left
            ret.left = aat
            ret.level += 1
            aat = ret
        return aat

    # insertion: b + c
    # deletion: a + b + c
    @classmethod
    def _balance(cls, aat):
        assert (aat)
        # a) decrease level
        # if one of aat.left and aat.right subtree is lower after modification, correct aat subtree's level
        m = min(aat.left.level if aat.left else 0, aat.right.level if aat.right else 0) + 1
        if m < aat.level:
            aat.level = m
            if aat.right and m < aat.right.level:
                # assert aat and aat.right node were viewed as a single pseudo-node
                aat.right.level = m
        # b) skew
        aat = cls._skew(aat)
        if aat.right:
            aat.right = cls._skew(aat.right)
        if aat.right and aat.right.right:
            aat.right.right = cls._skew(aat.right.right)
        # c) split
        aat = cls._split(aat)
        if aat.right:
            aat.right = cls._split(aat.right)
        return aat

    def insert(self, key, value):
        def _recur(aat, key, value):
            if aat == None:
                return self.__class__.Node(key, value)
            if key < aat.key:
                aat.left = _recur(aat.left, key, value)
                aat = self._skew(aat)
                aat = self._split(aat)
#                aat = self._balance(aat)
            elif key > aat.key:
                aat.right = _recur(aat.right, key, value)
                aat = self._skew(aat)
                aat = self._split(aat)
#                aat = self._balance(aat)
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
