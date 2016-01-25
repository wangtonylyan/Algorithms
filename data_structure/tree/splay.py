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


class SplayTree(bst.BalancedBinarySearchTree):
    class Node(object):
        def __init__(self, key, value, parent):
            self.left = None
            self.right = None
            self.parent = parent  # 该属性简化了平衡算法，但对于其自身的维护也增加了额外的复杂度
            self.key = key
            self.value = value

    def __init__(self):
        super(SplayTree, self).__init__()

    def _rotateLeft(self, spt):
        assert (spt and spt.right)
        spt = super(SplayTree, self)._rotateLeft(spt)
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
        spt = super(SplayTree, self)._rotateRight(spt)
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

    # Splay操作有两种实现策略：
    # 1）top down
    # 从树根开始遍历的同时就进行旋转操作，当遍历到目标节点时也就完成了整棵树的伸展
    # 若目标节点不存在，则与目标节点的key较接近的某个叶子节点将成为新的树根
    # 2）bottom up
    # 从树根开始遍历直至找到目标节点，再将目标节点向上旋转直至树根
    # 需要维护access path信息，无论是使用栈还是parent指针
    def _splay(self, spt, root):
        # 本数据结构是完全基于bottom up的，因此top down的实现仅作参考
        # push root, rather than root.child, down until spt
        # strategy: split root subtree into three parts
        def _top_down(root, spt):
            middle = self.__class__.Node(0, 0, 0)
            liter = middle.left
            riter = middle.right
            while root.key != spt.key:
                if spt.key < root.key and root.left:
                    # rotate right
                    if spt.key < root.left.key:
                        root = super(Splay, self)._rotateRight(root)
                        if root.left == None:
                            break
                    # link right
                    riter.left = root
                    riter = root
                    root = root.left
                elif spt.key > root.key and root.right:
                    # rotate left
                    if spt.key > root.right.key:
                        root = super(Splay, self)._rotateLeft(root)
                        if root.right == None:
                            break
                    # link left
                    liter.right = root
                    liter = root
                    root = root.right
                else:
                    break
            # assemble
            liter.right = root.left
            riter.left = root.right
            root.left = middle.right
            root.right = middle.left
            return root

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

    def _deleteMax(self, spt):
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

    def _deleteMin(self, spt):
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
        def _recur(spt):
            if spt:
                if spt.left:
                    assert (spt.left.parent == spt)
                    _recur(spt.left)
                if spt.right:
                    assert (spt.right.parent == spt)
                    _recur(spt.right)

        super(SplayTree, self).check()
        _recur(self.root)
        assert (not (self.root and self.root.parent))


if __name__ == '__main__':
    test = bst.BinarySearchTreeTest(SplayTree, 800, True)
    test.deleteMaxMin()
    test.delete()
    print 'done'
