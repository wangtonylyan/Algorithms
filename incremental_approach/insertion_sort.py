# -*- coding: utf-8 -*-


import sys

sys.path.append("..")
import sort


# 插入排序非常适用于输入域增量式地动态变化
class InsertionSort(sort.Sort):
    def __init__(self):
        super(InsertionSort, self).__init__()
        self.funcs.append(self.main_iter)
        self.funcs.append(self.main_recur)

    def main_iter(self, lst):
        # i is an iterator, which means at the beginning of each outer loop,
        # it will be reset to the value next to its former
        for i in range(0, len(lst) - 1):
            t = lst[i + 1]
            # so in the inner loop, variable i can be reused
            while i >= 0 and lst[i] > t:
                lst[i + 1] = lst[i]
                i -= 1
            assert (i == -1 or lst[i] <= t)
            lst[i + 1] = t
        return lst

    def main_recur(self, lst):
        # inner loop: insert (bubble up) lst[0] into sorted lst[1:]
        def _insert(lst):
            if len(lst) < 2 or lst[0] <= lst[1]:
                return lst
            lst[0], lst[1] = lst[1], lst[0]
            return [lst[0]] + _insert(lst[1:])

        # outer loop: recursion and insert
        if len(lst) < 2:
            return lst
        lst[1:] = self.main_recur(lst[1:])
        return _insert(lst)


if __name__ == '__main__':
    InsertionSort().testcase()
    print 'done'
