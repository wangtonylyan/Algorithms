# -*- coding: utf-8 -*-
# data structure: splay tree
# Splay operation does rotations along the access path
# and moves the target node all the way up to the root,
# which still preserves the symmetric order of the whole tree.
# 利用splay操作有时可以完成一些其他BST无法做到的行为
# 例如需要删除某个区间(a,b)内所有节点，区间树就很难完成，但对于伸展树而言就很简单
# 将a结点splay至根，将b结点伸展至根的右节点，最后再将b节点的左子树整体删除即可


from bst import SelfAdjustingBinarySearchTree, BinarySearchTreeTest


class SplayTree(SelfAdjustingBinarySearchTree):
    def __init__(self):
        super(SplayTree, self).__init__()

    # Splay操作有两种实现策略：
    # 1) top-down
    # 从树根开始遍历的同时就进行旋转操作，当遍历到目标节点时也就完成了整棵树的伸展
    # 若目标节点不存在，则与目标节点的key较接近的某个叶子节点将成为新的树根
    # 2) bottom-up
    # 从树根开始遍历直至找到目标节点，再将目标节点向上旋转直至树根
    # 需要维护access path信息，无论是使用栈还是父节点指针
    def _splay(self, *args):
        assert (False)


class SplayTreeBottomUp(SplayTree):
    class Node(SplayTree.Node):
        __slots__ = ['parent']

        def __init__(self, key, value, parent):
            super(SplayTreeBottomUp.Node, self).__init__(key, value)
            # bottom-up阶段依赖于子节点至父节点的路径信息，一般有以下两种获取方式
            # 1) 在每次的top-down阶段中，使用临时栈来存储整个access path
            # 2) 每个节点中都维护一个父节点指针，但会增加维护该指针的复杂度
            self.parent = parent

    def __init__(self):
        super(SplayTreeBottomUp, self).__init__()

    def _rotateLeft(self, spt):
        assert (spt and spt.right)
        spt = super(SplayTreeBottomUp, self)._rotateLeft(spt)
        assert (spt.left)
        # 以下需要额外地维护父节点指针，于是一次旋转操作就牵涉到了树中的三个层次
        if spt.left.right:
            spt.left.right.parent = spt.left
        spt.parent = spt.left.parent
        spt.left.parent = spt
        if spt.parent:
            if spt.parent.left is spt.left:
                spt.parent.left = spt
            else:
                assert (spt.parent.right is spt.left)
                spt.parent.right = spt
        return spt

    def _rotateRight(self, spt):
        assert (spt and spt.left)
        spt = super(SplayTreeBottomUp, self)._rotateRight(spt)
        assert (spt.right)
        if spt.right.left:
            spt.right.left.parent = spt.right
        spt.parent = spt.right.parent
        spt.right.parent = spt
        if spt.parent:
            if spt.parent.left is spt.right:
                spt.parent.left = spt
            else:
                assert (spt.parent.right is spt.right)
                spt.parent.right = spt
        return spt

    def _splay(self, spt):
        assert (spt)
        while spt.parent:
            if not spt.parent.parent:
                if spt.parent.left is spt:
                    self._rotateRight(spt.parent)
                else:
                    assert (spt.parent.right is spt)
                    self._rotateLeft(spt.parent)
            elif spt.parent.left is spt:
                if spt.parent.parent.left is spt.parent:  # zig-zig
                    self._rotateRight(spt.parent.parent)
                    self._rotateRight(spt.parent)
                else:  # zig-zag
                    assert (spt.parent.parent.right is spt.parent)
                    self._rotateRight(spt.parent)
                    self._rotateLeft(spt.parent)
            else:
                assert (spt.parent.right is spt)
                if spt.parent.parent.left is spt.parent:  # zig-zag
                    self._rotateLeft(spt.parent)
                    self._rotateRight(spt.parent)
                else:  # zig-zig
                    assert (spt.parent.parent.right is spt.parent)
                    self._rotateLeft(spt.parent.parent)
                    self._rotateLeft(spt.parent)
        self.root = spt

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
        if not iter:
            iter = self.__class__.Node(key, value, prev)
            if prev:
                if iter.key < prev.key:
                    assert (not prev.left)
                    prev.left = iter
                else:
                    assert (iter.key > prev.key)
                    assert (not prev.right)
                    prev.right = iter
        self._splay(iter)
        assert (self.root is iter)

    def delete(self, key):
        spt = self._search(self.root, key)
        if spt:
            assert (spt.key == key)
            self._splay(spt)
            assert (self.root is spt)
            if not self.root.left:
                self.root = self.root.right
            elif not self.root.right:
                self.root = self.root.left
            else:
                m = self._getMax(self.root.left)
                self.root.key = m.key
                self.root.value = m.value
                assert (not m.right)
                if m.parent.left is m:
                    assert (m.parent is self.root)
                    m.parent.left = m.left
                else:
                    assert (m.parent.right is m)
                    m.parent.right = m.left
                if m.left:
                    m.left.parent = m.parent
            if self.root:
                self.root.parent = None

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
                if spt.parent:
                    if spt.parent.left is spt:
                        spt.parent.left = spt.left
                    else:
                        assert (spt.parent.right is spt)
                        spt.parent.right = spt.left
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
                if spt.parent:
                    if spt.parent.left is spt:
                        spt.parent.left = spt.right
                    else:
                        assert (spt.parent.right is spt)
                        spt.parent.right = spt.right
                spt = spt.right
            else:
                spt = None
        return spt

    def _check(self, spt, left, right):
        if spt:
            if spt.left:
                assert (spt is spt.left.parent)
            if spt.right:
                assert (spt is spt.right.parent)
            if spt is self.root:
                assert (not spt.parent)
        return super(SplayTreeBottomUp, self)._check(spt, left, right)


class SplayTreeTopDown(SplayTree):
    def __init__(self):
        super(SplayTreeTopDown, self).__init__()

    def _splay(self, spt):
        # 当前实现是完全基于bottom-up的，如下top-down实现仅作参考
        # push 'root', rather than 'root.child', down until 'spt'
        # strategy: split 'root' subtree into three parts
        def topDown(root, spt):
            assert (root and spt)
            middle = self.__class__.Node(0, 0)
            liter = middle.left
            riter = middle.right
            while root.key != spt.key:
                if spt.key < root.key and root.left:
                    # rotate right
                    if spt.key < root.left.key:
                        root = super(SplayTreeTopDown, self)._rotateRight(root)
                        if root.left is None:
                            break
                    # link right
                    riter.left = root
                    riter = root
                    root = root.left
                elif spt.key > root.key and root.right:
                    # rotate left
                    if spt.key > root.right.key:
                        root = super(SplayTreeTopDown, self)._rotateLeft(root)
                        if root.right is None:
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

        root = topDown(spt, root)
        assert (root is spt)
        return root


if __name__ == '__main__':
    BinarySearchTreeTest(SplayTreeBottomUp, 1000).testcase()
    # BinarySearchTreeTest(SplayTreeTopDown, 1000).testcase()
    print 'done'
