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

    BinarySearchTree.widthfirst(tree, flip)


# 注意二叉树是否平衡取决于每个子树是否平衡，而不能仅考虑树根处的情况
def isbalanced(tree):
    stk = [tree.root]
    ban = [(None, None)]
    while len(stk) > 0:
        t = stk[-1]
        lh, rh = ban[-1]
        if lh is None:
            if t.left:
                stk.append(t.left)
                ban.append((None, None))
            else:
                ban[-1] = (0, rh)
        elif rh is None:
            if t.right:
                stk.append(t.right)
                ban.append((None, None))
            else:
                ban[-1] = (lh, 0)
        else:
            stk.pop()
            ban.pop()
            if lh - rh > 1 or rh - lh > 1:
                return False
            if len(stk) > 0:
                llh, rrh = ban[-1]
                if llh is None:
                    ban[-1] = (lh + rh + 1, rrh)
                elif rrh is None:
                    ban[-1] = (llh, lh + rh + 1)
                else:
                    assert False
    return True


if __name__ == '__main__':
    t = BinarySearchTree()
    l = [5, 6, 4, 1, 2, 3]
