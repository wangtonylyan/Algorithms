# -*- coding: utf-8 -*-
# data structure: splay tree
# 伸展树的核心是围绕splay操作
# Splay operation does rotations bottom-up along the access path
# and moves the accessed node all the way up to the root,
# which still preserves the symmetric order of the whole tree.
# 利用splay操作有时可以完成一些其他BST无法做到的行为
# 例如需要删除某个区间(a,b)内所有节点，区间树就很难完成，但对于伸展树而言就很简单
# 将a结点splay至根，将b结点伸展至根的右节点，最后再将b节点的左子树整体删除即可

import bst


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

    def _splay(self, spt, root):
        # push spt up until root.child
        def _bottom_up(spt, root):
            while spt.parent != root:
                assert (spt.parent)
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

        assert (spt)
        return _bottom_up(spt, root)

    def _balance(self, spt):
        assert (spt)
        self.root = self._splay(spt, None)
        assert (self.root.key == spt.key)

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
        self._balance(iter)

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
        spt = self._search(self.root, key)
        if spt:
            assert (spt.key == key)
            self._balance(spt)
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
        assert (not (self.root and self.root.parent))


if __name__ == '__main__':
    test = bst.BSTTest(Splay, 800, True)
    test.deleteMaxMin()
    test.delete()
    print 'done'
