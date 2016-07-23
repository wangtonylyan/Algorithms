# -*- coding: utf-8 -*-
# @problem: minimum(-weight) spanning tree (MST) and arborescence (MSA)
# 生成树都只有V-1条边，所谓的最小是指权重
# 针对于连通图，最小生成树属于无向图，最小树形图属于有向图


from graph import UndirectedGraph, DirectedGraph
from data_structure.tree.disjoint import DisjointSetForest


# Kruskal从“边”的角度入手，Prim从“点”的角度入手
# 以下四种基本算法都是贪婪算法，其核心是基于两大特性
# Assume that all edge costs are distinct.
# 1) cut property
# Let S be any subset of nodes that is neither empty nor equal to all of V,
# and let edge e = (v, w) be the minimum cost edge with one end in S and the other in V − S.
# Then every minimum spanning tree contains the edge e.
# 2) cycle property
# Let C be any cycle in G, and let edge e = (v, w) be the most expensive edge belonging to C.
# Then e does not belong to any minimum spanning tree of G.
class MinimumSpanningTree(UndirectedGraph):
    def __init__(self):
        super(MinimumSpanningTree, self).__init__()
        self.funcs = [self.main_Boruvka,
                      self.main_Kruskal,
                      self.main_Prim_1,
                      self.main_Prim_2]

    def main_Boruvka(self, grp, src=None):
        def union(sets, n1, n2):
            assert (n1 != n2)
            for i in range(len(sets)):
                if n1 in sets[i]:
                    n1 = i
                if n2 in sets[i]:
                    n2 = i
            assert (0 <= n1 < len(sets))
            assert (0 <= n2 < len(sets))
            if n1 != n2:
                sets[n1] += sets[n2]
                sets.remove(sets[n2])
            return n1

        sets = [[i] for i in range(len(grp))]
        mst = []
        ind = 0
        while len(sets) > 1:
            # check each connected component
            for set in sets:
                edge = []
                for i in set:
                    for j, w in grp[i]:
                        if j not in set:
                            edge.append(((i, j), w))
                assert (len(edge) > 0)
                (i, j), w = min(edge, key=lambda x: x[1])
                m = ((min(i, j), max(i, j)), w)
                if m not in mst:
                    mst.append(m)
            # update all connected components
            for (i, j), w in mst[ind:]:
                union(sets, i, j)
            ind = len(mst) - 1
        assert (len(mst) == len(grp) - 1)
        return mst

    # @algorithm: Reverse-Delete Algorithm
    # 与Kruskal思想互逆的算法：从权值最大的边开始删除
    # 如果删除某条边不会改变图的连通性，则可以删除之
    def main_Kruskal(self, grp, src=None):
        # 1) build edges array and sort
        edge = []
        for i in range(len(grp)):
            for j, w in grp[i]:
                m, n = min(i, j), max(i, j)
                if ((m, n), w) not in edge:
                    edge.append(((m, n), w))
        assert (len(edge) == sum(map(len, grp)) / 2)
        edge.sort(key=lambda x: x[1])
        # 2) build mst by selecting edges
        mst = []
        ds = DisjointSetForest(len(grp))
        for (i, j), w in edge:
            if ds.find(i) != ds.find(j):
                ds.union(i, j)
                mst.append(((i, j), w))
        assert (len(mst) == len(grp) - 1)
        return mst

    # 从树中的节点开始搜索
    def main_Prim_1(self, grp, src=0):
        vtx = [0 if i != src else 1 for i in range(len(grp))]
        mst = []
        for v in range(len(grp) - 1):
            m = None
            for i in range(len(grp)):
                if vtx[i] == 1:
                    for j, w in grp[i]:
                        if vtx[j] == 0 and (m == None or m[1] > w):
                            m = ((i, j), w)
            assert (m != None and vtx[m[0][0]] == 1 and vtx[m[0][1]] == 0)
            vtx[m[0][1]] = 1
            mst.append(m)
        assert (len(mst) == len(grp) - 1)
        assert (sum(vtx) == len(vtx))
        return mst

    # 从树外的节点开始搜索
    def main_Prim_2(self, grp, src=0):
        # 1) initialize
        vtx = [0 if i != src else 1 for i in range(len(grp))]
        dis = [None if i != src else 0 for i in range(len(grp))]
        pre = [None] * len(grp)
        for i, w in grp[src]:
            dis[i] = w
            pre[i] = src
        # 2) build mst by selecting vertices
        mst = []
        for v in range(len(grp) - 1):
            m = None
            for i in range(len(grp)):
                if vtx[i] == 0 and dis[i] != None:
                    assert (vtx[pre[i]] == 1)
                    if m == None or dis[m] > dis[i]:
                        m = i
            assert (m != None and vtx[m] == 0 and vtx[pre[m]] == 1)
            mst.append(((m, pre[m]), dis[m]))
            vtx[m] = 1
            # update dis array by incremental approach
            for i, w in grp[m]:
                if vtx[i] == 0 and (dis[i] == None or dis[i] > w):
                    dis[i] = w
                    pre[i] = m
        assert (len(mst) == len(grp) - 1)
        assert (sum(vtx) == len(vtx))
        return mst

    def testcase(self):
        def test(case):
            num = lambda mst: sum(map(lambda x: x[1], mst))
            assert (len(self.funcs) > 0)
            ret = self.funcs[0](case)
            for i in range(len(case)):
                assert (reduce(lambda x, y: x and num(y(case, i)) == num(ret), self.funcs, True) == True)
            assert (len(ret) == len(case) - 1)

        self._testcase(test, self.gencase_weighted())


class MinimumSpanningArborescence(DirectedGraph):
    def __init__(self):
        super(MinimumSpanningArborescence, self).__init__()

    def main_Edmonds(self, grp, src):
        msa = []
        pass


if __name__ == '__main__':
    MinimumSpanningTree().testcase()
    print 'done'
