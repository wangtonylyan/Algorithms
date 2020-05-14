# 数组中的双指针、移动窗口等思想，类似于链表


if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))


from algorithms.utility import *
from data_structure.tree.bst import BinarySearchTree


###############################################################################


def fliptree(tree):
    def flip(t):
        t.left, t.right = t.right, t.left

    BinarySearchTree.breadthfirst(tree, flip)


# 注意二叉树是否平衡取决于每个子树是否平衡，而不能仅考虑树根处的情况
def isbalanced(tree):
    stk = [(tree, None, None)]
    while len(stk) > 0:
        tree, left, right = stk[-1]
        if left is None:
            if tree.left is None:
                stk[-1] = tree, 0, right
            else:
                stk.append((tree.left, None, None))
        elif right is None:
            if tree.right is None:
                stk[-1] = tree, left, 0
            else:
                stk.append((tree.right, None, None))
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


if __name__ == '__main__':
    #t = BinarySearchTree()
    #l = [5, 6, 4, 1, 2, 3]
    class Father:
        def __init__(self, v1, v2):
            print(v1, v2)

    class Son(Father):
        def __init__(self, v1, v2):
            super().__init__(v1, v2)

    Son(1, 2)
