# -*- coding: utf-8 -*-
# problem: selection (find the k-th smallest element in a collection)
# solution: partitioning-based selection, bubble, divide and conquer

# solution1: partitioning-based
# @param k: the k-th smallest element [0, len(lst)-1]
def select(lst, k):
    # 同快排算法中的partition()
    # 返回值flag就是第flag小的数位于数组中的索引值
    def partition(lst):
        flag = 0
        for i in range(1, len(lst)):
            if lst[i] < lst[0]:
                lst[i], lst[flag + 1] = lst[flag + 1], lst[i]
                flag += 1
        lst[0], lst[flag] = lst[flag], lst[0]
        return flag

    while k >= 0:
        flag = partition(lst)
        if flag > k:
            lst = lst[:flag]
        elif flag < k:
            k -= flag + 1
            lst = lst[flag + 1:]
        else:
            return lst[flag]


# solution2: bubble-based
def select2(lst, k):
    for i in range(k + 1):
        for j in range(len(lst) - 1, i, -1):
            if lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
    return lst[k]

# 1,3,3,4,5,6,7,8
lst = [5, 3, 6, 4, 3, 7, 8, 1]
if __name__ == "__main__":
    k = 1
    print select(lst[:], k)
    print select2(lst[:], k)
