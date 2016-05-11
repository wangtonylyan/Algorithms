# -*- coding: utf-8 -*-

import copy
from collections import deque


class Graph(object):
    class Vertex():
        def __init__(self):
            self.status = 0
            self.depth = 0

        def clear(self):
            self.status = 0
            self.depth = 0

    def __init__(self, grp):
        self.grp = copy.deepcopy(grp)
        self.vtx = [self.__class__.Vertex() for i in range(len(self.grp))]

    def _clear(self):
        for v in self.vtx:
            v.clear()

    def testcase(self):
        ugrp = [[1, 4],
                [0, 5],
                [3, 5, 6],
                [2, 6, 7],
                [0],
                [1, 2, 6],
                [2, 3, 5, 7],
                [3, 6]]
        g = self.__class__(ugrp)
        assert (g.shortest_path(0, 7) == 4)
        print 'pass:', self.__class__


class GraphMatrix(Graph):
    def __init__(self, grp=[]):
        super(GraphMatrix, self).__init__(grp)


class GraphList(Graph):
    def __init__(self, grp=[]):
        super(GraphList, self).__init__(grp)

    def bfs(self, src):
        self._clear()
        que = deque()
        self.vtx[src].status = 1
        self.vtx[src].depth = 0
        que.append(src)
        while len(que) > 0:
            i = que.popleft()
            assert (self.vtx[i].status > 0)
            # status 2：用于表示是否已遍历过所有与其互通的顶点
            # 由于顶点之间存在多条通路，导致一个顶点可能在队列中出现多次
            # 因此利用该状态可以避免多次重复地检查同一个顶点
            if self.vtx[i].status == 1:
                self.vtx[i].status = 2
                for j in self.grp[i]:
                    # status 1：用于表示是否已得出了该顶点的深度
                    # 只有首次遍历到的深度才是最短路径
                    if self.vtx[j].status == 0:
                        self.vtx[j].status = 1
                        self.vtx[j].depth = self.vtx[i].depth + 1
                        que.append(j)

    def dfs(self, src):
        self._clear()
        stk = []
        self.vtx[src].status = 0
        stk.append(src)
        while len(stk) > 0:
            i = stk.pop()
            if self.vtx[i].status == 0:
                self.vtx[i].status = 1
                for j in self.grp[i]:
                    if self.vtx[j].status == 0:
                        stk.append(j)

    def _dfs_recur(self, src):
        pass

    def shortest_path(self, src, dst):
        assert (0 <= src < len(self.vtx) and 0 <= dst < len(self.vtx))
        self.bfs(src)
        return self.vtx[dst].depth


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
                    que = deque()
                    que.append((i, j))
                    while len(que) > 0:
                        a, b = que.popleft()
                        if 0 <= a < len(grp) and 0 <= b < len(grp[0]) and grp[a][b] == 1:
                            grp[a][b] = 0
                            que.append((a, b + 1))
                            que.append((a + 1, b + 1))
                            que.append((a + 1, b))
                            que.append((a + 1, b - 1))
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
    GraphList().testcase()
    LakeCounting().testcase()
    print 'done'
