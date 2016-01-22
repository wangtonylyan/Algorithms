# -*- coding: utf-8 -*-
# data structure: splay tree

import bst


# does rotations bottom-up along the access path and moves the accessed item all the way to the root.
# splay operation should preserve the symmetric order
# which means spt.parent node should still be the same side of spt node after rotation

class Splay(bst.BBST):
    class Node():
        def __init__(self, key, value, parent):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.parent = parent  # 该属性简化了平衡算法，但对于其自身的维护也增加了额外的复杂度

    def __init__(self):
        super(Splay, self).__init__()

    def _rotateLeft(self, spt):
        assert (spt and spt.right)
        spt = super(Splay, self)._rotateLeft(spt)
        assert (spt.left)
        if spt.left.right:
            spt.left.right.parent = spt.left
        spt.parent = spt.left.parent
        spt.left.parent = spt
        if spt.parent:
            if spt.parent.left == spt.left:
                spt.parent.left = spt
            else:
                assert (spt.parent.right == spt.left)
                spt.parent.right = spt
        return spt

    def _rotateRight(self, spt):
        assert (spt and spt.left)
        spt = super(Splay, self)._rotateRight(spt)
        assert (spt.right)
        if spt.right.left:
            spt.right.left.parent = spt.right
        spt.parent = spt.right.parent
        spt.right.parent = spt
        if spt.parent:
            if spt.parent.left == spt.right:
                spt.parent.left = spt
            else:
                assert (spt.parent.right == spt.right)
                spt.parent.right = spt
        return spt

    def _splay(self, spt):
        def _top_down(spt):
            pass

        def _bottom_up(spt):
            while spt.parent:
                if spt.parent.parent:
                    if spt == spt.parent.left and spt.parent == spt.parent.parent.left:
                        spt.parent = self._rotateRight(spt.parent.parent)
                        spt = self._rotateRight(spt.parent)
                    elif spt == spt.parent.left and spt.parent == spt.parent.parent.right:
                        spt = self._rotateRight(spt.parent)
                        spt = self._rotateLeft(spt.parent)
                    elif spt == spt.parent.right and spt.parent == spt.parent.parent.left:
                        spt = self._rotateLeft(spt.parent)
                        spt = self._rotateRight(spt.parent)
                    else:
                        assert (spt == spt.parent.right and spt.parent == spt.parent.parent.right)
                        spt.parent = self._rotateLeft(spt.parent.parent)
                        spt = self._rotateLeft(spt.parent)
                else:
                    if spt == spt.parent.left:
                        spt = self._rotateRight(spt.parent)
                    else:
                        assert (spt == spt.parent.right)
                        spt = self._rotateLeft(spt.parent)
            return spt

        self.root = _bottom_up(spt)

    def _access(self, key):
        iter = self.root
        while iter:
            if key < iter.key:
                iter = iter.left
            elif key > iter.key:
                iter = iter.right
            else:
                self._splay(iter)
                break

    def insert(self, key, value):
        prev = None
        iter = self.root
        while iter:
            if key < iter.key:
                prev = iter
                iter = iter.left
            elif key > iter.key:
                prev = iter
                iter = iter.right
            else:
                iter.value = value
                break
        if iter == None:
            iter = self.__class__.Node(key, value, prev)
            if prev:
                if iter.key < prev.key:
                    prev.left = iter
                else:
                    assert (iter.key > prev.key)
                    prev.right = iter
        self._splay(iter)

    @staticmethod
    def _deleteMax(spt):
        if spt:
            if spt.right:
                it = spt
                while it.right.right:
                    it = it.right
                it.right = it.right.left
                if it.right:
                    it.right.parent = it
            elif spt.left:
                spt.left.parent = spt.parent
                spt = spt.left
            else:
                spt = None
        return spt

    @staticmethod
    def _deleteMin(spt):
        if spt:
            if spt.left:
                it = spt
                while it.left.left:
                    it = it.left
                it.left = it.left.right
                if it.left:
                    it.left.parent = it
            elif spt.right:
                spt.right.parent = spt.parent
                spt = spt.right
            else:
                spt = None
        return spt

    def delete(self, key):
        self._access(key)
        if self.root and self.root.key == key:  # find it
            if self.root.left:
                m = self._getMax(self.root.left)
                self.root.left = self._deleteMax(self.root.left)
                self.root.key = m.key
                self.root.value = m.value
            elif self.root.right:
                self.root = self.root.right
                self.root.parent = None
            else:
                self.root = None

    def check(self):
        super(Splay, self).check()
        if self.root:
            assert (self.root.parent == None)


if __name__ == '__main__':
    test = bst.BSTTest(Splay, 800, True)
    test.new()
    test.deleteMaxMin()
    test.delete()
    print 'done'
