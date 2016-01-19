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

    # no side-effect
    @staticmethod
    def _skew(aat):  # == RBT._rotateRight
        assert (aat and aat.left)
        assert (aat.level == aat.left.level)
        ret = aat.left
        aat.left = ret.right
        ret.right = aat
        return ret

    # side-effect: increase height of aat subtree
    @staticmethod
    def _split(aat):  # == RBT._rotateLeft + RBT._flipColor
        assert (aat and aat.right and aat.right.right)
        assert (aat.level == aat.right.level == aat.right.right.level)
        ret = aat.right
        aat.right = ret.left
        ret.left = aat
        ret.level += 1
        return ret

    @classmethod
    def _balance(cls, aat):
        assert (aat)
        if aat.left and aat.level == aat.left.level:
            aat = cls._skew(aat)
        if aat.right and aat.right.right and aat.level == aat.right.right.level:
            assert(aat.level == aat.right.level)
            aat = cls._split(aat)
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

    @staticmethod
    def _lower(aat):
        assert(aat)
        m = min(aat.left.level if aat.left else 0, aat.right.level if aat.right else 0) + 1
        if m < aat.level:
            aat.level = m
            if aat.right and m < aat.right.level:
                aat.right.level = m
        return aat

    @classmethod
    def _bal(aat):
        if aat.left and aat.left.level == aat.level:
            aat = self._skew(aat)
        if aat.right and aat.right.left and aat.right.left.level == aat.right.level:
            aat.right = self._skew(aat.right)
        if aat.right and aat.right and aat.right.left and aat.right.left.level == aat.right.level:
            aat.right.right = self._skew(aat.right.right)


    def delete(self, key):
        def _recur(aat, key):
            if aat == None:
                return aat #deletion failed
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
                    aat = self._lower(aat)
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
            _recur(aat.left)
            _recur(aat.right)
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
                # 隐式特征
                # every node of level greater than one must have two children
                assert(aat.left and aat.right)

        super(AAT, self).check()
        _recur(self.root)


if __name__ == '__main__':
    test = bst.BSTTest(AAT, 1000, True)
    test.new()
    test.deleteMaxMin()
    test.delete()
    print 'done'
