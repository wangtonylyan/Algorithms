# -*- coding: utf-8 -*-
# http://acm.hdu.edu.cn/showproblem.php?pid=1754

input = [5, 6,  # number of students and operations
         7, 5, 8, 3, 9,  # students' grades
         2, 4]  # query interval
output = [8]
tree = [0 for i in range(100)]
grades = [0] + input[2:]


class Node():
    def __init__(self, low, high, value):
        self.low = low
        self.high = high
        self.value = value


def build(root, low, high):
    tree[root] = Node(low, high, max(grades[low:high + 1]))
    if low != high:
        mid = (low + high) >> 1
        build(root << 1, low, mid)
        build(root << 1 | 1, mid + 1, high)


def query(root, low, high):
    if root >= len(tree) or tree[root] == None:
        return 0
    if tree[root].low == low and tree[root].high == high:
        return tree[root].value
    else:
        left, right = 0, 0
        root <<= 1
        if low <= tree[root].high:
            # 调用子递归查询的区间范围必须控制在[low,high]之内
            left = query(root, max(low, tree[root].low), min(high, tree[root].high))
        root += 1
        if high >= tree[root].low:
            right = query(root, max(low, tree[root].low), min(high, tree[root].high))
        return max(left, right)


if __name__ == '__main__':
    build(1, 1, input[0])
    low = input[1 + input[0] + 1]
    high = input[1 + input[0] + 1 + 1]
    result = query(1, low, high)
    assert (output == [result])
