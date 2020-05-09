if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))

from algorithms.utility import *


# 排序可以看作是一种分治算法，其主要涉及到了以下两个阶段
# split，将一个数组分解为规模更小的子数组
# join，将规模更小的子数组合并成更大规模的原数组
# 根据the law of entropy，仅有以下两种组合，
# 1. hard split + easy join
#    bubble, selection, quick
# 2. easy split + hard join
#    insertion, shell, merge

# 1. stable
#    bubble, insertion, merge, radix
# 2. unstable
#    selection, shell, quick, heap

# 实际中推荐使用快速排序(随机访问，倾向数组)和合并排序(顺序访问，倾向链表)
#########################################################################################
class Sorting(Problem):
    def check(self, lst):
        return self.check_list_nonempty(lst)


class ComparisonBasedSorting(Sorting):
    def algo_bubble(self, lst):
        for i in range(len(lst) - 1, 0, -1):
            swap = False
            for j in range(i):
                if lst[j] > lst[j + 1]:  # 不使用等号，以保证稳定性
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
                    swap = True
            if not swap:
                break
        return lst

    def algo_select(self, lst):
        for i in range(len(lst) - 1, 0, -1):
            m = i
            for j in range(i):
                if lst[j] > lst[m]:
                    m = j
            if m != i:
                # 可以将lst[m+1:i+1]整体向前平移一位，随后再赋值lst[i]
                # 可见，正是以下减少元素移动的策略，才破坏了选择排序的稳定性
                lst[i], lst[m] = lst[m], lst[i]
        return lst

    def algo_insert(self, lst):
        for i in range(1, len(lst)):
            t, j = lst[i], i
            while j >= 1 and lst[j - 1] > t:
                lst[j] = lst[j - 1]
                j -= 1
            lst[j] = t
        return lst

    def algo_shell(self, lst):
        # 整个算法的时间复杂度，与以下被选用的序列相关
        gaps = [701, 301, 132, 57, 23, 10, 4, 1]  # Marcin Ciura's gap sequence
        # 以[i, i+gap, i+gap*2, ...]为一组，对原数组进行分组
        # 对每个分组分别执行插入排序
        for gap in gaps:
            # 当gap=1时，该循环也就退化成了插入排序
            for i in range(gap, len(lst)):
                m, j = lst[i], i
                while j >= gap and lst[j - gap] > m:
                    lst[j] = lst[j - gap]
                    j -= gap
                lst[j] = m
        return lst

    def algo_quick1(self, lst):
        def recur(start, end):
            if end - start <= 1:
                return

            mid = self.quick_partition_1way(lst, start, end)
            # mid = self.quick_partition_2way(lst, start, end)

            recur(start, mid)
            recur(mid + 1, end)

        recur(0, len(lst))
        return lst

    def algo_quick2(self, lst):
        stk = [(0, len(lst))]

        while len(stk) > 0:
            start, end = stk.pop()

            # mid = self.quick_partition_1way(lst, start, end)
            mid = self.quick_partition_2way(lst, start, end)

            if mid - start > 1:
                stk.append((start, mid))
            if end - (mid + 1) > 1:
                stk.append((mid + 1, end))

        return lst

    # Quick sort is faster in practice, because its inner loop is efficiently
    # implemented on most architectures, and for most real-world data.
    @staticmethod
    def quick_partition_1way(lst, start, end):
        p = lst[start]
        i = start

        for j in range(i + 1, end):
            if lst[j] < p:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        lst[start], lst[i] = lst[i], lst[start]

        return i

    @staticmethod
    def quick_partition_2way(lst, start, end):
        p = lst[start]
        i, j = start, end - 1

        while i < j:
            while i < j and lst[j] >= p:
                j -= 1
            lst[i] = lst[j]

            while i < j and lst[i] <= p:
                i += 1
            lst[j] = lst[i]

        assert i == j
        lst[i] = p
        return i

    def algo_merge(self, lst):
        pass

    def algo_heap(self, lst):
        pass


class NonComparisonBasedSorting(Sorting):
    def algo_counting(self, lst):
        pass

    def algo_radix(self, lst):
        pass

    def algo_bucket(self, lst):
        pass


if __name__ == "__main__":
    Problem.testsuit([
        [ComparisonBasedSorting, [1, 2, 3, 4, 5], [5, 1, 3, 2, 4]],
        [ComparisonBasedSorting, [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]],
    ])
