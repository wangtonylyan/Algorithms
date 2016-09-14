# -*- coding: utf-8 -*-
# data structure: splay tree
# 伸展树的特点就是每一次对于树的访问后都要进行一次伸展操作
# 目的是将最近被访问的节点置于更接近树根的位置，以便提高平均访问效率
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

    def split(self, *args):
        assert (False)

    def join(self, *args):
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

    def _splay(self, spt, root):
        assert (spt)
        while spt.parent is not root:
            if not spt.parent.parent or spt.parent.parent is root:
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
        assert (spt.parent is root)
        return spt

    def _searchPattern(self, func, *args):
        assert (callable(func))
        spt = func(self.root, *args)
        assert (not spt or spt.value is not None)
        if spt:
            self.root = self._splay(spt, self.root.parent)
            return spt.value
        return None

    def search(self, key):
        return self._searchPattern(self._search, key)

    def getMax(self):
        return self._searchPattern(self._getMax)

    def getMin(self):
        return self._searchPattern(self._getMin)

    def insert(self, key, value):
        pre = None
        spt = self.root
        while spt:
            if key < spt.key:
                pre = spt
                spt = spt.left
            elif key > spt.key:
                pre = spt
                spt = spt.right
            else:
                spt.value = value
                break
        if not spt:
            spt = self.__class__.Node(key, value, pre)
            if pre:
                if spt.key < pre.key:
                    assert (not pre.left)
                    pre.left = spt
                else:
                    assert (spt.key > pre.key)
                    assert (not pre.right)
                    pre.right = spt
            else:
                self.root = spt
        self.root = self._splay(spt, self.root.parent)

    def delete(self, key):
        spt = self._search(self.root, key)
        if spt:
            assert (spt.key == key)
            self.root = self._splay(spt, self.root.parent)
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
                spt = self._splay(it, spt.parent)
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
                spt = self._splay(it, spt.parent)
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

    def _splay(self, spt, key):
        assert (spt and key is not None)
        # 1) 沿着access path将整棵树分解成左(left)、中(spt)、右(right)三棵子树
        # 其中'left'/'right'连接了access path左/右侧的所有子树，即键值小/大于目标节点的所有子节点
        # [left]  [right]
        #  /.        .\
        #   /.      .\
        #    /.    .\
        # 上图呈现了'left'和'right'子树的形态，其中
        # 点表示link阶段新增的边，即'left.right'和'right.left'
        # 线段表示原本树中已有的边，即access path左右两侧的子树
        # 2) 通过单次rotate操作不断地将局部zig-zig形状的access path调整为zig-zag形状
        # 以期降低'left'和'right'子树的高度，避免整棵树随伸展而退化
        root = self.__class__.Node(None, None)
        left = right = root
        while spt.key != key:
            if key < spt.key:
                if not spt.left:
                    break
                # rotate
                if key < spt.left.key:  # zig-zig
                    spt = self._rotateRight(spt)
                    if not spt.left:
                        break
                # link
                # 在保证下一步访问的是'spt.left'(且其存在)的前提下，将'spt'及其整棵右子树连接至'right'子树
                assert (spt.key > key)
                right.left = spt
                right = right.left
                spt = spt.left
            else:
                assert (key > spt.key)
                if not spt.right:
                    break
                # rotate
                if key > spt.right.key:  # zig-zig
                    spt = self._rotateLeft(spt)
                    if not spt.right:
                        break
                # link
                assert (spt.key < key)
                left.right = spt
                left = left.right
                spt = spt.right
        # assemble
        # 进一步将'spt'子树分解并连接至'left'和'right'子树中
        left.right = spt.left
        right.left = spt.right
        # 将'spt'节点作为树根，即完成对于该节点的伸展
        spt.left = root.right
        spt.right = root.left
        # 'spt.key'与'key'的大小关系不确定，但'spt.left'和'spt.right'的构成则是完全根据'key'来划分的
        assert (not spt.left or spt.left.key < key)
        assert (not spt.right or spt.right.key > key)
        return spt

    def search(self, key):
        self.root = self._search(self.root, key)
        if self.root and self.root.key == key:
            assert (self.root.value is not None)
            return self.root.value
        return None

    def _search(self, spt, key):
        if spt:
            spt = self._splay(spt, key)
        return spt

    def getMax(self):  # not implemented
        assert (False)

    def getMin(self):  # not implemented
        assert (False)

    def insert(self, key, value):
        assert (key is not None and value is not None)
        if not self.root:
            self.root = self.__class__.Node(key, value)
        else:
            self.root = self._splay(self.root, key)
            if self.root.key == key:
                self.root.value = value
            else:
                spt = self.__class__.Node(key, value)
                if self.root.key > key:
                    spt.left = self.root.left
                    self.root.left = None
                    spt.right = self.root
                else:
                    assert (self.root.key < key)
                    spt.right = self.root.right
                    self.root.right = None
                    spt.left = self.root
                self.root = spt

    def delete(self, key):
        if self.root:
            self.root = self._splay(self.root, key)
            if self.root.key == key:
                if not self.root.left:
                    self.root = self.root.right
                else:
                    self.root.left = self._splay(self.root.left, key)
                    assert (not self.root.left.right)
                    self.root.left.right = self.root.right
                    self.root = self.root.left

    def deleteMax(self):  # not implemented
        assert (False)

    def deleteMin(self):  # not implemented
        assert (False)


if __name__ == '__main__':
    BinarySearchTreeTest(SplayTreeBottomUp, 1000).testcase()
    BinarySearchTreeTest(SplayTreeTopDown, 2000).delete()
    print 'done'
