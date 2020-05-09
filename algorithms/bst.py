if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))


from algorithms.utility import *
from data_structure.tree.bst import BinarySearchTree


class BSTProblem(Problem):
    def check(self, tree):
        assert isinstance(tree, BinarySearchTree) and tree.root
        return tree.root


class BSTCheck(BSTProblem):
    def algo(self, tree):
        def depth(_, d): return d

        def key(t, _): return t.key

        def isleaf(t, d):
            if not t.left and not t.right:
                return t, d

        leaf = list(filter(lambda x: x is not None,
                           BinarySearchTree.widthfirst(tree, isleaf)))

        return tuple([
            ## width-first
            BinarySearchTree._len_(tree),  # 节点总数
            len(leaf),  # 叶子节点个数
            BinarySearchTree._height_(tree),  # 最大高度
            leaf[0][1],  # 最小高度，亦即第一个叶子节点的高度
            BinarySearchTree.widthfirst(tree, depth),  # 各节点高度
            # 翻转

            ## depth-first
            BinarySearchTree.depthfirst(tree, 'preorder', key),  # 前序遍历
            BinarySearchTree.depthfirst(tree, 'inorder', key),  # 中序遍历
            BinarySearchTree.depthfirst(tree, 'postorder', key),  # 后序遍历
        ])


## 判断二叉树是否是完全的
class Problem1(BSTProblem):
    def algo1(self, tree):
        que = [tree]
        leaf = False  # 需判断何时访问到了叶子节点

        while len(que) > 0:
            tree = que.pop(0)

            # 结合leaf状态，分别讨论左右子树的四种情况
            if tree.left and tree.right:
                if leaf:
                    return False
                que.append(tree.left)
                que.append(tree.right)
            if tree.left and not tree.right:
                if leaf:
                    return False
                leaf = True  # 后续节点将是叶子节点
                que.append(tree.left)
            if not tree.left and tree.right:
                return False
            if not tree.left and not tree.right:
                leaf = True  # 当前节点已是叶子节点

        return True

    def algo2(self, tree):
        # 通过广度优先遍历获取每个节点的高度
        lst = BinarySearchTree.widthfirst(tree, lambda _, d: d)

        i, j = 0, 0
        while i < len(lst):
            while j < len(lst) and lst[i] == lst[j]:
                j += 1
            if lst[i] != lst[-1] and j - i != 2 ** lst[i]:
                return False
            i = j

        return True


## 寻找最近公共祖先
class Problem2(BSTProblem):
    def check(self, tree, v1, v2):
        return super.check(tree), v1, v2

    def algo(self, tree, v1, v2):
        tree = tree.root
        while tree:
            if tree.value > v1 and tree.value > v2:
                tree = tree.left
                continue
            if tree.value < v1 and tree.value < v2:
                tree = tree.right
                continue
            # tree.value > value1 and tree.value < value2
            # tree.value == value1 or tree.value == value2
            return tree  # 找到目标节点


if __name__ == '__main__':
    t1 = [1, 2, 3, 4, 5, 6]
    t2 = [6, 5, 4, 3, 2, 1]
    t3 = [5, 6, 4, 1, 2, 3]
    t4 = [5, 6, 4, 1, 3, 2]

    Problem.testsuit([
        [BSTCheck, (
            len(t1), 1,
            6, 6, [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [6, 5, 4, 3, 2, 1],
        ), BinarySearchTree().insert(t1, t1)],
        [BSTCheck, (
            len(t2), 1,
            6, 6, [1, 2, 3, 4, 5, 6],
            [6, 5, 4, 3, 2, 1],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
        ), BinarySearchTree().insert(t2, t2)],
        [BSTCheck, (
            len(t3), 2,
            5, 2, [1, 2, 2, 3, 4, 5],
            [5, 4, 1, 2, 3, 6],
            [1, 2, 3, 4, 5, 6],
            [3, 2, 1, 4, 6, 5],
        ), BinarySearchTree().insert(t3, t3)],
        [BSTCheck, (
            len(t4), 2,
            5, 2, [1, 2, 2, 3, 4, 5],
            [5, 4, 1, 3, 2, 6],
            [1, 2, 3, 4, 5, 6],
            [2, 3, 1, 4, 6, 5],
        ), BinarySearchTree().insert(t4, t4)],

        [Problem1, False, BinarySearchTree().insert(t1, t1)],
        [Problem1, False, BinarySearchTree().insert(t2, t2)],
        [Problem1, False, BinarySearchTree().insert(t3, t3)],
        [Problem1, False, BinarySearchTree().insert(t4, t4)],
    ])
