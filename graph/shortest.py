# -*- coding: utf-8 -*-
# @problem: single-source shortest paths problem
# 针对于连通的有向图


from data_structure.heap.binary import MinBinaryHeap
from base.graph import DirectedAcyclicGraphTest
from sort import TopologicalSort


class ShortestPath(DirectedAcyclicGraphTest):
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
                if dis[i] is not None:
                    for j, w in grp[i]:
                        if dis[j] is None or dis[j] > dis[i] + w:
                            dis[j] = dis[i] + w
                            pre[j] = i
        # 3) check
        for i in range(len(grp)):
            if dis[i] is not None:
                for j, w in grp[i]:
                    if dis[j] is None or dis[j] > dis[i] + w:  # if there exists negative-weight cycle
                        return None
        # 4) build shortest-path tree
        return dis, pre

        for n in range(len(grp)):
            for i in range(len(grp)):
                if dis[i] is not None:
                    for j, w in grp[i]:
                        if dis[j] is None or dis[j] > dis[i] + w:
                            if n == len(grp) - 1:  # the last iteration is used to check
                                return None
                            dis[j] = dis[i] + w
                            pre[j] = i
        return dis, pre

    # dag (directed acyclic graph)
    # 仅适用于无环的有向图，O(V+E)
    def main_dag(self, grp, src):
        # 1) sort
        seq = TopologicalSort().main_Kahn(map(lambda x: map(lambda y: y[0], x), grp))
        if seq is None:
            return None  # this algorithm doesn't work
        assert (len(seq) == len(grp))
        # 2) initialize
        dis = [None if i != src else 0 for i in range(len(grp))]
        pre = [None] * len(grp)
        # 3) calculate
        for i in seq:
            if dis[i] is not None:
                for j, w in grp[i]:
                    if dis[j] is None or dis[j] > dis[i] + w:
                        dis[j] = dis[i] + w
                        pre[j] = i
        # 4) build shortest-path tree
        return dis, pre

    # weighted directed graph with non-negative-weight edges，仅适用于权值非负的有向图
    # Dijkstra与Prim的区别在于：
    # 1) dis数组中维护的是某点与源点之间的最短距离，而不是连接该点的边的最小权值
    # 2) 有向图中以任意点为起始点，未必可以到达其他所有点，即最短路径树未必包含了所有连通的点
    def main_Dijkstra_1(self, grp, src):
        # 1) initialize
        vtx = [0 if i != src else 1 for i in range(len(grp))]
        dis = [None if i != src else 0 for i in range(len(grp))]
        pre = [None] * len(grp)
        for i, w in grp[src]:
            dis[i] = w
            pre[i] = src
        # 2) calculate by greedily selecting vertexes from list
        for _ in range(len(grp) - 1):  # the 'src' vertex has been selected
            m = None
            for i in range(len(grp)):
                if vtx[i] == 0 and dis[i] is not None:
                    assert (vtx[pre[i]] == 1)
                    if m is None or dis[m] > dis[i]:
                        m = i
            if m is None:
                break
            assert (m is not None and vtx[m] == 0 and vtx[pre[m]] == 1)
            vtx[m] = 1
            for i, w in grp[m]:
                if vtx[i] == 0 and (dis[i] is None or dis[i] > dis[m] + w):
                    dis[i] = dis[m] + w
                    pre[i] = m
        # 3) build shortest-path tree
        return dis, pre

    def main_Dijkstra_2(self, grp, src):
        # 1) initialize
        vtx = [0 if i != src else 1 for i in range(len(grp))]
        dis = [None if i != src else 0 for i in range(len(grp))]
        pre = [None] * len(grp)
        hp = MinBinaryHeap(key=lambda x: x[1])
        for i, w in grp[src]:
            dis[i] = w
            pre[i] = src
            hp.push((i, dis[i]))
        # 2) calculate by greedily selecting vertexes from heap
        while len(hp) > 0:
            i, w = hp.pop()
            assert (dis[i] is not None and w >= dis[i])
            if w > dis[i] or vtx[i] != 0:
                continue
            vtx[i] = 1
            for j, v in grp[i]:
                if vtx[j] == 0 and (dis[j] is None or dis[j] > dis[i] + v):
                    dis[j] = dis[i] + v
                    pre[j] = i
                    hp.push((j, dis[j]))
        # 3) build shortest-path tree
        return dis, pre

    def testcase(self):
        def test(case):
            for i in range(len(case)):
                assert (self.main_BellmanFord(case, i) == self.main_dag(case, i)
                        == self.main_Dijkstra_1(case, i) == self.main_Dijkstra_2(case, i))

        self._testcase(test, self._gencase())


if __name__ == '__main__':
    ShortestPath().testcase()
    print 'done'
