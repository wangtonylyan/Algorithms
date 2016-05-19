# -*- coding: utf-8 -*-
# @problem: single-source shortest paths problem


class BellmanFord():
    def __init__(self, grp=[]):
        self.grp = grp

    def main(self):
        # 1) init
        src = 0
        dis = [-1 if i != src else 0 for i in range(len(self.grp))]
        for v in range(len(self.grp) - 1):
            for i in range(len(self.grp)):
                for j, w in self.grp[i]:
                    if dis[i] != -1 and (dis[j] == -1 or dis[j] > dis[i] + w):
                        dis[j] = dis[i] + w
        # 2) check
        for i in range(len(self.grp)):
            for j, w in self.grp[i]:
                if dis[i] != -1 and dis[j] > dis[i] + w:
                    return None

    def testcase(self):
        case = [
            [(1, 4), (7, 8)],
            [(2, 8), (7, 11)],
            [(8, 2), (3, 7), (5, 4)],
            [(4, 9), (5, 14)],
            [(5, 10)],
            [(6, 2)],
            [(7, 1), (8, 6)],
            [],
            []
        ]
        g = self.__class__(case)
        g.main()
        print 'pass:', self.__class__


if __name__ == '__main__':
    BellmanFord().testcase()
    print 'done'
