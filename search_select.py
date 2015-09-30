# -*- coding: utf-8 -*-
# problem: selection (find the k-th biggest/smallest element in a collection)
# solution: partitioning-based, bubble-based, divide and conquer

# @param k: the k-th biggest/smallest element, in the range of [0, len(lst)-1]

# solution1: partitioning-based selection
def select(lst, k):
    # 返回值flag就是第flag大的数位于数组中的索引值
    def _partition(lst, low, high):
        flag = low
        for i in range(low + 1, high):  # traverse from low+1
            if lst[i] < lst[low]:
                lst[i], lst[flag + 1] = lst[flag + 1], lst[i]
                flag += 1
        lst[low], lst[flag] = lst[flag], lst[low]
        return flag

    def _max(lst, k):
        low = 0
        high = len(lst)
        while k >= 0 and low <= high:
            flag = _partition(lst, low, high)
            # len(lst)-1-flag就是比lst[flag]值大的数的个数
            if len(lst) - 1 - flag > k:
                low = flag + 1
            elif len(lst) - 1 - flag < k:
                k = (k + 1) - (len(lst) - 1 - flag)
                high = flag
            else:
                return lst[flag]
        return None

    def _min(lst, k):
        low = 0
        high = len(lst)
        while k >= 0 and low <= high:
            # flag就是第flag大的
            flag = _partition(lst, low, high)
            if flag > k:
                high = flag
            elif flag < k:
                k -= flag
                low = flag + 1
            else:
                return lst[flag]
        return None

    return (_max(lst[:], k), _min(lst[:], k))


# solution2: bubble-based selection
def select2(lst, k):
    def _max(lst, k):
        for i in range(len(lst) - 1, len(lst) - 1 - k - 1, -1):
            for j in range(0, i):
                if lst[j] > lst[j + 1]:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
        return lst[len(lst) - 1 - k]

    def _min(lst, k):
        for i in range(k + 1):
            for j in range(len(lst) - 1, i, -1):
                if lst[j] < lst[j - 1]:
                    lst[j], lst[j - 1] = lst[j - 1], lst[j]
        return lst[k]

    return (_max(lst[:], k), _min(lst[:], k))


# binary search
# @premise: lst是已排序的递增序列
def binary_search(lst, val):
    low = 0
    high = len(lst) - 1
    while low <= high:
        mid = (low + high) / 2
        if lst[mid] < val:
            low = mid + 1
        elif lst[mid] > val:
            high = mid - 1
        else:
            return True
    return False


if __name__ == "__main__":
    lst = [5, 3, 6, 4, 3, 7, 8, 1]
    slst = [1, 3, 3, 4, 5, 6, 7, 8]
    print select(lst[:], 1)  # (7,3)
    print select2(lst[:], 1)  # (7,3)
    print binary_search(slst, 3)
