# -*- coding: utf-8 -*-


from algos.data_structure.tree.binary.bst import SelfBalancingBinarySearchTree


class RedBlackTree(SelfBalancingBinarySearchTree):
    class Node(SelfBalancingBinarySearchTree.Node):
        __slots__ = ['color']

        # default color of a new leaf node is red
        def __init__(self, key, value, left=None, right=None, color=True):
            super().__init__(key, value, left, right)
            self.color = color  # True if red else False (black)

    def __init__(self):
        super().__init__()

    def insert(self, key, value):
        assert key is not None
        self.root = self._insert(self.root, key, value)
        if self.root.color:
            self.root.color = False

    def delete_pattern(self, func, *args):
        if self.root:
            if not (self.root.left and self.root.left.color) and not (self.right and self.right.color):
                self.root.color = True
            self.root = func(self.root, *args)
            if self.root and self.root.color:
                self.root.color = False

    def delete(self, key):
        assert key is not None
        self.delete_pattern(self._delete, key)

    def delmax(self):
        self.delete_pattern(self._delmax)

    def delmin(self):
        self.delete_pattern(self._delmin)

    def _insert(self, tree, key, value):
        return self._recur_(tree,
                            which=lambda tree: tree.cmp(key),
                            find=lambda tree: self.__class__.Node(tree.key, value, tree.left, tree.right, tree.color),
                            miss=lambda: self.__class__.Node(key, value),
                            up=self._balance)

    def _delete(self, tree, key):
        def find(tree):
            if not tree.left:
                if tree.right:
                    tree.right.color = tree.color
                return tree.right
            if not tree.right:
                if tree.left:
                    tree.left.color = tree.color
                return tree.left
            tree = _make_right_red(tree)
            if key != tree.key:  # if 'tree' node is no longer the one before _make_right_red()
                tree.right = self._delete(tree.right, key)  # continue traversing
            else:
                m = self._getmin(tree.right)
                tree.key = m.key
                tree.value = m.value
                tree.right = self._delmin(tree.right)  # deletion
            return tree

        def down(tree):
            cmp = tree.cmp(key)
            if cmp < 0:
                tree = _make_left_red(tree)
            elif cmp > 0:
                tree = _make_right_red(tree)
            return tree

        return self._recur_(tree,
                            which=lambda tree: tree.cmp(key),
                            find=find,
                            down=down,
                            up=self._balance)

    '''

  def delmax
    if @root
      @root.color = true unless (@root.left && @root.left.color) || (@root.right && @root.right.color)
      @root = _delmax(@root, down: method(:_make_right_red), up: method(:_balance))
      @root.color = false if @root && @root.color
    end
  end

  def delmin
    if @root
      @root.color = true unless (@root.left && @root.left.color) || (@root.right && @root.right.color)
      @root = _delmin(@root, down: method(:_make_left_red), up: method(:_balance))
      @root.color = false if @root && @root.color
    end
  end
'''

    # 1) rotate left：no side-effect
    # 2) rotate right：no side-effect
    # 3) flip color：change subtree's height

    # @invariant: 'tree' is a red-black tree
    def _rotate_left(self, tree):
        assert tree and tree.right
        tree = self._rotate_left_(tree)
        # concerning the augment
        tree.color, tree.left.color = tree.left.color, tree.color
        return tree

    def _rotate_right(self, tree):
        assert tree and tree.left
        tree = self._rotate_right_(tree)
        tree.color, tree.right.color = tree.right.color, tree.color
        return tree

    # @invariant: 'tree' is a relaxed red-black tree
    # @what: turn 'tree' from a 2-node into a 4-node, or reversely
    def _flip_color(self, tree):
        assert tree and tree.left and tree.right
        tree.left.color = not tree.left.color
        tree.right.color = not tree.right.color
        tree.color = not tree.color
        return tree

    # @premise: at most one of 'tree', 'tree.left' and 'tree.right' is a 4-node
    # @what: eliminate 4-node, resulting in the balance of 'tree' subtree
    def _balance(self, tree):
        assert (tree)
        if tree.left and tree.left.color:
            if tree.left.right and tree.left.right.color:
                tree.left = self._rotate_left(tree.left)
            if tree.left.left and tree.left.left.color:
                tree = self._rotate_right(tree)
        elif tree.right and tree.right.color:
            if tree.right.left and tree.right.left.color:
                tree.right = self._rotate_right(tree.right)
            if tree.right.right and tree.right.right.color:
                tree = self._rotate_left(tree)
        if tree.left and tree.left.color and tree.right and tree.right.color:
            tree = self._flip_color(tree)
        return tree

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
            tree = _flip_color(tree)
            if tree.right.left and tree.right.left.color:
                tree.right = _rotate_right(tree.right)
            if tree.right.right and tree.right.right.color:
                tree = _rotate_left(tree)
                tree = _flip_color(tree)
        else:
            assert tree.right.color
            tree = _rotate_left(tree)
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
            tree = _flip_color(tree)
            if tree.left.right and tree.left.right.color:
                tree.left = _rotate_left(tree.left)
            if tree.left.left and tree.left.left.color:
                tree = _rotate_right(tree)
                tree = _flip_color(tree)
        else:
            assert tree.left.color
            tree = _rotate_right(tree)
        assert tree.right.color or \
               (tree.right.left and tree.right.left.color) or \
               (tree.right.right and tree.right.right.color)
        return tree
