# -*- coding: utf-8 -*-

# @problem: 渡轮问题
# 一条河的两岸各有n个城市，每个城市都有一个位于其河对岸的友好城市
# 现需在两个友好城市之间建立一条航线，但要求所有的航线都不能相交
# 求最多可以建立多少条不交叉的航线？
class Ferry():
    def __init__(self):
        pass

    def main_1(self, map):
        tab = [[0 for col in range(len(map) + 1)] for row in range(len(map) + 1)]
        for i in range(1, len(map) + 1):
            for j in range(1, len(map) + 1):
                tab[i][j] = max(tab[i - 1][map[i - 1] - 1] + 1 if j >= map[i - 1] else 0,
                                tab[i - 1][j])
        return tab[-1][-1]

    def main_2(self, map):
        tab = [0] * (len(map) + 1)
        for i in range(len(map)):
            for j in range(1, len(map) + 1):
                tab[j] = max(tab[map[i] - 1] + 1 if j >= map[i] else 0,
                             tab[j])
        return tab[-1]

    def testcase(self):
        # 数组的索引值与其中的内容构成一对友好城市
        map = [7, 8, 4, 3, 5, 1, 6, 2]
        assert (self.main_1(map[:]) == self.main_2(map[:]))
        print 'pass:', self.__class__


if __name__ == '__main__':
    Ferry().testcase()
    print 'done'
