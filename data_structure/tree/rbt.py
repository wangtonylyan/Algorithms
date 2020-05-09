## data structure: red-black tree, left-leaning red-black (LLRB) tree
# 红黑树属于2-3(-4)树的一种变种
# 左倾红黑树增加了"左倾"这一约束，使得实现上需要讨论的情况减少了

if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))


from data_structure.tree.bst import SelfBalancingBST


class RedBlackTree(SelfBalancingBST):
    class Node(SelfBalancingBST.Node):
        __slots__ = ['color']

        def __init__(self, key, value):
            super().__init__(key, value)
            # True if red else (black) False
            self.color = True  # default color of a new leaf node

        def __str__(self):
            return super().__str__() + ', ' + f'color={str(self.color)}'

    # top-down中，天然地不存在有4结点
    # insertion中，新增结点会导致，2或3结点变为3或4结点
    # bottom-up中，消除4结点
    def insert(self, key, value):
        super().insert(key, value)
        self.root.color = False

    # [invariant] 'tree' is a red-black tree
    @classmethod
    def rotateleft(cls, tree):
        tree = cls._rotateleft_(tree)
        # concerning the augment
        tree.color, tree.left.color = tree.left.color, tree.color
        return tree

    @classmethod
    def rotateright(cls, tree):
        tree = cls._rotateright_(tree)
        tree.color, tree.right.color = tree.right.color, tree.color
        return tree

    # [invariant] 'tree' is a relaxed red-black tree
    # [what] turn 'tree' from a 2-node into a 4-node, or reversely
    # [side-effect] increase or decrease 'tree' height by 1
    @classmethod
    def flipcolor(cls, tree):
        tree.left.color = not tree.left.color
        tree.right.color = not tree.right.color
        tree.color = not tree.color
        return tree

    # [premise] at most one of 'tree', 'tree.left' and 'tree.right' is a 4-node
    # [what] eliminate 4-node, resulting in the 'tree' balance
    @classmethod
    def balance(cls, tree):
        if tree.left and tree.left.color:
            if tree.left.right and tree.left.right.color:
                tree.left = cls.rotateleft(tree.left)
            if tree.left.left and tree.left.left.color:
                tree = cls.rotateright(tree)
        elif tree.right and tree.right.color:
            if tree.right.left and tree.right.left.color:
                tree.right = cls.rotateright(tree.right)
            if tree.right.right and tree.right.right.color:
                tree = cls.rotateleft(tree)
        if tree.left and tree.left.color and tree.right and tree.right.color:
            tree = cls.flipcolor(tree)
        return tree

    ###########################################################################

    def _apply_del_func(self, func, *args, **kwargs):
        if self.root:
            # make sure that 'root' isn't a 2-node before recursion
            if not (self.root.left and self.root.left.color) and not (self.root.right and self.root.right.color):
                self.root.color = True
            self.root = func(self.root, *args, **kwargs)
            if self.root and self.root.color:
                self.root.color = False

    # top-down中，下沉3或4结点
    # deletion中，删除结点会导致，3或4结点变为2结点
    # bottom-up中，消除4结点
    def delete(self, key):
        assert key is not None
        self._apply_del_func(self._delete, key)

    def delmax(self):
        self._apply_del_func(self._delmax)

    def delmin(self):
        self._apply_del_func(self._delmin)

    # 1) top-down: make 'tree.left' or 'tree.right' a 3-node
    # 2) recursion: delete or fail
    # 3) buttom-up: rebalance
    def _delete(self, tree, key):
        def find(tree):
            if not tree.left:
                if tree.right:
                    tree.right.color = tree.color
                return tree.right  # delete without necessity of rebalancing
            if not tree.right:
                if tree.left:
                    tree.left.color = tree.color
                return tree.left
            # 用左子树中的最大节点或右子树中的最小节点来替换要被删除的目标节点：_delmax(tree.left) vs. _delmin(tree.right)
            # 两种策略的实现方式是完全对称的，但对于LLRB树而言，由于其左倾的特性，选择后者效率会略高
            tree = self._make_right_red(tree)
            if key != tree.key:  # if 'tree' node is no longer the one before _make_right_red()
                tree.right = self._delete(tree.right, key)  # continue traversing
            else:
                m = self._getmin(tree.right)
                tree.key = m.key
                tree.value = m.value
                tree.right = self._delmin(tree.right)  # delete
            return tree

        def down(tree):
            cmp = tree.cmp(key)
            if cmp < 0:
                tree = self._make_left_red(tree)
            elif cmp > 0:
                tree = self._make_right_red(tree)
            return tree

        return self._recur_(tree, which=lambda tree: tree.cmp(key), find=find, down=down)

    def _delmax(self, tree):
        return self._recur_(tree,
                            which=lambda tree: 1 if tree.right else 0,
                            find=lambda tree: tree.left.set(
                                color=tree.color) if tree.left else tree.left,
                            down=self._make_right_red)

    def _delmin(self, tree):
        return self._recur_(tree,
                            which=lambda tree: -1 if tree.left else 0,
                            find=lambda tree: tree.right.set(
                                color=tree.color) if tree.right else tree.right,
                            down=self._make_left_red)

    # @premise: 'tree' is a 3-node
    # @invariant: 'tree.right' is a balanced red-black tree, which will be neither traversed nor rebalanced after return
    # @what: turn 'tree.left' into a 3-node
    # @how: move red from 'tree' or 'tree.right' node to 'tree.left' node
    # @when: before traversal of the 'tree.left' subtree
    def _make_left_red(self, tree):
        if not tree or not tree.left:
            return tree
        assert tree.color or tree.left.color or (tree.right and tree.right.color)
        if tree.left.color or \
                (tree.left.left and tree.left.left.color) or \
                (tree.left.right and tree.left.right.color):
            return tree
        assert tree.right  # black-height invariant
        if tree.color:
            tree = self._flip_color(tree)  # move red from 'tree' node to its children
            if tree.right.left and tree.right.left.color:  # 'tree.right' subtree is no longer balanced
                tree.right = self._rotate_right(tree.right)
            if tree.right.right and tree.right.right.color:
                tree = self._rotate_left(tree)
                tree = self._flip_color(tree)
        else:
            assert tree.right.color
            # move red from 'tree.right' node to 'tree.left' node
            tree = self._rotate_left(tree)
        assert tree.left.color or \
            (tree.left.left and tree.left.left.color) or \
            (tree.left.right and tree.left.right.color)
        return tree

    def _make_right_red(self, tree):
        if not tree or not tree.right:
            return tree
        assert tree.color or tree.right.color or (tree.left and tree.left.color)
        if tree.right.color or \
                (tree.right.left and tree.right.left.color) or \
                (tree.right.right and tree.right.right.color):
            return tree
        assert tree.left
        if tree.color:
            tree = self._flip_color(tree)
            if tree.left.right and tree.left.right.color:
                tree.left = self._rotate_left(tree.left)
            if tree.left.left and tree.left.left.color:
                tree = self._rotate_right(tree)
                tree = self._flip_color(tree)
        else:
            assert tree.left.color
            tree = self._rotate_right(tree)
        assert tree.right.color or \
            (tree.right.left and tree.right.left.color) or \
            (tree.right.right and tree.right.right.color)
        return tree


# LLRB树的实现涉及有以下几种策略上的选择：
# 选择不同的策略意味着树的表现特征会有所区别，从而导致实现上的些许差异
# 1) 2-3 tree vs. 2-3-4 tree
# 前者要求在破坏树的结构后，在bottom-up阶段重新平衡树并消除4-node
# 即允许4-node存在的relaxed red-black tree
# 后者要求在破坏树的结构后，在bottom-up阶段重新平衡树即可
# 目前采用的实现方式是基于2-3树，分类讨论的情形可以略微简单点
# 2) left-leaning vs. right-leaning
# 两种实现方式完全对称，没有实质性的区别
# 只是由于倾向了一侧，所以对左右子树的处理可能会略有不同，但也可以规避
# 例如在当前delete()的实现中，每次递归都总是先将当前子树由左/右倾转变成右/左倾
# 即在top-down阶段破坏leaning invariant，于是随后的操作就完全对称了
class LeftLeaningRedBlackTree(RedBlackTree):
    # this implementation only of use for relaxed LLRB tree is just for illustration here
    # 1) top-down: split 4-node
    # 2) recursion
    # 3) bottom-up: accept 4-node
    def _insert_relaxed(self, tree, key, value):
        def split4node(tree):
            if tree.left and tree.left.color and tree.right and tree.right.color:
                tree = self._flip_color(tree)
            return tree

        def balance(tree):
            if tree.right and tree.right.color:
                tree = self._rotateLeft(tree)
            if tree.left and tree.left.color and tree.left.left and tree.left.left.color:
                tree = self._rotateRight(tree)
            return tree

        return self._recur_(tree,
                            which=lambda tree: tree.cmp(key),
                            find=lambda tree: tree.set(value=value),
                            miss=lambda: self.__class__.Node(key, value),
                            down=split4node,
                            up=balance)

    # 相比于传统的红黑树，三个基本操作所产生的额外副作用
    # 1) rotate left: 将tree.right.left这棵左子树变成了右子树
    # 2) rotate right: 可能将tree从一颗左子树变成了右子树
    # 3) flip color: 无
    # 注意这三个基本操作是同时适用于2-3和2-3-4 tree、left-和right-leaning策略的
    # 因为其没有维护这些策略的各自特征，具体实现哪种策略取决于这些操作之间的组合

    def _balance(self, tree):
        if not tree:
            return tree
        # @case: a; b+c; a+b+c(==c)
        if tree.right and tree.right.color:  # a
            tree = self._rotate_left(tree)
        if tree.left and tree.left.color and tree.left.left and tree.left.left.color:  # b
            tree = self._rotate_right(tree)
        if tree.left and tree.left.color and tree.right and tree.right.color:  # c
            tree = self._flip_color(tree)
        return tree

    # @what: turn 'tree.left' into a 3- or 4- node, regardless of its leaning characteristic
    def _make_left_red(self, tree):
        if not tree or not tree.left:
            return tree
        assert tree.color or tree.left.color or (tree.right and tree.right.color)
        if tree.left.color or \
                (tree.left.left and tree.left.left.color) or \
                (tree.left.right and tree.left.right.color):
            return tree
        assert tree.right  # black-height invariant
        if tree.color:
            tree = self._flip_color(tree)
            assert not tree.right.right or not tree.right.right.color  # left-leaning invariant
            if tree.right.left and tree.right.left.color:
                # keep left-leaning invariant of 'tree.right' subtree
                tree.right = self._rotate_right(tree.right)
                tree = self._rotate_left(tree)
                tree = self._flip_color(tree)
        else:
            assert tree.right.color
            tree = self._rotate_left(tree)
        assert tree.left.color or \
            (tree.left.left and tree.left.left.color) or \
            (tree.left.right and tree.left.right.color)
        return tree

    def _make_right_red(self, tree):
        if not tree or not tree.right:
            return tree
        assert tree.color or tree.right.color or (tree.left and tree.left.color)
        if tree.right.color or \
                (tree.right.left and tree.right.left.color) or \
                (tree.right.right and tree.right.right.color):
            return tree
        assert tree.left
        if tree.color:
            tree = self._flip_color(tree)
            assert not tree.left.right or not tree.left.right.color
            if tree.left and tree.left.left and tree.left.left.color:
                tree = self._rotate_right(tree)
                tree = self._flip_color(tree)
        else:
            assert tree.left.color
            tree = self._rotate_right(tree)
        assert tree.right.color or \
            (tree.right.left and tree.right.left.color) or \
            (tree.right.right and tree.right.right.color)
        return tree
