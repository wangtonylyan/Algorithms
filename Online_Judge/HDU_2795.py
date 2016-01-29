# -*- coding: utf-8 -*-
# http://acm.hdu.edu.cn/showproblem.php?pid=2795

input = [3, 5, 5,  # height, width, number
         2, 4, 3, 3, 3]  # announcements' height
output = [1, 2, 1, 3, 0]
tree = [None for i in range(100)]


class Node():
    def __init__(self, low, high, value):
        self.low = low
        self.high = high
        self.value = value


def build(root, low, high, width):
    tree[root] = Node(low, high, width)
    if low != high:
        mid = (low + high) >> 1
        build(root << 1, low, mid, width)
        build(root << 1 | 1, mid + 1, high, width)


def query(root, width):
    if root > len(tree) or tree[root] == None:
        return 0
    if tree[root].value < width:
        return 0  # no more space
    elif tree[root].low == tree[root].high:
        tree[root].value -= width
        return tree[root].low
    elif tree[root << 1].value >= width:
        ret = query(root << 1, width)
        # 查询过程中同步更新每个节点的max信息，该信息将指导下次查询操作
        tree[root].value = max(tree[root << 1].value, tree[root << 1 | 1].value)
        return ret
    else:
        assert (tree[root << 1 | 1].value >= width)
        ret = query(root << 1 | 1, width)
        tree[root].value = max(tree[root << 1].value, tree[root << 1 | 1].value)
        return ret


if __name__ == '__main__':
    # 以总高度为区间构建线段树
    # 以总宽度为每个高度上剩余宽度的初始值
    build(1, 1, input[0], input[1])
    result = []
    for i in range(3, len(input)):
        result.append(query(1, input[i]))
    assert (result == output)
