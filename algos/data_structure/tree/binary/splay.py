# -*- coding: utf-8 -*-
# data structure: splay tree
# 伸展树的特点就是每一次对于树的访问后都要进行一次伸展操作
# 目的是将最近被访问的节点置于更接近树根的位置，以便提高平均访问效率
# 利用splay操作有时可以完成一些其他BST无法做到的行为
# 例如需要删除某个区间(a,b)内所有节点，区间树就很难完成，但对于伸展树而言就很简单
# 将a结点splay至根，将b结点伸展至根的右节点，最后再将b节点的左子树整体删除即可
# In 2000, Danny Sleator and Robert Tarjan won the ACM Kanellakis Theory and
# Practice Award for their papers on splay trees and amortized analysis.


from algos.data_structure.tree.binary.bst import SelfAdjustingBinarySearchTree


class SplayTree(SelfAdjustingBinarySearchTree):
    def search(self, key):
        assert key is not None
        self.root = self._search(self.root, key)
        return self.root.value if self.root and self.root.cmp(key) == 0 else None

    def getmax(self):
        self.root = self._getmax(self.root)
        return (self.root.key, self.root.value) if self.root else None

    def getmin(self):
        self.root = self._getmin(self.root)
        return (self.root.key, self.root.value) if self.root else None

    def _search(self, tree, key):
        return self._splay_(tree, key) if tree else tree

    def _getmax(self, tree):
        return self._splay_max_(tree) if tree else tree

    def _getmin(self, tree):
        return self._splay_min_(tree) if tree else tree

    def _insert(self, tree, key, value):
        if tree:
            tree = self._splay_(tree, key)
            cmp = tree.cmp(key)
            if cmp == 0:
                tree.value = value
            else:
                root = self.__class__.Node(key, value)
                if cmp < 0:
                    root.left = tree.left
                    tree.left = None
                    root.right = tree
                else:
                    root.right = tree.right
                    tree.right = None
                    root.left = tree
                tree = root
        else:
            tree = self.__class__.Node(key, value)
        return tree

    def _delete(self, tree, key):
        if tree:
            tree = self._splay_(tree, key)
            cmp = tree.cmp(key)
            if cmp == 0:
                if not tree.left:
                    tree = tree.right
                elif not tree.right:
                    tree = tree.left
                else:
                    tree.left = self._splay_(tree.left, key)
                    assert not tree.left.right
                    tree.left.right = tree.right
                    tree = tree.left
        return tree

    def _delmax(self, tree):
        return self._getmax(tree).left if tree else tree

    def _delmin(self, tree):
        return self._getmin(tree).right if tree else tree

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
    def _splay_(self, tree, key):
        assert False

    def _splay_max_(self, tree):
        assert False

    def _splay_min_(self, tree):
        assert False


class SplayTreeTopDown(SplayTree):
    # 1) 沿着access path将整棵树分解成左(left)、中(spt)、右(right)三棵子树
    # 其中'left/right'分别连接了access path左/右侧的所有子树，即键值小/大于key的所有节点
    # [left]  [right]
    #  /.        .\
    #   /.      .\
    #    /.    .\
    # 上图呈现了'left'和'right'子树的形态，其中
    # 点表示link阶段新增的边，即'left.right'和'right.left'
    # 线段表示原本树中已有的边，即access path左右两侧的子树
    # 2) 消除沿access path出现的zig-zig形状，而zig-zag形状则被自然地分解至了'left'和'right'子树中
    def _splay_(self, tree, key):
        root = self.__class__.Node(None, None)
        left = right = root
        cmp = tree.cmp(key)
        while cmp:
            if cmp < 0:
                if not tree.left:
                    break
                if tree.left.cmp(key) < 0:
                    # rotate right to eliminate 'tree.left'+'tree.left.left' zig-zig
                    tree = self._rotate_right_(tree)
                    if not tree.left:
                        break
                right.left = tree  # link 'tree.right' to 'right.right'
                right = right.left
                tree = tree.left
            else:
                if not tree.right:
                    break
                if tree.right.cmp(key) > 0:
                    # rotate left to eliminate 'tree.right'+'tree.right.right' zag-zag
                    tree = self._rotate_left_(tree)
                    if not tree.right:
                        break
                left.right = tree  # link 'tree.left' to 'left.left'
                left = left.right
                tree = tree.right
            cmp = tree.cmp(key)
        # re-assemble 'tree'
        left.right = tree.left
        right.left = tree.right
        tree.left = root.right
        tree.right = root.left
        assert not tree.left or tree.left.cmp(key) > 0
        assert not tree.right or tree.right.cmp(key) < 0
        return tree

    def _splay_max_(self, tree):
        root = self.__class__.Node(None, None)
        left = root
        while tree.right:
            if tree.right.right:  # zag-zag
                tree = self._rotate_left_(tree)
            tree = self._rotate_left_(tree)
            if not tree.right:
                break
            left.right = tree
            left = left.right
            tree = tree.right
        left.right = tree.left
        tree.left = root.right
        return tree

    def _splay_min_(self, tree):
        root = self.__class__.Node(None, None)
        right = root
        while tree.left:
            if tree.left.left:  # zig-zig
                tree = self._rotate_right_(tree)
            tree = self._rotate_right_(tree)
            if not tree.left:
                break
            right.left = tree
            right = right.left
            tree = tree.left
        right.left = tree.right
        tree.right = root.left
        return tree


class SplayTreeBottomUp(SplayTree):
    def _splay_(self, tree, key):
        cmp = tree.cmp(key)
        if cmp < 0 and tree.left:
            cmp = tree.left.cmp(key)
            if cmp < 0:  # zig-zig
                if tree.left.left:
                    tree.left.left = self._splay_(tree.left.left, key)
                    tree = self._rotate_right_(tree)
                tree = self._rotate_right_(tree)
            # elif cmp > 0:  # zig-zag
            #    if tree.left.right:
            #        tree.left.right = self._splay_(tree.left.right, key)
            #        tree.left = self._rotate_left_(tree.left)
            #    tree = self._rotate_right_(tree)
            else:
                tree.left = self._splay_(tree.left, key)
                tree = self._rotate_right_(tree)
        elif cmp > 0 and tree.right:
            cmp = tree.right.cmp(key)
            if cmp > 0:  # zag-zag
                if tree.right.right:
                    tree.right.right = self._splay_(tree.right.right, key)
                    tree = self._rotate_left_(tree)
                tree = self._rotate_left_(tree)
            # elif cmp < 0:  # zag-zig
            #    if tree.right.left:
            #        tree.right.left = self._splay_(tree.right.left, key)
            #        tree.right = self._rotate_right_(tree.right)
            #    tree = self._rotate_left_(tree)
            else:
                tree.right = self._splay_(tree.right, key)
                tree = self._rotate_left_(tree)
        assert not tree.left or tree.left.cmp(key) > 0
        assert not tree.right or tree.right.cmp(key) < 0
        return tree

    def _splay_max_(self, tree):
        if tree.right:
            if tree.right.right:  # zag-zag
                tree.right.right = self._splay_max_(tree.right.right)
                tree = self._rotate_left_(tree)
            tree = self._rotate_left_(tree)
        return tree

    def _splay_min_(self, tree):
        if tree.left:
            if tree.left.left:  # zig-zig
                tree.left.left = self._splay_min_(tree.left.left)
                tree = self._rotate_right_(tree)
            tree = self._rotate_right_(tree)
        return tree
