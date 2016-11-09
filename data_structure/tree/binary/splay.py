# -*- coding: utf-8 -*-
# data structure: splay tree
# 伸展树的特点就是每一次对于树的访问后都要进行一次伸展操作
# 目的是将最近被访问的节点置于更接近树根的位置，以便提高平均访问效率
# 利用splay操作有时可以完成一些其他BST无法做到的行为
# 例如需要删除某个区间(a,b)内所有节点，区间树就很难完成，但对于伸展树而言就很简单
# 将a结点splay至根，将b结点伸展至根的右节点，最后再将b节点的左子树整体删除即可
# In 2000, Danny Sleator and Robert Tarjan won the ACM Kanellakis Theory and
# Practice Award for their papers on splay trees and amortized analysis.

from bst import SelfAdjustingBinarySearchTree, BinarySearchTreeTest


class SplayTree(SelfAdjustingBinarySearchTree):
    def __init__(self):
        super(SplayTree, self).__init__()
        self._search = self._splay

    # 1) splay操作有两种实现策略：
    # (a) top-down
    # 从树根开始遍历的同时就进行旋转操作，当遍历到目标节点时也就完成了整棵树的伸展
    # 若目标节点不存在，则与目标节点的key较接近的某个叶子节点将成为新的树根
    # (b) bottom-up
    # 从树根开始遍历直至找到目标节点，再将目标节点向上旋转直至树根
    # 需要维护access path信息，无论是使用栈/递归还是父节点指针
    # 2) 由原始论文中的描述，"将目标节点伸展至树根"的思想并不是伸展树所开创的
    # 但该树的与众不同之处就在于，其旋转是成双成对的(以降低平均的时间复杂度)：
    # 即根据zig-zig或zig-zag(而不是单个zig)来决定对于目标节点的伸展方式
    # 3) 如下所示，编程实现中，对于zig-zag形状的讨论常被蕴含于整个循环或递归逻辑中，而无需单独处理
    def _splay(self, spt, key):
        assert (False)

    def search(self, key):
        self.root = self._search(self.root, key)
        assert (not self.root or (self.root.key is not None and
                                  self.root.value is not None))
        return self.root.value if self.root and self.root.key == key else None

    def getMax(self):
        self.root = self._getMax(self.root)
        assert (not self.root or (self.root.key is not None and
                                  self.root.value is not None))
        return (self.root.key, self.root.value) if self.root else None

    def getMin(self):
        self.root = self._getMin(self.root)
        assert (not self.root or (self.root.key is not None and
                                  self.root.value is not None))
        return (self.root.key, self.root.value) if self.root else None

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
                elif not self.root.right:
                    self.root = self.root.left
                else:
                    self.root.left = self._splay(self.root.left, key)
                    assert (not self.root.left.right)
                    self.root.left.right = self.root.right
                    self.root = self.root.left

    def _deleteMax(self, spt):
        if not spt:
            return spt
        spt = self._getMax(spt)
        assert (not spt.right)
        return spt.left

    def _deleteMin(self, spt):
        if not spt:
            return spt
        spt = self._getMin(spt)
        assert (not spt.left)
        return spt.right


class SplayTreeTopDown(SplayTree):
    def __init__(self):
        super(SplayTreeTopDown, self).__init__()

    def _splay(self, spt, key):
        if not spt:
            return spt
        # 1) 沿着access path将整棵树分解成左(left)、中(spt)、右(right)三棵子树
        # 其中'left'/'right'连接了access path左/右侧的所有子树，即键值小/大于目标节点的所有子节点
        # [left]  [right]
        #  /.        .\
        #   /.      .\
        #    /.    .\
        # 上图呈现了'left'和'right'子树的形态，其中
        # 点表示link阶段新增的边，即'left.right'和'right.left'
        # 线段表示原本树中已有的边，即access path左右两侧的子树
        # 2) 消除沿access path出现的zig-zig形状，而zig-zag形状则被自然地分解至了'left'和'right'子树中
        root = self.__class__.Node(None, None)
        left = right = root
        while spt.key != key:
            if key < spt.key:
                if not spt.left:
                    break
                # rotate
                if key < spt.left.key:  # zig-zig
                    spt = self._rotateRight_(spt)
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
                    spt = self._rotateLeft_(spt)
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

    def _getMax(self, spt):
        if spt:
            root = self.__class__.Node(None, None)
            left = root
            while spt.right:
                if spt.right.right:
                    spt = self._rotateLeft_(spt)
                spt = self._rotateLeft_(spt)
                if spt.right:
                    left.right = spt
                    left = left.right
                    spt = spt.right
            left.right = spt.left
            spt.left = root.right
        return spt

    def _getMin(self, spt):
        if spt:
            root = self.__class__.Node(None, None)
            right = root
            while spt.left:
                if spt.left.left:
                    spt = self._rotateRight_(spt)
                spt = self._rotateRight_(spt)
                if spt.left:
                    right.left = spt
                    right = right.left
                    spt = spt.left
            right.left = spt.right
            spt.right = root.left
        return spt


class SplayTreeBottomUp(SplayTree):
    def __init__(self):
        super(SplayTreeBottomUp, self).__init__()

    def _splay(self, spt, key):
        if not spt:
            return spt
        if key < spt.key and spt.left:
            if key < spt.left.key:  # zig-zig
                spt.left.left = self._splay(spt.left.left, key)
                spt = self._rotateRight_(spt)
                if spt.left:
                    spt = self._rotateRight_(spt)
            # elif key > spt.left.key:  # zig-zag
            #    spt.left.right = self._splay(spt.left.right, key)
            #    if spt.left.right:
            #        spt.left = self._rotateLeft_(spt.left)
            #    spt = self._rotateRight_(spt)
            else:
                spt.left = self._splay(spt.left, key)
                spt = self._rotateRight_(spt)
        elif key > spt.key and spt.right:
            if key > spt.right.key:  # zig-zig
                spt.right.right = self._splay(spt.right.right, key)
                spt = self._rotateLeft_(spt)
                if spt.right:
                    spt = self._rotateLeft_(spt)
            # elif key < spt.right.key:  # zig-zag
            #    spt.right.left = self._splay(spt.right.left, key)
            #    if spt.right.left:
            #        spt.right = self._rotateRight_(spt.right)
            #    spt = self._rotateLeft_(spt)
            else:
                spt.right = self._splay(spt.right, key)
                spt = self._rotateLeft_(spt)
        assert (not spt.left or spt.left.key < key)
        assert (not spt.right or spt.right.key > key)
        return spt

    def _getMax(self, spt):
        if spt and spt.right:
            spt.right.right = self._getMax(spt.right.right)
            spt = self._rotateLeft_(spt)
            if spt.right:
                spt = self._rotateLeft_(spt)
        return spt

    def _getMin(self, spt):
        if spt and spt.left:
            spt.left.left = self._getMin(spt.left.left)
            spt = self._rotateRight_(spt)
            if spt.left:
                spt = self._rotateRight_(spt)
        return spt


if __name__ == '__main__':
    BinarySearchTreeTest(SplayTreeTopDown).testcase()
    BinarySearchTreeTest(SplayTreeBottomUp).testcase()
    print 'done'
