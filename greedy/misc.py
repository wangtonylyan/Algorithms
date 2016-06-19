# -*- coding: utf-8 -*-

import random


# @problem: Given n activities with their start and finish times.
# Select the maximum number of activities that can be performed by a single person,
# assuming that a person can only work on a single activity at a time.
class ActivitySelection():
    def main_dynamic(self, lst):
        # 以下维护tab的逻辑对于输入的活动顺序有所依赖
        # 即对于任意活动lst[k]，lst[k:]中不能存在可以在其前被实施的活动
        # 基于开始时间或结束时间对lst进行排序都是满足上述条件的
        lst.sort(key=lambda x: x[0])
        lst.sort(key=lambda x: x[1])

        time = max(map(lambda x: x[1], lst))
        tab = [[0] * (len(lst) + 1) for i in range(time + 1)]
        for i in range(1, time + 1):
            for j in range(1, len(lst) + 1):
                tab[i][j] = max(tab[lst[j - 1][0]][j - 1] + 1 if lst[j - 1][1] <= i else 0,
                                tab[i][j - 1])

        return tab[-1][-1]

    def main_greedy_1(self, lst):
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
        for t in range(500):
            case = []
            for i in range(random.randint(5, 60)):
                start = random.randint(1, 30)
                end = random.randint(1, 30)
                while end == start:
                    end = random.randint(1, 30)
                start, end = min(start, end), max(start, end)
                if (start, end) not in case:
                    case.append((start, end))
            cases.append(case)

        map(test, cases)
        print 'pass:', self.__class__


from dynamic.knapsack import Knapsack


class FractionalKnapsack(Knapsack):
    def __init__(self):
        super(FractionalKnapsack, self).__init__()
        self.funcs.append(self.main_1)
        self.funcs.append(self.main_2)

    def main_1(self, weight, items):
        def recur(wgt, ind):
            if wgt <= 0 or ind >= len(items):
                return 0
            if wgt >= items[ind][0]:
                v = recur(wgt - items[ind][0], ind + 1) + items[ind][1]
            else:
                v = round(wgt * (float(items[ind][1]) / float(items[ind][0])), 4)
            return max(v, recur(wgt, ind + 1))

        return int(round(recur(weight, 0), 0))

    def main_2(self, weight, items):
        per = map(lambda x: float(x[1]) / float(x[0]), items)
        for i in range(len(items) - 1):
            m = i
            for j in range(i + 1, len(items)):
                if per[m] < per[j]:
                    m = j
            if m != i:
                items[i], items[m] = items[m], items[i]
                per[i], per[m] = per[m], per[i]

        ret = 0
        ind = 0
        while weight > 0 and ind < len(items):
            if weight >= items[ind][0]:
                ret += items[ind][1]
                weight -= items[ind][0]
            else:
                ret += round(weight * per[ind], 4)
                weight = 0
            ind += 1

        return int(round(ret, 0))


if __name__ == '__main__':
    ActivitySelection().testcase()
    FractionalKnapsack().testcase()
