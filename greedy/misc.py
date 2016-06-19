# -*- coding: utf-8 -*-

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
    FractionalKnapsack().testcase()
