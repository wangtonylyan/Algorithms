# -*- coding: utf-8 -*-


import sys, random

sys.path.append("..")
import sort


class MergeSort(sort.Sort):
    def __init__(self):
        super(MergeSort, self).__init__()
        self.funcs.append(self.main_1)
        self.funcs.append(self.main_2)
        self.funcs.append(self.main_3)

    @staticmethod
    def _merge(lst, low, mid, high):  # [low,high)
        # auxliary space
        t1 = lst[low:mid]
        t2 = lst[mid:high]
        i, j = 0, 0
        while i < len(t1) and j < len(t2):
            if t1[i] <= t2[j]:
                lst[low + i + j] = t1[i]
                i += 1
            else:
                lst[low + i + j] = t2[j]
                j += 1
        if i < len(t1):
            assert (j == len(t2))
            lst[low + i + j:high] = t1[i:]
        else:
            assert (i == len(t1) and j < len(t2))
            lst[low + i + j:high] = t2[j:]

    # bottom-up, iterative
    def main_1(self, lst):
        step = 1
        while step < len(lst):
            i = 0
            while i + step + step <= len(lst):
                self._merge(lst, i, i + step, i + step + step)
                i += step + step
            # 以下处理边界情况
            if i + step < len(lst):
                self._merge(lst, i, i + step, len(lst))
            step *= 2
        return lst

    # top-down, iterative
    def main_2(self, lst):
        stk = [0, len(lst)]
        low, high = 0, len(stk)
        while low < high:
            for i in range(low, high, 2):
                if stk[i + 1] - stk[i] < 2:
                    continue
                mid = stk[i] + (stk[i + 1] - stk[i]) / 2
                if mid - stk[i] > 1:
                    stk.append(stk[i])
                    stk.append(mid)
                if stk[i + 1] - mid > 1:
                    stk.append(mid)
                    stk.append(stk[i + 1])
            low = high
            high = len(stk)
        for i in range(len(stk) - 1, -1, -2):
            mid = stk[i - 1] + (stk[i] - stk[i - 1]) / 2
            self._merge(lst, stk[i - 1], mid, stk[i])
        return lst

    # top-down, recursive
    def main_3(self, lst):
        def _merge(lst1, lst2):
            if len(lst1) == 0:
                return lst2
            elif len(lst2) == 0:
                return lst1
            if lst1[0] <= lst2[0]:
                return [lst1[0]] + _merge(lst1[1:], lst2)
            else:
                return [lst2[0]] + _merge(lst1, lst2[1:])

        # recursion and merge
        if len(lst) < 2:
            return lst
        mid = len(lst) >> 1
        return _merge(self.main_3(lst[:mid]), self.main_3(lst[mid:]))


# @problem:
# Inversion Count for an array indicates – how far (or close) the array is from being sorted.
# If array is already sorted then inversion count is 0. If array is sorted in reverse order that inversion count is the maximum.
# e.g. The sequence [2, 4, 1, 3, 5] has three inversions (2, 1), (4, 1), (4, 3).
class CountInversionsInArray():
    # recursive sort with iterative merge, in place
    def main(self, lst):
        # count inversions during merge
        def _merge(low, mid, high):
            count = 0
            alst1 = lst[low:mid]
            alst2 = lst[mid:high]
            i, j = 0, 0
            while i < len(alst1) and j < len(alst2):
                if alst1[i] <= alst2[j]:
                    lst[low + i + j] = alst1[i]
                    i += 1
                else:
                    lst[low + i + j] = alst2[j]
                    j += 1
                    count += len(alst1) - i  # the only difference with MergeSort
            if i == mid - low:
                lst[low + i + j:high] = alst2[j:]
            else:
                lst[low + i + j:high] = alst1[i:]
            return count

        def _recur(low, high):
            if high - low <= 1:
                return 0
            mid = low + ((high - low) >> 1)
            count = _recur(low, mid)
            count += _recur(mid, high)
            count += _merge(low, mid, high)
            return count

        return _recur(0, len(lst))

    def testcase(self):
        def test(lst):
            # brute-force algorithm
            count = 0
            for i in range(0, len(lst) - 1):
                for j in range(i + 1, len(lst)):
                    if lst[i] > lst[j]:
                        count += 1
            # check
            cpy = lst[:]
            cpy.sort()
            assert (self.main(lst) == count)
            assert (lst == cpy)

        cases = [[1], [1, 2], [2, 1]]
        for i in range(20):
            lst = [random.randint(0, 100) for i in range(random.randint(5, 50))]
            random.shuffle(lst)
            cases.append(lst)
        map(test, cases)
        print 'pass:', self.__class__


# @problem: sort one linked list
# 合并排序相比于其他排序，无需过多的随机访问
# 因此非常适用于链表排序
class SortLinkedList():
    class Node():
        def __init__(self, value, next=None):
            self.value = value
            self.next = next

    def _insert(self, lst, value):
        return self.__class__.Node(value, lst) if lst else self.__class__.Node(value)

    def main(self, lst):
        def _split(lst):
            slow = lst  # tortoise
            fast = lst.next  # hare
            while fast != None:
                fast = fast.next
                if fast:
                    # update slow pointer here
                    slow = slow.next
                    fast = fast.next
            # so that slow is before the midpoint in the list
            ret = slow.next
            # then split the list into two
            slow.next = None
            return ret

        def _merge(lst1, lst2):
            if lst1 == None:
                return lst2
            elif lst2 == None:
                return lst1
            if lst1.value <= lst2.value:
                lst1.next = _merge(lst1.next, lst2)
                return lst1
            else:
                lst2.next = _merge(lst1, lst2.next)
                return lst2

        # recursion and merge
        if lst == None or lst.next == None:
            return lst
        mid = _split(lst)
        lst = self.main(lst)
        mid = self.main(mid)
        return _merge(lst, mid)

    def testcase(self):
        def test(lst):
            llst = None
            for i in lst:
                llst = self._insert(llst, i)
            llst = self.main(llst)
            lst.sort()
            i = 0
            while llst and i < len(lst):
                assert (llst.value == lst[i])
                llst = llst.next
                i += 1
            assert (llst == None and i == len(lst))

        cases = [[1], [1, 2], [2, 1]]
        for i in range(20):
            lst = [random.randint(0, 100) for i in range(random.randint(5, 50))]
            random.shuffle(lst)
            cases.append(lst)
        map(test, cases)
        print 'pass:', self.__class__


if __name__ == '__main__':
    MergeSort().testcase()
    CountInversionsInArray().testcase()
    SortLinkedList().testcase()
    print 'done'
