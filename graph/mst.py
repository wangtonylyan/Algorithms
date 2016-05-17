# -*- coding: utf-8 -*-
# minimum(-weight) spanning tree problem
# 生成树都只有V-1条边，所谓的最小是指权重


class MinimumSpanningTree(object):
    def __init__(self, grp):
        edge = []
        for i in range(len(grp)):
            for j, w in grp[i]:
                flg = True
                for e, v in edge:
                    if cmp((min(i, j), max(i, j)), e) == 0:
                        flg = False
                        break
                if flg:
                    edge.append(((min(i, j), max(i, j)), w))
        assert (len(edge) == sum(map(len, grp)) / 2)

        self.grp = grp
        self.edge = edge

    def testcase(self):
        case = [
            [(1, 4), (7, 8)],
            [(0, 4), (2, 8), (7, 11)],
            [(1, 8), (8, 2), (3, 7), (5, 4)],
            [(2, 7), (4, 9), (5, 14)],
            [(3, 9), (5, 10)],
            [(2, 4), (3, 14), (4, 10), (6, 2)],
            [(5, 2), (7, 1), (8, 6)],
            [(0, 8), (1, 11), (8, 7), (6, 1)],
            [(2, 2), (6, 6), (7, 7)]
        ]

        edge = 0
        for i in range(len(case)):
            for j, w1 in case[i]:
                for k, w2 in case[j]:
                    if k == i:
                        assert (w1 == w2 > 0)
                        edge += 1
                        break
        assert (edge == sum(map(len, case)))

        g = self.__class__(case)
        mst = g.main()
        assert (len(mst) == len(case) - 1)
        assert (sum(map(lambda x: x[1], mst)) == 37)
        print 'pass:', self.__class__


class Kruskal(MinimumSpanningTree):
    def __init__(self, grp=[]):
        super(Kruskal, self).__init__(grp)

    def main(self):
        def find(ds, n):
            while ds[n] != n:
                ds[n] = ds[ds[n]]
                n = ds[n]
            return n

        def union(ds, n1, n2):
            p1 = find(ds, n1)
            p2 = find(ds, n2)
            if p1 != p2:
                ds[p2] = p1
            return p1

        # 1) sort
        cnt = [0] * (max(map(lambda x: x[1], self.edge)) + 1)
        sort = [None] * len(self.edge)
        for e, w in self.edge:
            cnt[w] += 1
        for i in range(len(cnt) - 1):
            cnt[i + 1] += cnt[i]
        for e, w in self.edge:
            sort[cnt[w - 1]] = (e, w)
            cnt[w - 1] += 1
        # 2) select
        mst = []
        sets = [i for i in range(len(self.grp) + 1)]  # disjoint set
        for (i, j), w in sort:
            if find(sets, i) != find(sets, j):
                union(sets, i, j)
                mst.append(((i, j), w))
        assert (len(mst) == len(self.grp) - 1)
        return mst


class Prim(MinimumSpanningTree):
    def __init__(self, grp=[]):
        super(Prim, self).__init__(grp)

    def main(self):
        pass


if __name__ == '__main__':
    Kruskal().testcase()
    # Prim().testcase()
    print 'done'
