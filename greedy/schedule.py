# -*- coding: utf-8 -*-

import random


# @problem: interval scheduling
# @reference: <Algorithm Design> 4.1
# 给定若干个区间，求互不重叠区间所能组成的最大集合
# 1) 证明：由于贪婪算法的迭代过程中，每步可供选择的区间不会少于最优算法
# 于是每步所得的解也都不会差于(结束时间晚于或开始时间早于)最优解
# 因此此贪婪算法的解就是最优解
# 2) 几种错误的贪婪策略：
# (a) 选择开始时间最早的区间
# (b) 选择持续时间最短的区间
# (c) 选择与其他区间冲突最少的区间
class IntervalSchedule():
    # @problem: weighted interval scheduling
    # 无权重的版本就相当于所有区间的权重值都为1
    def main_dynamic(self, lst):
        # 以下维护tab的逻辑对于输入的活动顺序有所依赖
        # 即对于任意活动lst[k]，lst[k:]中不能存在可以在其前被实施的活动
        # 基于开始时间或结束时间对lst进行排序都是满足上述条件的
        lst.sort(key=lambda x: x[0])
        lst.sort(key=lambda x: x[1])

        time = max(map(lambda x: x[1], lst))
        tab = [[0] * (len(lst) + 1) for _ in range(time + 1)]
        for i in range(1, time + 1):
            for j in range(1, len(lst) + 1):
                tab[i][j] = max(tab[lst[j - 1][0]][j - 1] + 1 if lst[j - 1][1] <= i else 0,
                                tab[i][j - 1])

        return tab[-1][-1]

    def main_greedy_1(self, lst):
        # 贪婪算法中排序为的是事先得出每次贪婪决策的结果
        lst.sort(key=lambda x: x[1])  # sort by finish time
        ret = [lst[0]]  # greedy choice: the first one to finish
        for i in range(1, len(lst)):
            if lst[i][0] >= ret[-1][1]:
                ret.append(lst[i])
        return len(ret)

    def main_greedy_2(self, lst):
        lst.sort(key=lambda x: x[0])  # sort by start time
        ret = [lst[-1]]  # greedy choice: the last one to start
        for i in range(len(lst) - 2, -1, -1):
            if lst[i][1] <= ret[-1][0]:
                ret.append(lst[i])
        return len(ret)

    def testcase(self):
        def test(lst):
            assert (self.main_dynamic(lst[:]) ==
                    self.main_greedy_1(lst[:]) ==
                    self.main_greedy_2(lst[:]))

        cases = []
        for _ in range(500):
            case = []
            for _ in range(random.randint(5, 60)):
                st = random.randint(0, 30)
                ft = random.randint(0, 30)
                while ft == st:
                    ft = random.randint(0, 30)
                st, ft = min(st, ft), max(st, ft)
                if (st, ft) not in case:
                    case.append((st, ft))
            cases.append(case)

        map(test, cases)
        print 'pass:', self.__class__


# @problem: <Algorithm Design> 4.1
# 给定若干个区间，求能够包含所有区间且各自元素互不重叠的集合的最少个数
# 该算法会对任意两个区间进行一次是否重叠的判断
class IntervalPartition():
    def __init__(self):
        self.isOverlapped = lambda lst, i, j: lst[i][0] < lst[j][1] and lst[i][1] > lst[j][0]

    def main(self, lst):
        dpt = [0] * len(lst)
        for i in range(len(lst)):
            # 为每个区间分配一个与其之前所有重叠区间都不同的分区
            assert (dpt[i] == 0)
            for j in range(i):
                if self.isOverlapped(lst, i, j):
                    dpt[i] |= 1 << dpt[j]
            k = 0
            while dpt[i] & (1 << k) != 0:
                k += 1
            dpt[i] = k

        part = [[] for i in range(max(dpt) + 1)]
        for i in range(len(lst)):
            part[dpt[i]].append(lst[i])
        return part

    def testcase(self):
        def test(case):
            dpt = [0] * len(case)
            for i in range(len(case) - 1):
                for j in range(i + 1, len(case)):
                    if self.isOverlapped(case, i, j):
                        dpt[j] += 1

            ret = self.main(case[:])
            assert (sum(map(len, ret)) == len(case))
            assert (len(ret) <= max(dpt) + 1)
            for i in ret:
                for j in range(len(i) - 1):
                    assert (not self.isOverlapped(i, j, j + 1))

        cases = []
        for _ in range(500):
            case = []
            for _ in range(random.randint(5, 60)):
                st = random.randint(0, 30)
                ft = random.randint(0, 30)
                while ft == st:
                    ft = random.randint(0, 30)
                st, ft = min(st, ft), max(st, ft)
                if (st, ft) not in case:
                    case.append((st, ft))
            cases.append(case)

        map(test, cases)
        print 'pass:', self.__class__


# @problem: <Algorithm Design> 4.2
# 给定每个任务的持续时间和截止时间，求最少延期
# 几种错误的贪婪策略：
# (a) 选择持续时间最短的任务
# (b) 选择截止时间与持续时间之差最小的任务
class MinimizeLateness():
    def main(self, lst):
        lst.sort(key=lambda x: x[1])  # sort by deadline
        time = 0
        ret = []
        # greedy choice: Earliest Deadline First
        for lt, dt in lst:
            ret.append((time, time + lt, 0 if time + lt <= dt else time + lt - dt))
            time += lt
        assert (time == sum(map(lambda x: x[0], lst)))
        return ret

    def testcase(self):
        def test(case):
            ret = self.main(case[:])

        cases = []
        for _ in range(500):
            case = []
            for _ in range(random.randint(5, 60)):
                lt = random.randint(1, 10)  # interval length
                dt = random.randint(lt * 5, lt * 10)  # deadline
                if (lt, dt) not in case:
                    case.append((lt, dt))
            cases.append(case)

        map(test, cases)
        print 'pass:', self.__class__


# @problem: <Introduction to Algorithms> 16.6
# 给定若每个任务的持续时间，求最少的任务平均完成时间
class MinimizeAverageCompletionTime():
    def main(self, lst):
        lst.sort()
        time = 0
        total = 0
        for i in lst:
            time += i
            total += time
        return total / len(lst)

    def testcase(self):
        assert (self.main([1, 2, 3, 4, 5, 6]) == 9)
        print 'pass:', self.__class__


if __name__ == '__main__':
    IntervalSchedule().testcase()
    IntervalPartition().testcase()
    MinimizeLateness().testcase()
    MinimizeAverageCompletionTime().testcase()
