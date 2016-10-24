# -*- coding: utf-8 -*-
# data structure: AA (Arne Andersson) tree
# AA树可被视为是一种简化版的"右倾"红黑树
# 每个节点中维护的level综合了AVL树和红黑树的特性


from bst import SelfBalancingBinarySearchTree, BinarySearchTreeTest, AugmentedBinarySearchTreeWrapper


class AATree(SelfBalancingBinarySearchTree):
    class Node(SelfBalancingBinarySearchTree.Node):
        __slots__ = ['level']

        def __init__(self, key, value):
            super(AATree.Node, self).__init__(key, value)
            self.level = 1

    def __init__(self):
        super(AATree, self).__init__()

    # AA树与红黑树的区别：
    # 1) 插入和删除过程都没有top-down阶段的提前准备，仅需在bottom-up时重新平衡
    # 2) 由于'右倾'的特性，平衡算法就变得单调了，即skew+split的线性组合
    # 沿右子树的多次(单层上至多两次)skew操作首先将所有的左倾结构都转换成右倾
    # 沿右子树的多次(单层上至多两次)split操作再通过增加树的层次来消除多余的右倾

    # == rotateRight: turning 'aat.left.right' into left
    def _skew(self, aat):
        if aat.left and aat.left.level == aat.level:
            aat = self._rotateRight_(aat)
            assert (aat.level == aat.right.level)
        return aat

    # == rotateLeft + flipColor: increasing 'aat' level
    def _split(self, aat):
        if aat.right and aat.right.right and aat.right.right.level == aat.level:
            assert (aat.level == aat.right.level == aat.right.right.level)
            aat = self._rotateLeft_(aat)
            assert (aat.level == aat.left.level == aat.right.level)
            aat.level += 1
        return aat

    def _balance(self, aat):
        # scenarios after insertion in one subtree:
        #          a             a
        #         / \             \
        # [left] b   c   [right]   b
        #                           \
        #                            c
        # scenarios after deletion in one subtree:
        #        a                 a
        #         \               /
        # [left]   b     [right] b
        #         / \             \
        #        c   d             c
        #         \   \
        #          e   f
        assert (aat)
        # 1) decrease 'aat' level as much as possible
        # actually it only matters during deletion in case that one subtree is lower
        m = min(aat.left.level if aat.left else 0, aat.right.level if aat.right else 0) + 1
        if aat.level > m:
            assert (aat.level == m + 1)
            aat.level = m
            if aat.right and aat.right.level > m:
                # 'aat' and 'aat.right' were viewed as a single pseudo-node
                aat.right.level = m
        # 2) skew+split combo along the right subtree
        aat = self._skew(aat)
        if aat.right:
            aat.right = self._skew(aat.right)
            if aat.right.right:
                aat.right.right = self._skew(aat.right.right)
        aat = self._split(aat)
        if aat.right:
            aat.right = self._split(aat.right)
        return aat

    def insert(self, key, value):
        assert (key is not None and value is not None)
        self.root = self._insert(self.root, key, value)

    def _insert(self, aat, key, value):
        if not aat:
            return self.__class__.Node(key, value)
        if key < aat.key:
            aat.left = self._insert(aat.left, key, value)
            aat = self._balance(aat)
        elif key > aat.key:
            aat.right = self._insert(aat.right, key, value)
            aat = self._balance(aat)
        else:
            aat.value = value
        return aat

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, aat, key):
        if not aat:
            return aat
        if key < aat.key:
            aat.left = self._delete(aat.left, key)
            aat = self._balance(aat)
        elif key > aat.key:
            aat.right = self._delete(aat.right, key)
            aat = self._balance(aat)
        else:
            if aat.right:
                m = self._getMin(aat.right)
                aat.right = self._deleteMin(aat.right)
                assert (self._search(aat.right, m.key) is None)
                aat.key = m.key
                aat.value = m.value
                aat = self._balance(aat)
            elif aat.left:
                aat = aat.left
            else:
                assert (aat.level == 1)
                aat = None
        return aat

    def _deleteMax(self, aat):
        if aat:
            if aat.right:
                aat.right = self._deleteMax(aat.right)
                aat = self._balance(aat)
            else:
                aat = aat.left
        return aat

    def _deleteMin(self, aat):
        if aat:
            if aat.left:
                aat.left = self._deleteMin(aat.left)
                aat = self._balance(aat)
            else:
                aat = aat.right
        return aat

    def _check(self, aat, left, right):
        if aat:
            if aat.left:
                # level of a left child is strictly less than that of its parent
                assert (aat.left.level < aat.level)
            if aat.right:
                # level of a right child is less than or equal to that of its parent
                assert (aat.right.level <= aat.level)
                if aat.right.right:
                    # level of a right grandchild is strictly less than that of its grandparent
                    assert (aat.right.right.level < aat.level)
            if not aat.left and not aat.right:
                # level of a leaf node is one
                assert (aat.level == 1)
            if aat.level > 1:
                # 隐式特征: every node of level greater than one must have two children
                assert (aat.left and aat.right)
        # 无需像红黑树那样统计左右子树的black height，因为level就已经对其约束了
        return super(AATree, self)._check(aat, left, right)


class AugmentedAATree(AugmentedBinarySearchTreeWrapper, AATree):
    def __init__(self):
        super(AugmentedAATree, self).__init__()


if __name__ == '__main__':
    BinarySearchTreeTest(AATree).testcase()
    print 'done'
