# -*- coding: utf-8 -*-
# @problem: single-source shortest paths problem
# 针对于连通的有向图


from graph import DirectedAcyclicGraph
from sort import TopologicalSort


class ShortestPath(DirectedAcyclicGraph):
    def __init__(self):
        super(ShortestPath, self).__init__(True)

    # weighted directed graph
    # 适合于任何带权值的有向图，O(VE)
    def main_BellmanFord(self, grp, src):
        # 1) initialize
        dis = [None if i != src else 0 for i in range(len(grp))]
        pre = [None] * len(grp)
        # 2) calculate
        # best: 1->2->...->n
        # worst: n->n-1->...->1
        for _ in range(len(grp) - 1):
            for i in range(len(grp)):
                if dis[i] != None:
                    for j, w in grp[i]:
                        if dis[j] == None or dis[j] > dis[i] + w:
                            dis[j] = dis[i] + w
                            pre[j] = i
        # 3) check
        for i in range(len(grp)):
            for j, w in grp[i]:
                if dis[i] != None and (dis[j] == None or dis[j] > dis[i] + w):  # if there exists negative-weight cycle
                    return None
                assert (dis[i] == None or (dis[i] != None and dis[j] != None and dis[j] <= dis[i] + w))
        # 4) build shortest-path tree
        pass
        return dis, pre

    # dag (directed acyclic graph)
    # 仅适用于无环的有向图，O(V+E)
    def main_dag(self, grp, src):
        # 1) sort
        unwgt = map(lambda x: map(lambda y: y[0], x), grp)
        seq = TopologicalSort().main_Kahn(unwgt)
        if seq == None:
            return None  # this algorithm doesn't work
        assert (len(seq) == len(grp))
        # 2) initialize
        dis = [None if i != src else 0 for i in range(len(grp))]
        pre = [None] * len(grp)
        # 3) calculate
        for i in seq:
            if dis[i] != None:
                for j, w in grp[i]:
                    if dis[j] == None or dis[j] > dis[i] + w:
                        dis[j] = dis[i] + w
                        pre[j] = i
        # 4) build shortest-path tree
        pass
        return dis, pre

    # weighted directed graph with nonnegative-weight edges
    # 适用于权值非负的有向图
    # Dijkstra与Prim的区别在于：
    # 1) dis数组中维护的是某点与源点之间的最短距离，而不是连接该点的边的最小权值
    # 2) 有向图中以任意点为起始点，未必可以到达其他所有点
    # 换言之，最短路径树未必包含了所有连通的点
    def main_Dijkstra(self, grp, src):
        # 1) initialize
        vtx = [0 if i != src else 1 for i in range(len(grp))]
        dis = [None if i != src else 0 for i in range(len(grp))]
        pre = [None] * len(grp)
        for i, w in grp[src]:
            dis[i] = w
            pre[i] = src
        # 2) calculate by selecting vertices
        for _ in range(len(grp) - 1):
            m = None
            for i in range(len(grp)):
                if vtx[i] == 0 and dis[i] != None:
                    assert (vtx[pre[i]] == 1)
                    if m == None or dis[m] > dis[i]:
                        m = i
            if m == None:
                break
            assert (m != None and vtx[m] == 0 and vtx[pre[m]] == 1)
            vtx[m] = 1
            for i, w in grp[m]:
                if vtx[i] == 0 and (dis[i] == None or dis[i] > dis[m] + w):
                    dis[i] = dis[m] + w
                    pre[i] = m
        # 3) build shortest-path tree
        pass
        return dis, pre

    def testcase(self):
        def test(case):
            for i in range(len(case)):
                assert (self.main_BellmanFord(case, i) == self.main_dag(case, i)
                        == self.main_Dijkstra(case, i))

        self._testcase(test, self._gencase())


if __name__ == '__main__':
    ShortestPath().testcase()
    print 'done'
