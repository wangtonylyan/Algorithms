# -*- coding: utf-8 -*-
# @problem: graph traversal
# 针对于无向图
# BFS：bipartite graph
# DFS：topological sort


import copy
from data_structure.queue import Queue
from data_structure.stack import Stack


def graph_traverse_check(func):
    def f(self, src):
        assert (self.vtx and isinstance(self.vtx, list) and len(self.vtx) > 0)
        assert (self.grp and isinstance(self.grp, list) and len(self.grp) > 0)
        assert (len(self.vtx) == len(self.grp))
        assert (0 <= src < len(self.vtx))
        self._clear()
        for v in self.vtx:
            assert (v.state == 0)
        ret = func(self, src)
        for v in self.vtx:
            assert (v.state == 0 or v.state == 2)
        return ret

    return f


class Graph(object):
    class Vertex():
        def __init__(self):
            self.state = 0
            self.depth = 0  # 最小深度，层次
            self.time = [0, 0]  # 首次和末次访问的顺序

        def clear(self):
            self.state = 0
            self.depth = 0
            self.time = [0, 0]

    def __init__(self):
        pass

    def _clear(self):
        map(lambda x: getattr(x, 'clear')(), self.vtx)

    def testcase(self):
        case = [[1, 4],
                [0, 5],
                [3, 5, 6],
                [2, 6, 7],
                [0],
                [1, 2, 6],
                [2, 3, 5, 7],
                [3, 6]]
        g = self.__class__(case)

        for i in range(len(g.vtx)):
            g.bfs_iter(i)
            gb = copy.deepcopy(g.vtx)
            for j in range(len(g.vtx)):
                if j != i:
                    g.bfs_iter(j)
                    assert (gb[j].depth == g.vtx[i].depth)

            g.dfs_iter(i)
            gd1 = map(lambda x: copy.deepcopy(x.time), g.vtx)
            g.dfs_recur(i)
            gd2 = map(lambda x: copy.deepcopy(x.time), g.vtx)
            assert (gd1 == gd2)

        print 'pass:', self.__class__


def check_param(func):
    def f(self, grp, *args):
        assert (isinstance(grp, list) and reduce(lambda x, y: x and isinstance(y, list), grp, True))
        return func(self, grp, args)

    return f


class GraphList(Graph):
    def __init__(self):
        super(GraphList, self).__init__()

    @check_param
    def bfs_iter_singleSource(self, grp, src):
        assert (0 <= src < len(grp))
        vtx = [0] * len(grp)
        que = Queue()
        vtx[src] = 1
        que.push(src)
        while len(que) > 0:
            i = que.pop()
            assert (vtx[i] == 1)
            for j in grp[i]:
                if vtx[j] == 0:
                    vtx[j] = 1
                    que.push(j)

        assert (vtx.count(1) == sum(vtx))
        return sum(vtx)

    @check_param
    def dfs_iter_singleSource(self, grp, src):
        assert (0 <= src < len(grp))
        vtx = [0] * len(grp)
        stk = Stack()
        vtx[src] = 1
        stk.push(src)
        while len(stk) > 0:
            i = stk.pop()
            assert (vtx[i] == 1)
            for j in grp[i]:
                if vtx[j] == 0:
                    stk.push(i)
                    vtx[j] = 1
                    stk.push(j)
                    break

        assert (vtx.count(1) == sum(vtx))
        return sum(vtx)

    @check_param
    def dfs_recur_singleSource(self, grp, src):
        assert (0 <= src < len(grp))

        def recur(src):
            assert (vtx[src] == 0)
            vtx[src] = 1
            for i in grp[src]:
                if vtx[i] == 0:
                    recur(i)

        vtx = [0] * len(grp)
        recur(src)

        assert (vtx.count(1) == sum(vtx))
        return sum(vtx)

    def testcase(self):
        pass


class UndirectedGraphList(GraphList):
    def __init__(self):
        super(UndirectedGraphList, self).__init__()

    @check_param
    def bfs_iter(self, src):
        que = Queue()
        self.vtx[src].state = 1
        self.vtx[src].depth = 0
        que.push(src)
        while len(que) > 0:
            i = que.pop()
            assert (self.vtx[i].state == 1)
            for j in self.grp[i]:
                # 只有首次遍历到的深度才是最小深度
                if self.vtx[j].state == 0:
                    self.vtx[j].depth = self.vtx[i].depth + 1
                    que.push(j)
                    self.vtx[j].state = 1
            self.vtx[i].state = 2  # optional

    @check_param
    def dfs_iter(self, src):
        stk = []
        time = 1
        stk.append(src)
        while len(stk) > 0:
            i = stk[-1]
            if self.vtx[i].state == 0:
                self.vtx[i].time[0] = time
                time += 1
                self.vtx[i].state = 1
            elif self.vtx[i].state == 1:
                self.vtx[i].state = 2
                for j in self.grp[i]:
                    if self.vtx[j].state == 0:
                        stk.append(j)
                        self.vtx[i].state = 1
                        break
            else:
                assert (self.vtx[i].state == 2)
                self.vtx[i].time[1] = time
                time += 1
                stk.pop()

    @check_param
    def dfs_recur(self, src):
        def recur(i, t):
            assert (self.vtx[i].state == 0)
            self.vtx[i].time[0] = t
            t += 1
            self.vtx[i].state = 1
            for j in self.grp[i]:
                if self.vtx[j].state == 0:
                    t = recur(j, t)
            self.vtx[i].time[1] = t
            t += 1
            self.vtx[i].state = 2
            return t

        recur(src, 1)

    def testcase(self):
        pass


class DirectedGraphList(GraphList):
    def __init__(self):
        super(DirectedGraphList, self).__init__()

    def testcase(self):
        pass


class GraphMatrix(Graph):
    pass


class LakeCounting():
    def __init__(self):
        self.funcs = []
        self.funcs.append(self.main_dfs_recur)
        self.funcs.append(self.main_dfs_iter)
        self.funcs.append(self.main_bfs_iter)

    def main_dfs_recur(self, grp):
        def recur(i, j):
            if 0 <= i < len(grp) and 0 <= j < len(grp[0]) and grp[i][j] == 1:
                grp[i][j] = 0
                recur(i, j + 1)
                recur(i + 1, j + 1)
                recur(i + 1, j)
                recur(i + 1, j - 1)

        num = 0
        for i in range(len(grp)):
            for j in range(len(grp[0])):
                if grp[i][j] == 1:
                    num += 1
                    recur(i, j)

        return num

    def main_dfs_iter(self, grp):
        num = 0
        for i in range(len(grp)):
            for j in range(len(grp[0])):
                if grp[i][j] == 1:
                    num += 1
                    stk = [(i, j)]
                    while len(stk) > 0:
                        a, b = stk.pop()
                        if 0 <= a < len(grp) and 0 <= b < len(grp[0]) and grp[a][b] == 1:
                            grp[a][b] = 0
                            stk.append((a, b + 1))
                            stk.append((a + 1, b + 1))
                            stk.append((a + 1, b))
                            stk.append((a + 1, b - 1))
        return num

    def main_bfs_iter(self, grp):
        num = 0
        for i in range(len(grp)):
            for j in range(len(grp[0])):
                if grp[i][j] == 1:
                    num += 1
                    que = Queue()
                    que.push((i, j))
                    while len(que) > 0:
                        a, b = que.pop()
                        if 0 <= a < len(grp) and 0 <= b < len(grp[0]) and grp[a][b] == 1:
                            grp[a][b] = 0
                            que.push((a, b + 1))
                            que.push((a + 1, b + 1))
                            que.push((a + 1, b))
                            que.push((a + 1, b - 1))
        return num

    def testcase(self):
        case = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0],
                [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                ]

        for f in self.funcs:
            assert (f(copy.deepcopy(case)) == 3)
        print 'pass:', self.__class__


if __name__ == '__main__':
    # GraphList().testcase()
    UndirectedGraphList().testcase()
    DirectedGraphList().testcase()
    LakeCounting().testcase()
    print 'done'
