if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))


from algorithms.utility import *
from data_structure.tree.bst import BinarySearchTree


class BTProblem(Problem):
    def check(self, tree):
        assert isinstance(tree, BinarySearchTree) and tree.root
        return tree.root


#########################################################################################
class BTCheck(BTProblem):
    def algo(self, tree):
        def depth(_, d): return d

        def key(t, _): return t.key

        def isleaf(t, d):
            if not t.left and not t.right:
                return t, d

        leaf = list(filter(lambda x: x is not None,
                           BinarySearchTree.breadthfirst(tree, isleaf)))

        return tuple([
            ## breadth-first
            BinarySearchTree._len_(tree),  # 节点总数
            len(leaf),  # 叶子节点个数
            BinarySearchTree._height_(tree),  # 最大高度
            leaf[0][1],  # 最小高度，亦即第一个叶子节点的高度
            BinarySearchTree.breadthfirst(tree, depth),  # 各节点高度
            # 翻转

            ## depth-first
            BinarySearchTree.depthfirst(tree, 'preorder', key),  # 前序遍历
            BinarySearchTree.depthfirst(tree, 'inorder', key),  # 中序遍历
            BinarySearchTree.depthfirst(tree, 'postorder', key),  # 后序遍历
        ])


## LeetCode 958
## 判断二叉树是否完全
class IsComplete(BTProblem):
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
            elif tree.left and not tree.right:
                if leaf:
                    return False
                leaf = True  # 后续节点将是叶子节点
                que.append(tree.left)
            elif not tree.left and tree.right:
                return False
            else:
                assert not tree.left and not tree.right
                leaf = True  # 当前节点已是叶子节点

        return True

    def algo2(self, tree):
        # 通过广度优先遍历获取每个节点的高度
        lst = BinarySearchTree.breadthfirst(tree, lambda _, d: d)

        i, j = 0, 0
        while i < len(lst):
            while j < len(lst) and lst[i] == lst[j]:
                j += 1
            if lst[i] != lst[-1] and j - i != 2 ** lst[i]:
                return False
            i = j

        return True


## LeetCode 110
## 判断二叉树是否平衡
class IsBalanced(BTProblem):
    def algo1(self, tree):
        stk = [(tree, None, None)]

        while len(stk) > 0:
            tree, left, right = stk[-1]

            if left is None:
                if tree.left:
                    stk.append((tree.left, None, None))
                else:
                    stk[-1] = tree, 0, right
            elif right is None:
                if tree.right:
                    stk.append((tree.right, None, None))
                else:
                    stk[-1] = tree, left, 0
            else:
                if abs(left - right) > 1:
                    return False

                stk.pop()

                if len(stk) > 0:
                    if stk[-1][1] is None:
                        stk[-1] = stk[-1][0], max(left, right) + 1, stk[-1][2]
                    else:
                        assert stk[-1][2] is None
                        stk[-1] = stk[-1][0], stk[-1][1], max(left, right) + 1

        return True


## LeetCode 101
## 判断二叉树是否对称
class IsSymmetric(BTProblem):
    def algo1(self, tree):
        que = [tree]

        while len(que) > 0:
            nodes = []
            for tree in que:
                nodes.append(tree.left)
                nodes.append(tree.right)

            keys = list(map(lambda t: t.key if t else None, nodes))
            if keys != keys[::-1]:  # 回文
                return False

            que = list(filter(lambda t: t is not None, nodes))

        return True

    def algo2(self, tree):
        def recur(left, right):
            if not left and not right:
                return True
            if (left and not right) or (not left and right) or (left.key != right.key):
                return False
            return recur(left.left, right.right) and recur(left.right, right.left)

        return recur(tree.left, tree.right)


## 寻找最近公共祖先节点
## 假设二叉树中每个节点的键都是唯一的
class LeetCode236(BTProblem):
    def check(self, tree, k1, k2):
        assert k1 != k2
        return super().check(tree), k1, k2

    def algo1(self, tree, k1, k2):
        stk = [(tree, 0)]
        visit, path = None, None

        while len(stk) > 0:
            tree, state = stk[-1]

            if state == 0:  # 第二个被访问到的目标节点，只会被访问这一次
                # 第一次遇到某个目标节点时，要根据另一个目标节点被访问的次数
                # 来决定是否已找到了最近公共祖先节点
                if tree.key == k1 or tree.key == k2:
                    if visit == 1 or visit == 2:
                        return k1 if tree.key == k2 else k2
                    if visit == 3:
                        i = 0
                        while stk[i][0].key == path[i][0].key:
                            i += 1
                        return stk[i - 1][0].key
                    assert visit is None
                    visit = 1

                stk[-1] = tree, state + 1
                if tree.left:
                    stk.append((tree.left, 0))
            elif state == 1:
                if tree.key == k1 or tree.key == k2:
                    visit += 1

                stk[-1] = tree, state + 1
                if tree.right:
                    stk.append((tree.right, 0))
            else:
                if tree.key == k1 or tree.key == k2:
                    visit += 1
                    path = stk[:]  # 最多只有第一个被访问到的目标节点会出栈

                assert state == 2
                stk.pop()


#########################################################################################
## 寻找最近公共祖先节点
class Problem1(BTProblem):
    def check(self, tree, k1, k2):
        assert k1 != k2
        return super().check(tree), k1, k2

    def algo1(self, tree, k1, k2):
        tree = tree.root
        while tree:
            if tree.key > k1 and tree.key > k2:
                tree = tree.left
                continue
            if tree.key < k1 and tree.key < k2:
                tree = tree.right
                continue
            # tree.key > k1 and tree.key < k2
            # tree.key == k1 or tree.key == k2
            return tree  # 找到目标节点


if __name__ == '__main__':
    # 暂以二叉搜索树来构造二叉树
    t1 = [1, 2, 3, 4, 5, 6]
    t2 = [6, 5, 4, 3, 2, 1]
    t3 = [5, 6, 4, 1, 2, 3]
    t4 = [5, 6, 4, 1, 3, 2]

    # Binary Tree
    Problem.testsuit([
        [BTCheck, (
            len(t1), 1,
            6, 6, [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
            [6, 5, 4, 3, 2, 1],
        ), BinarySearchTree().insert(t1, t1)],
        [BTCheck, (
            len(t2), 1,
            6, 6, [1, 2, 3, 4, 5, 6],
            [6, 5, 4, 3, 2, 1],
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 5, 6],
        ), BinarySearchTree().insert(t2, t2)],
        [BTCheck, (
            len(t3), 2,
            5, 2, [1, 2, 2, 3, 4, 5],
            [5, 4, 1, 2, 3, 6],
            [1, 2, 3, 4, 5, 6],
            [3, 2, 1, 4, 6, 5],
        ), BinarySearchTree().insert(t3, t3)],
        [BTCheck, (
            len(t4), 2,
            5, 2, [1, 2, 2, 3, 4, 5],
            [5, 4, 1, 3, 2, 6],
            [1, 2, 3, 4, 5, 6],
            [2, 3, 1, 4, 6, 5],
        ), BinarySearchTree().insert(t4, t4)],

        [IsComplete, False, BinarySearchTree().insert(t1, t1)],
        [IsComplete, False, BinarySearchTree().insert(t2, t2)],
        [IsComplete, False, BinarySearchTree().insert(t3, t3)],
        [IsComplete, False, BinarySearchTree().insert(t4, t4)],

        [IsBalanced, False, BinarySearchTree().insert(t1, t1)],
        [IsBalanced, False, BinarySearchTree().insert(t2, t2)],
        [IsBalanced, False, BinarySearchTree().insert(t3, t3)],
        [IsBalanced, False, BinarySearchTree().insert(t4, t4)],

        [IsSymmetric, False, BinarySearchTree().insert(t1, t1)],
        [IsSymmetric, False, BinarySearchTree().insert(t2, t2)],
        [IsSymmetric, False, BinarySearchTree().insert(t3, t3)],
        [IsSymmetric, False, BinarySearchTree().insert(t4, t4)],
    ])

    # Binary Search Tree
    Problem.testsuit([

    ])
