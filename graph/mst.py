# -*- coding: utf-8 -*-
# @problem: minimum(-weight) spanning tree
# 生成树都只有V-1条边，所谓的最小是指权重
# 针对于连通的无向图


# Kruskal从“边”的角度入手，Prim从“点”的角度入手
class MinimumSpanningTree():
    def __init__(self):
        self.funcs = [self.main_Kruskal,
                      self.main_Prim_1,
                      self.main_Prim_2]

    def main_Kruskal(self, grp, src=None):
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

        # 1) build edge array
        edge = []
        for i in range(len(grp)):
            for j, w in grp[i]:
                if ((min(i, j), max(i, j)), w) not in edge:
                    edge.append(((min(i, j), max(i, j)), w))
        assert (len(edge) == sum(map(len, grp)) / 2)
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
        sets = [i for i in range(len(grp) + 1)]  # disjoint set
        for (i, j), w in sort:
            if find(sets, i) != find(sets, j):
                union(sets, i, j)
                mst.append(((i, j), w))
        assert (len(mst) == len(grp) - 1)
        return mst

    # 从树中的节点开始搜索
    def main_Prim_1(self, grp, src=0):
        vtx = [0 if i != src else 1 for i in range(len(grp))]
        mst = []
        for v in range(len(grp) - 1):
            m = None
            for i in range(len(vtx)):
                if vtx[i] == 1:
                    for j, w in grp[i]:
                        if vtx[j] == 0 and (m == None or m[1] > w):
                            m = ((i, j), w)
            assert (m != None and vtx[m[0][0]] == 1 and vtx[m[0][1]] == 0)
            vtx[m[0][1]] = 1
            mst.append(m)
        assert (len(mst) == len(grp) - 1)
        return mst

    # 从树外的节点开始搜索
    def main_Prim_2(self, grp, src=0):
        # 1) initialize
        vtx = [0 if i != src else 1 for i in range(len(grp))]
        dis = [None] * len(grp)
        for i, w in grp[src]:
            dis[i] = (src, w)
        # 2) build mst by selecting vertices
        mst = []
        for v in range(len(grp) - 1):
            m = None
            for i in range(len(vtx)):
                if vtx[i] == 0 and dis[i] != None:
                    assert (vtx[dis[i][0]] == 1)
                    if m == None or dis[m][1] > dis[i][1]:
                        m = i
            assert (m != None and vtx[m] == 0 and vtx[dis[m][0]] == 1)
            mst.append(((m, dis[m][0]), dis[m][1]))
            vtx[m] = 1
            # update dis array by incremental approach
            for i, w in grp[m]:
                if vtx[i] == 0 and (dis[i] == None or dis[i][1] > w):
                    dis[i] = (m, w)
        assert (len(mst) == len(grp) - 1)
        assert (sum(vtx) == len(vtx))
        return mst

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
        assert (len(self.funcs) > 0)
        ret = self.funcs[0](case[:])
        for i in range(len(case)):
            assert (reduce(lambda x, y: x and num(y(case[:], i)) == num(ret), self.funcs, True) == True)
        assert (len(ret) == len(case) - 1)
        assert (sum(map(lambda x: x[1], ret)) == 37)
        print 'pass:', self.__class__


if __name__ == '__main__':
    MinimumSpanningTree().testcase()
    print 'done'
