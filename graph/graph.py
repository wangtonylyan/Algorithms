# -*- coding: utf-8 -*-
import copy


class Enum(tuple):
    __getattr__ = tuple.index


# LIST: adjacency list
# MATRIX: adjacency matrix
# DICT: http://code.activestate.com/recipes/119466/
GraphRepresentationType = Enum(['LIST', 'MATRIX', 'DICT'])

lib_undirected_acyclic_ugrp = [
    [  # line
        [1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6]
    ],
    [  # star
        [5], [5], [5], [5], [5], [0, 1, 2, 3, 4]
    ],
    [  # tree
        [1, 2, 3], [0], [0, 4, 5], [0, 6, 7], [2, 8, 9], [2, 10],
        [3, 12], [3], [4], [4], [5, 11], [10], [6]
    ],
]

lib_undirected_ugrp = lib_undirected_acyclic_ugrp + [
    [  # loop
        [1, 7], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6, 0]
    ],
    [  # pentagram
        [1, 2, 3, 4], [0, 4, 3, 2], [1, 0, 4, 3], [1, 2, 0, 4], [0, 1, 2, 3]
    ],
    [
        [1, 4], [0, 5], [3, 5, 6], [2, 6, 7], [0], [1, 2, 6], [2, 3, 5, 7], [3, 6]
    ],
    [
        [1, 2], [0, 2, 3], [0, 1, 4, 5], [1, 4, 6], [3, 6, 5, 2], [2, 4, 6], [3, 4, 5]
    ],
    [
        [1], [0, 3, 2], [1, 3, 4], [1, 2], [2, 6], [6], [4, 5]
    ],
    [
        [1, 2, 3], [0, 2, 5, 7], [1, 0, 3, 5, 4], [0, 2, 4, 8], [2, 3, 5, 6],
        [1, 2, 4, 6, 7], [5, 4, 7, 8], [1, 5, 6, 8], [3, 6, 7]
    ],
]

lib_undirected_acyclic_wgrp = [
]
lib_undirected_wgrp = lib_undirected_acyclic_wgrp + [
    [
        [(1, 4), (7, 8)],
        [(0, 4), (2, 8), (7, 11)],
        [(1, 8), (8, 2), (3, 7), (5, 4)],
        [(2, 7), (4, 9), (5, 14)],
        [(3, 9), (5, 10)],
        [(2, 4), (3, 14), (4, 10), (6, 2)],
        [(5, 2), (7, 1), (8, 6)],
        [(0, 8), (1, 11), (8, 7), (6, 1)],
        [(2, 2), (6, 6), (7, 7)]
    ],
    [
        [(1, 7), (3, 4)],
        [(0, 7), (2, 11), (3, 9), (4, 10)],
        [(1, 11), (4, 5)],
        [(0, 4), (1, 9), (4, 15), (5, 6)],
        [(1, 10), (2, 5), (3, 15), (5, 12), (6, 8)],
        [(3, 6), (4, 12), (6, 13)],
        [(4, 8), (5, 13)]
    ],
    [
        [(1, 15), (2, 53)],
        [(0, 15), (2, 40), (3, 46)],
        [(0, 53), (1, 40), (4, 31), (5, 17)],
        [(1, 46), (4, 3), (6, 11)],
        [(3, 3), (6, 8), (5, 29), (2, 31)],
        [(2, 17), (4, 29), (6, 40)],
        [(3, 11), (4, 8), (5, 40)]
    ],
    [
        [(1, 22), (2, 9), (3, 12)],
        [(0, 22), (2, 35), (5, 36), (7, 34)],
        [(1, 35), (0, 9), (3, 4), (5, 42), (4, 65)],
        [(0, 12), (2, 4), (4, 33), (8, 30)],
        [(2, 65), (3, 33), (5, 18), (6, 23)],
        [(1, 36), (2, 42), (4, 18), (6, 39), (7, 24)],
        [(5, 39), (4, 23), (7, 25), (8, 21)],
        [(1, 34), (5, 24), (6, 25), (8, 19)],
        [(3, 30), (6, 21), (7, 19)]
    ],
    [
        [(1, 1), (7, 8)], [(0, 1), (2, 2)], [(1, 2), (3, 3)],
        [(2, 3), (4, 4)], [(3, 4), (5, 5)], [(4, 5), (6, 6)],
        [(5, 6), (7, 7)], [(6, 7), (0, 8)]
    ],
    [
        [(1, 90), (2, 67), (3, 30), (4, 7)],
        [(0, 90), (4, 81), (3, 10), (2, 19)],
        [(1, 19), (0, 67), (4, 74), (3, 50)],
        [(1, 10), (2, 50), (0, 30), (4, 24)],
        [(0, 7), (1, 81), (2, 74), (3, 24)]
    ],
]
lib_directed_acyclic_ugrp = [
    [
        [], [0], [1], [2], [3], [4]
    ],
    [
        [1], [2], [3], [4], [5], []
    ],
    [
        [1, 2], [3, 4], [5, 6], [], [], [], [], []
    ],
    [
        [1, 7], [2, 7], [8, 3, 5], [4, 5], [5], [6], [7, 8], [], [7]
    ],
    [
        [5], [5, 6], [7], [6], [8], [9], [7, 10, 8], [9], [], [], []
    ],
    [
        [5], [7], [7, 0], [0, 6], [], [], [], [4, 5, 6]
    ]
]
lib_directed_ugrp = lib_directed_acyclic_ugrp + [
]
lib_directed_acyclic_wgrp = [
    [
        [], [(0, 1)], [(1, 1)], [(2, 1)], [(3, 1)], [(4, 1)]
    ],
    [
        [(1, 1)], [(2, 1)], [(3, 1)], [(4, 1)], [(5, 1)], []
    ],
    [
        [(1, 1), (2, 1)], [(3, 1), (4, 1)], [(5, 1), (6, 1)], [], [], [], [], []
    ],
    [
        [(1, 4), (7, 8)],
        [(2, 8), (7, 11)],
        [(8, 2), (3, 7), (5, 4)],
        [(4, 9), (5, 14)],
        [(5, 10)],
        [(6, 2)],
        [(7, 1), (8, 6)],
        [],
        []
    ],
]
lib_directed_wgrp = lib_directed_acyclic_wgrp + [
]


def dec_check_cases(func):
    def f(self, *args):
        assert (isinstance(self, AbstractGraph))
        assert (0 <= self.rpst < len(GraphRepresentationType))
        assert (isinstance(self.wgt, bool))
        assert (isinstance(self.drct, bool))
        assert (isinstance(self.grps, list))

        cases = func(self, *args)
        assert (isinstance(cases, list))

        for case in cases:
            if self.rpst == GraphRepresentationType.LIST:
                assert (isinstance(case, list))
                if self.drct:  # directed
                    if self.wgt:  # weighted
                        for i in range(len(case)):
                            for j, w in case[i]:
                                assert (0 <= j < len(case) and w > 0)
                    else:  # unweighted
                        for i in range(len(case)):
                            for j in case[i]:
                                assert (0 <= j < len(case))
                else:  # undirected
                    if self.wgt:  # weighted
                        num = 0
                        for i in range(len(case)):
                            for j, w in case[i]:
                                for k, v in case[j]:
                                    if k == i:
                                        assert (w == v > 0)
                                        num += 1
                                        break
                        assert (num == sum(map(len, case)))
                    else:  # unweighted
                        num = 0
                        for i in range(len(case)):
                            for j in case[i]:
                                for k in case[j]:
                                    if k == i:
                                        num += 1
                                        break
                        assert (num == sum(map(len, case)))
            elif self.rpst == GraphRepresentationType.MATRIX:
                assert (isinstance(case, list))
                if self.drct:  # directed
                    if self.wgt:  # weighted
                        for i in range(len(case)):
                            for j in range(len(case)):
                                assert (case[i][j] >= 0)  # connection or weight
                    else:  # unweighted
                        for i in range(len(case)):
                            for j in range(len(case)):
                                assert (0 <= case[i][j] <= 1)  # connection
                else:  # undirected
                    if self.wgt:  # weighted
                        for i in range(len(case)):
                            for j in range(len(case)):
                                assert (case[i][j] == case[j][i] >= 0)
                    else:  # unweighted
                        for i in range(len(case)):
                            for j in range(len(case)):
                                assert (0 <= case[i][j] == case[j][i] <= 1)
            elif self.rpst == GraphRepresentationType.DICT:
                assert (isinstance(case, dict))
                if self.drct:  # directed
                    if self.wgt:  # weighted
                        for i in case.keys():
                            for j, w in case[i].items():
                                assert (w > 0)
                    else:  # unweighted
                        for i in case.keys():
                            for j, w in case[i].items():
                                assert (w == 1)
                else:  # undirected
                    if self.wgt:  # weighted
                        for i in case.keys():
                            for j in case[i].keys():
                                assert (case[i][j] == case[j][i] > 0)
                    else:  # unweighted
                        for i in case.keys():
                            for j in case[i].keys():
                                assert (case[i][j] == case[j][i] == 1)
            else:
                assert (False)

        return cases

    return f


# interface
class AbstractGraph(object):
    def testcase(self):
        assert (False)

    def _testcase(self, test, cases):
        assert (False)

    def _gencase(self):
        assert (False)


class Graph(AbstractGraph):
    def __init__(self, rpst, wgt, drct):
        assert (0 <= rpst < len(GraphRepresentationType))
        assert (isinstance(wgt, bool))
        assert (isinstance(drct, bool))
        super(Graph, self).__init__()
        self.rpst = rpst  # representation/structure
        self.wgt = wgt  # weight
        self.drct = drct  # direction
        self.grps = None

    def _testcase(self, test, cases):
        map(test, cases)
        print 'pass:', self.__class__, '-', len(cases)

    @dec_check_cases
    def _gencase(self):
        assert (isinstance(self.grps, list) and all(map(lambda x: isinstance(x, list), self.grps)))
        return map(lambda x: self._transform(GraphRepresentationType.LIST, self.rpst, x, self.wgt), self.grps)

    @staticmethod
    def _transform(fm, to, grp, wgt):
        assert (0 <= fm < len(GraphRepresentationType))
        assert (0 <= to < len(GraphRepresentationType))
        assert (grp != None and isinstance(wgt, bool))
        ret = None
        if fm == to:
            ret = copy.deepcopy(grp)  # return a new instance of grp
        elif fm == GraphRepresentationType.LIST:
            assert (isinstance(grp, list) and all(map(lambda x: isinstance(x, list), grp)))
            if to == GraphRepresentationType.MATRIX:
                ret = [[0] * len(grp) for i in range(len(grp))]
                if wgt:
                    for i in range(len(grp)):
                        for j, w in grp[i]:
                            ret[i][j] = w
                else:
                    for i in range(len(grp)):
                        for j in grp[i]:
                            ret[i][j] = 1
            elif to == GraphRepresentationType.DICT:
                ret = {}
                if wgt:
                    for i in range(len(grp)):
                        for j, w in grp[i]:
                            if not ret.has_key(i):
                                ret[i] = {}
                            ret[i][j] = w
                else:
                    for i in range(len(grp)):
                        for j in grp[i]:
                            if not ret.has_key(i):
                                ret[i] = {}
                            ret[i][j] = 1
        elif fm == GraphRepresentationType.MATRIX:
            assert (isinstance(grp, list) and all(map(lambda x: isinstance(x, list), grp)))
            if to == GraphRepresentationType.LIST:
                pass
            elif to == GraphRepresentationType.DICT:
                pass
        elif fm == GraphRepresentationType.DICT:
            assert (isinstance(grp, dict) and all(map(lambda x: isinstance(x, dict), grp)))
            if to == GraphRepresentationType.LIST:
                pass
            elif to == GraphRepresentationType.MATRIX:
                pass

        assert (ret != None)
        if isinstance(ret, list):
            assert (all(map(lambda x: isinstance(x, list), ret)))
        elif isinstance(ret, dict):
            assert (all(map(lambda x: isinstance(x, dict), ret.values())))
        else:
            assert (False)
        return ret

    @staticmethod
    def _transpose(rpst, grp, wgt):
        assert (grp != None)
        assert (0 <= rpst < len(GraphRepresentationType))
        assert (isinstance(wgt, bool))
        if rpst == GraphRepresentationType.LIST:
            ret = [[] for i in range(len(grp))]
            if wgt:
                for i in range(grp):
                    for j, w in grp[i]:
                        ret[j].append((i, w))
            else:
                for i in range(grp):
                    for j in grp[i]:
                        ret[j].append(i)
        elif rpst == GraphRepresentationType.MATRIX:
            ret = [[0] * len(grp) for i in range(len(grp))]
            for i in range(len(grp)):
                for j in range(len(grp)):
                    if grp[i][j] > 0:
                        ret[j][i] = grp[i][j]
        elif rpst == GraphRepresentationType.DICT:
            ret = {}
            for i in grp.keys():
                for j in grp[i].keys():
                    if not ret.has_key(j):
                        ret[j] = {}
                    ret[j][i] = grp[i][j]
        assert (len(ret) == len(grp))
        return ret


class UndirectedGraph(Graph):
    def __init__(self, wgt, rpst=GraphRepresentationType.LIST):
        assert (isinstance(wgt, bool))
        assert (0 <= rpst < len(GraphRepresentationType))
        super(UndirectedGraph, self).__init__(rpst, wgt, False)
        if self.wgt:
            self.grps = lib_undirected_wgrp
        else:
            self.grps = lib_undirected_ugrp


class UndirectedAcyclicGraph(UndirectedGraph):
    def __init__(self, wgt, rpst=GraphRepresentationType.LIST):
        assert (isinstance(wgt, bool))
        assert (0 <= rpst < len(GraphRepresentationType))
        super(UndirectedAcyclicGraph, self).__init__(wgt, rpst)
        if self.wgt:
            self.grps = lib_undirected_acyclic_wgrp
        else:
            self.grps = lib_undirected_acyclic_ugrp


class DirectedGraph(Graph):
    def __init__(self, wgt, rpst=GraphRepresentationType.LIST):
        assert (isinstance(wgt, bool))
        assert (0 <= rpst < len(GraphRepresentationType))
        super(DirectedGraph, self).__init__(rpst, wgt, True)
        if self.wgt:
            self.grps = lib_directed_wgrp
        else:
            self.grps = lib_directed_ugrp


class DirectedAcyclicGraph(DirectedGraph):
    def __init__(self, wgt, rpst=GraphRepresentationType.LIST):
        assert (isinstance(wgt, bool))
        assert (0 <= rpst < len(GraphRepresentationType))
        super(DirectedAcyclicGraph, self).__init__(wgt, rpst)
        if self.wgt:
            self.grps = lib_directed_acyclic_wgrp
        else:
            self.grps = lib_directed_acyclic_ugrp


if __name__ == '__main__':
    def main(cls):
        assert (len(cls(False, GraphRepresentationType.LIST)._gencase()) ==
                len(cls(False, GraphRepresentationType.MATRIX)._gencase()) ==
                len(cls(False, GraphRepresentationType.DICT)._gencase()))
        assert (len(cls(True, GraphRepresentationType.LIST)._gencase()) ==
                len(cls(True, GraphRepresentationType.MATRIX)._gencase()) ==
                len(cls(True, GraphRepresentationType.DICT)._gencase()))


    map(main, [UndirectedGraph, UndirectedAcyclicGraph, DirectedGraph, DirectedAcyclicGraph])
    print 'done'
