# -*- coding: utf-8 -*-

import copy
from collections import deque


def graph_traverse_check(func):
    def f(self, src):
        assert (self.vtx and isinstance(self.vtx, list) and len(self.vtx) > 0)
        assert (self.grp and isinstance(self.grp, list) and len(self.grp) > 0)
        assert (len(self.vtx) == len(self.grp))
        assert (0 <= src < len(self.vtx))
        self._clear()
        for v in self.vtx:
            assert (v.status == 0)
        ret = func(self, src)
        for v in self.vtx:
            assert (v.status == 0 or v.status == 2)
        return ret

    return f


class Graph(object):
    class Vertex():
        def __init__(self):
            self.status = 0
            self.depth = 0
            self.time = [0, 0]

        def clear(self):
            self.status = 0
            self.depth = 0
            self.time = [0, 0]

    def __init__(self, grp):
        self.grp = copy.deepcopy(grp)
        self.vtx = [self.__class__.Vertex() for i in range(len(self.grp))]
        assert (len(self.grp) == len(self.vtx))

    def _clear(self):
        for v in self.vtx:
            v.clear()

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

        # shortest path
        for i in range(len(g.vtx)):
            g.bfs(i)
            gb = copy.deepcopy(g.vtx)
            for j in range(len(g.vtx)):
                if j != i:
                    g.bfs(j)
                    assert (gb[j].depth == g.vtx[i].depth)

        for i in range(len(g.vtx)):
            g.bfs(i)
            g.dfs(i)
            gd1 = map(lambda x: copy.deepcopy(x.time), g.vtx)
            g.dfs_recur(i)
            gd2 = map(lambda x: copy.deepcopy(x.time), g.vtx)
            assert (gd1 == gd2)

        print 'pass:', self.__class__


class GraphMatrix(Graph):
    def __init__(self, grp=[]):
        super(GraphMatrix, self).__init__(grp)


class GraphList(Graph):
    def __init__(self, grp=[]):
        super(GraphList, self).__init__(grp)

    @graph_traverse_check
    def bfs(self, src):
        que = deque()
        self.vtx[src].status = 1
        self.vtx[src].depth = 0
        que.append(src)
        while len(que) > 0:
            i = que.popleft()
            assert (self.vtx[i].status == 1)
            if self.vtx[i].status == 1:
                for j in self.grp[i]:
                    # 只有首次遍历到的深度才是最短路径
                    if self.vtx[j].status == 0:
                        self.vtx[j].depth = self.vtx[i].depth + 1
                        que.append(j)
                        self.vtx[j].status = 1
                self.vtx[i].status = 2  # optional

    @graph_traverse_check
    def dfs(self, src):
        stk = []
        time = 1
        stk.append(src)
        while len(stk) > 0:
            i = stk[-1]
            if self.vtx[i].status == 0:
                self.vtx[i].time[0] = time
                time += 1
                self.vtx[i].status = 1
            elif self.vtx[i].status == 1:
                self.vtx[i].status = 2
                for j in self.grp[i]:
                    if self.vtx[j].status == 0:
                        stk.append(j)
                        self.vtx[i].status = 1
                        break
            else:
                assert (self.vtx[i].status == 2)
                self.vtx[i].time[1] = time
                time += 1
                stk.pop()

    @graph_traverse_check
    def dfs_recur(self, src):
        def recur(i, t):
            assert (self.vtx[i].status == 0)
            self.vtx[i].time[0] = t
            t += 1
            self.vtx[i].status = 1
            for j in self.grp[i]:
                if self.vtx[j].status == 0:
                    t = recur(j, t)
            self.vtx[i].time[1] = t
            t += 1
            self.vtx[i].status = 2
            return t

        recur(src, 1)


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
