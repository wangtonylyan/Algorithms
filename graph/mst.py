# -*- coding: utf-8 -*-
# minimum(-weight) spanning tree problem
# 生成树都只有V-1条边，所谓的最小是指权重
# Kruskal从“边”的角度入手，Prim从“点”的角度入手


class MinimumSpanningTree(object):
    def __init__(self, grp):
        self.grp = grp
        self.funcs = []

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
        # check test case
        num = 0
        for i in range(len(case)):
            for j, w1 in case[i]:
                for k, w2 in case[j]:
                    if k == i:
                        assert (w1 == w2 > 0)
                        num += 1
                        break
        assert (num == sum(map(len, case)))
        # run test case
        num = lambda mst: sum(map(lambda x: x[1], mst))
        g = self.__class__(case)
        assert (len(self.funcs) > 0)
        ret = getattr(g, self.funcs[0])()
        for i in range(len(g.grp)):
            assert (reduce(lambda x, y: x and num(getattr(g, y)(i)) == num(ret), self.funcs, True) == True)
        assert (len(ret) == len(case) - 1)
        assert (sum(map(lambda x: x[1], ret)) == 37)
        print 'pass:', self.__class__


class Kruskal(MinimumSpanningTree):
    def __init__(self, grp=[]):
        super(Kruskal, self).__init__(grp)
        self.funcs.append('main')

    def main(self, src=None):
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

        # 1) build edges
        edge = []
        for i in range(len(self.grp)):
            for j, w in self.grp[i]:
                if ((min(i, j), max(i, j)), w) not in edge:
                    edge.append(((min(i, j), max(i, j)), w))
        assert (len(edge) == sum(map(len, self.grp)) / 2)
        # 2) sort edges
        cnt = [0] * (max(map(lambda x: x[1], edge)) + 1)
        sort = [None] * len(edge)
        for e, w in edge:
            cnt[w] += 1
        for i in range(len(cnt) - 1):
            cnt[i + 1] += cnt[i]
        for e, w in edge:
            sort[cnt[w - 1]] = (e, w)
            cnt[w - 1] += 1
        # 3) build mst by selecting edges
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
        self.funcs.append("main_1")
        self.funcs.append("main_2")

    # 从树中的节点开始搜索
    def main_1(self, src=0):
        vtx = [0 if i != src else 1 for i in range(len(self.grp))]
        mst = []
        while len(mst) < len(self.grp) - 1:
            m = None
            for i in range(len(vtx)):
                if vtx[i] == 1:
                    for j, w in self.grp[i]:
                        if vtx[j] == 0 and (m == None or m[1] > w):
                            m = ((i, j), w)
            assert (m != None and vtx[m[0][0]] == 1 and vtx[m[0][1]] == 0)
            vtx[m[0][1]] = 1
            mst.append(m)
        return mst

    # 从树外的节点开始搜索
    def main_2(self, src=0):
        vtx = [0 if i != src else 1 for i in range(len(self.grp))]
        closest = [None] * len(self.grp)
        for i in range(len(self.grp)):
            if i != src:
                for j, w in self.grp[i]:
                    if j == src and (closest[i] == None or closest[i][1] > w):
                        closest[i] = (j, w)

        mst = []
        while len(mst) < len(vtx) - 1:
            m = None
            for i in range(len(vtx)):
                if vtx[i] == 0 and closest[i] != None:
                    assert (vtx[closest[i][0]] == 1)
                    if m == None or closest[m][1] > closest[i][1]:
                        m = i
            assert (m != None and vtx[m] == 0 and vtx[closest[m][0]] == 1)
            mst.append(((m, closest[m][0]), closest[m][1]))
            vtx[m] = 1
            # incremental approach
            for i in range(len(vtx)):
                if vtx[i] == 0:
                    for j, w in self.grp[i]:
                        if j == m:
                            if closest[i] == None or closest[i][1] > w:
                                closest[i] = (j, w)
                            break
        assert (sum(vtx) == len(vtx))
        return mst


if __name__ == '__main__':
    Kruskal().testcase()
    Prim().testcase()
    print 'done'
