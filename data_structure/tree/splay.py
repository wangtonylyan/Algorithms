# -*- coding: utf-8 -*-
# data structure: splay tree

import bst


# does rotations bottom-up along the access path and moves the accessed item all the way to the root.
# splay operation should preserve the symmetric order
# which means spt.parent should still be the same side of spt after rotation

class Splay(bst.BBST):
    class Node():
        def __init__(self, key, value, parent):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            # 该属性使得平衡算法的实现得到了简化
            # 但对于其自身的维护也增加了额外的复杂度
            self.parent = parent
            if self.parent:
                if self.key < self.parent.key:
                    self.parent.left = self
                else:
                    assert (self.key > self.parent.key)
                    self.parent.right = self

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
        self._splay(iter)


if __name__ == '__main__':
    test = bst.BSTTest(Splay, 1000, True)
    test.new()
    #    test.deleteMaxMin()
    #    test.delete()
    print 'done'
