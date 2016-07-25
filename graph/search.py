# -*- coding: utf-8 -*-
# @problem: graph traversal


import copy
from graph import AbstractGraph, UndirectedGraph, DirectedGraph
from data_structure.queue import Queue
from data_structure.stack import Stack


def dec_search_source_wrapper(func):
    def f(self, grp, src, *args):
        assert (isinstance(grp, list) and reduce(lambda x, y: x and isinstance(y, list), grp, True))
        assert (0 <= src < len(grp))
        vtx = func(self, grp, src, *args)
        assert (isinstance(vtx, list) and len(vtx) == len(grp))
        if 2 in vtx:
            assert (vtx.count(2) * 2 == sum(vtx))
            return filter(lambda x: vtx[x] == 2, range(len(vtx)))
        elif 1 in vtx:
            assert (vtx.count(1) == sum(vtx))
            return filter(lambda x: vtx[x] == 1, range(len(vtx)))
        return None

    return f


class GraphSearch_List(AbstractGraph):
    def __init__(self):
        AbstractGraph.__init__(self)
        self.funcs = [
            self.bfs_iter,
            self.bfs_iter_2,
            self.dfs_iter,
            self.dfs_iter_2,
            self.dfs_recur,
        ]

    @dec_search_source_wrapper
    def bfs_iter(self, grp, src):
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
        return vtx

    @dec_search_source_wrapper
    def bfs_iter_2(self, grp, src):
        vtx = [0] * len(grp)
        que = [src]
        while len(que) > 0:
            i = que[0]
            if vtx[i] == 0:
                vtx[i] = 1
            elif vtx[i] == 1:
                for j in grp[i]:
                    if vtx[j] == 0:
                        que.append(j)
                vtx[i] = 2
            else:
                assert (vtx[i] == 2)
                que = que[1:]
        return vtx

    @dec_search_source_wrapper
    def dfs_iter(self, grp, src):
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
        return vtx

    @dec_search_source_wrapper
    def dfs_iter_2(self, grp, src):
        vtx = [0] * len(grp)
        stk = [src]
        while len(stk) > 0:
            i = stk[-1]
            if vtx[i] == 0:
                vtx[i] = 1
            elif vtx[i] == 1:
                vtx[i] = 2
                for j in grp[i]:
                    if vtx[j] == 0:
                        stk.append(j)
                        vtx[i] = 1
                        break
            else:
                assert (vtx[i] == 2)
                stk.pop()
        return vtx

    @dec_search_source_wrapper
    def dfs_recur(self, grp, src):
        def recur(src):
            assert (vtx[src] == 0)
            vtx[src] = 1
            for i in grp[src]:
                if vtx[i] == 0:
                    recur(i)

        vtx = [0] * len(grp)
        recur(src)
        return vtx

    def _traverse(self, grp, fs):
        assert (callable(fs))
        vtx = [False] * len(grp)  # if visited
        num = 0
        while False in vtx:
            ret = fs(grp, vtx.index(False))
            assert (len(ret) <= len(vtx))
            for i in ret:
                if not vtx[i]:
                    vtx[i] = True
            num += 1
        assert (all(vtx))
        return num

    def testcase(self):
        def test(case):
            assert (len(self.funcs) > 0)
            for i in range(len(case)):
                assert (reduce(lambda x, y: x if x == y(copy.deepcopy(case), i) else None,
                               self.funcs[1:], self.funcs[0](copy.deepcopy(case), i)) != None)
            assert (reduce(lambda x, y: x if x == self._traverse(copy.deepcopy(case), y) else None,
                           self.funcs[1:], self._traverse(copy.deepcopy(case), self.funcs[0])) != None)

        self._testcase(test, self._gencase())


class UndirectedGraphSearch_List(GraphSearch_List, UndirectedGraph):
    def __init__(self):
        GraphSearch_List.__init__(self)
        UndirectedGraph.__init__(self, False)


class DirectedGraphSearch_List(GraphSearch_List, DirectedGraph):
    def __init__(self):
        GraphSearch_List.__init__(self)
        DirectedGraph.__init__(self, False)


# @problem: 获取所有节点距离某个源点的深度/层次
# @problem: bipartite graph，实现：对不同层次的节点进行染色
class VertexDepth(UndirectedGraph):
    def __init__(self):
        super(VertexDepth, self).__init__(False)

    def main_bfs(self, grp, src):
        vtx = [0] * len(grp)
        dpt = [None] * len(grp)
        que = Queue()
        vtx[src] = 1
        dpt[src] = 0
        que.push(src)
        while len(que) > 0:
            i = que.pop()
            assert (vtx[i] == 1)
            for j in grp[i]:
                # 只有首次遍历到的深度才是最小深度
                if vtx[j] == 0:
                    vtx[j] = 1
                    dpt[j] = dpt[i] + 1
                    que.push(j)
        return dpt

    def testcase(self):
        def test(case):
            for i in range(len(case)):
                self.main_bfs(case, i)

        self._testcase(test, self._gencase())


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
    UndirectedGraphSearch_List().testcase()
    DirectedGraphSearch_List().testcase()
    VertexDepth().testcase()
    LakeCounting().testcase()
    print 'done'
