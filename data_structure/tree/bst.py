# -*- coding: utf-8 -*-
# data structure: binary search tree

class BST(object):
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def insert(self, key, value):
        def _recur(bst, key, value):
            if bst == None:
                return self.__class__.Node(key, value)
            if key < bst.key:
                bst.left = _recur(bst.left, key, value)
            elif key > bst.key:
                bst.right = _recur(bst.right, key, value)
            else:
                bst.value = value
            return bst

        self.root = _recur(self.root, key, value)

    def deleteMax(self):
        self.root = self._deleteMax(self.root)

    @staticmethod
    def _deleteMax(bst):
        if bst:
            if bst.right:
                it = bst
                while it.right.right:
                    it = it.right
                it.right = it.right.left
            else:
                bst = bst.left
        return bst

    def deleteMin(self):
        self.root = self._deleteMin(self.root)

    @staticmethod
    def _deleteMin(bst):
        if bst:
            if bst.left:
                it = bst
                while it.left.left:
                    it = it.left
                it.left = it.left.right
            else:
                bst = bst.right
        return bst

    def delete(self, key):
        def _recur(bst, key):
            if bst == None:
                return None
            if key < bst.key:
                bst.left = _recur(bst.left, key)
            elif key > bst.key:
                bst.right = _recur(bst.right, key)
            else:  # bst就是需要被删除的节点
                if bst.left == None:
                    bst = bst.right
                elif bst.right == None:
                    bst = bst.left
                else:  # 将bst节点替换为其左子树中的最大节点或右子树中的最小节点
                    if bst.left.right == None:
                        bst.left.right = bst.right
                        bst = bst.left
                    elif bst.right.left == None:
                        bst.right.left = bst.left
                        bst = bst.right
                    else:
                        it = bst.left
                        while it.right.right:
                            it = it.right
                        bst.key = it.right.key
                        bst.value = it.right.value
                        it.right = it.right.left
            return bst

        self.root = _recur(self.root, key)

    def search(self, key):
        bst = self._search(self.root, key)
        return bst.value if bst else None

    @staticmethod
    def _search(bst, key):
        while bst:
            if key < bst.key:
                bst = bst.left
            elif key > bst.key:
                bst = bst.right
            else:
                break
        return bst

    def getMax(self):
        return self._getMax(self.root)

    @staticmethod
    def _getMax(bst):
        while bst and bst.right:
            bst = bst.right
        return bst

    def getMin(self):
        return self._getMin(self.root)

    @staticmethod
    def _getMin(bst):
        while bst and bst.left:
            bst = bst.left
        return bst

    def size(self):
        return self._size(self.root)

    @staticmethod
    def _size(bst):
        if bst == None:
            return 0
        return BST._size(bst.left) + BST._size(bst.right) + 1

    def clean(self):
        self.root = None

    def check(self):
        def _recur(bst):
            if bst == None:
                return
            _recur(bst.left)
            _recur(bst.right)
            # check symmetric order property
            if bst.left:
                assert (bst.left.value < bst.value)
            if bst.right:
                assert (bst.right.value > bst.value)

        _recur(self.root)


# balanced binary search tree
class BBST(BST):
    def __index__(self):
        super(BBST, self).__init__()

    # the following are two restructuring primitives for almost all kinds of balanced BSTs
    # which always hold the symmetric order property,
    # and can be used to balance an unbalanced BST in composition
    # rotate left与rotate right这两个操作是完全对称的，且互为可逆
    # 例如，对同一个节点先后各执行一次这两个操作，以该节点为根的子树结构不变
    def _rotateLeft(self, bbst):
        if bbst and bbst.right:
            ret = bbst.right
            bbst.right = ret.left
            ret.left = bbst
            bbst = ret
        return bbst

    def _rotateRight(self, bbst):
        if bbst and bbst.left:
            ret = bbst.left
            bbst.left = ret.right
            ret.right = bbst
            bbst = ret
        return bbst

    def _balance(self, bbst):
        pass


import time, random


class BSTTest(object):
    def __init__(self, clsobj, num, check=False, time=True):
        assert (issubclass(clsobj, BST))
        self.tcls = clsobj
        self.tree = None
        self.dic = {}
        assert (0 < num < 100000)
        for i in range(num):
            r = random.randint(0, 100000)
            self.dic[r] = r + 1
        print "dic's size: ", len(self.dic)
        self.check = check
        self.time = time
        self.start_t = 0
        self.end_t = 0

    def new(self):
        self.tree = self.tcls()
        c = 0
        if self.time:
            self.start_t = time.time()
        for i, j in self.dic.viewitems():
            self.tree.insert(i, j)
            if self.check:
                self.tree.check()
            assert (self.tree.search(i) == j)
            c += 1
            assert (self.tree.size() == c)
        if self.time:
            self.end_t = time.time()
            print 'new:\t\t', self.end_t - self.start_t
        assert (self.tree.size() == len(self.dic))

    def deleteMaxMin(self):
        def test(get, delete):
            c = s = self.tree.size()
            if self.time:
                self.start_t = time.time()
            for i in range(s):
                m = getattr(self.tree, get)()
                getattr(self.tree, delete)()
                if self.check:
                    self.tree.check()
                assert (self.tree.search(m.key) == None)
                c -= 1
                assert (self.tree.size() == c)
            if self.time:
                self.end_t = time.time()
                print delete + ':\t', self.end_t - self.start_t
            assert (self.tree.size() == 0)

        self.new()
        test('getMin', 'deleteMin')
        self.new()
        test('getMax', 'deleteMax')

    def delete(self):
        self.new()
        c = self.tree.size()
        if self.time:
            self.start_t = time.time()
        for i in self.dic:
            assert (self.tree.search(i))
            self.tree.delete(i)
            if self.check:
                self.tree.check()
            assert (self.tree.search(i) == None)
            c -= 1
            assert (self.tree.size() == c)
        if self.time:
            self.end_t = time.time()
            print 'delete:\t\t', self.end_t - self.start_t
        assert (self.tree.size() == 0)


if __name__ == '__main__':
    test = BSTTest(BST, 800, True)
    test.deleteMaxMin()
    test.delete()
    print 'done'
