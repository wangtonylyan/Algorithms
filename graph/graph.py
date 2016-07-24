# -*- coding: utf-8 -*-

class Enum(tuple):
    __getattr__ = tuple.index


# adjacency list and adjacency matrix representation
GraphRepresentationType = Enum(['LIST', 'MATRIX'])

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


def dec_check_cases(drct):
    assert (isinstance(drct, bool))

    def f1(func):
        def f2(self, wgt, rpst, *args):
            assert (isinstance(self, Graph))
            assert (isinstance(wgt, bool))
            assert (isinstance(rpst, int))

            cases = func(self, wgt, rpst, *args)
            assert (isinstance(cases, list))

            for case in cases:
                assert (isinstance(case, list))
                if rpst == GraphRepresentationType.LIST:
                    if drct:  # directed
                        if wgt:  # weighted
                            for i in range(len(case)):
                                for j, w in case[i]:
                                    assert (0 <= j < len(case) and w > 0)
                        else:  # unweighted
                            for i in range(len(case)):
                                for j in case[i]:
                                    assert (0 <= j < len(case))
                    else:  # undirected
                        if wgt:  # weighted
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
                elif rpst == GraphRepresentationType.MATRIX:
                    if drct:  # directed
                        if wgt:  # weighted
                            for i in range(len(case)):
                                for j in range(len(case)):
                                    assert (case[i][j] >= 0)  # connection or weight
                        else:  # unweighted
                            for i in range(len(case)):
                                for j in range(len(case)):
                                    assert (0 <= case[i][j] <= 1)  # connection
                    else:  # undirected
                        if wgt:  # weighted
                            for i in range(len(case)):
                                for j in range(len(case)):
                                    assert (case[i][j] == case[j][i] >= 0)
                        else:  # unweighted
                            for i in range(len(case)):
                                for j in range(len(case)):
                                    assert (0 <= case[i][j] == case[j][i] <= 1)
                else:
                    assert (False)

            return cases

        return f2

    return f1


class Graph(object):
    def __init__(self):
        self.ugrps = None  # unweighted graph
        self.wgrps = None  # weighted graph

    def testcase(self):
        assert (False)

    def _testcase(self, test, cases):
        map(test, cases)
        print 'pass:', self.__class__, '-', len(cases)

    def gencase(self, wgt, rpst=GraphRepresentationType.LIST):
        return self._gencase(wgt, rpst)

    def _gencase(self, wgt, rpst):
        if rpst == GraphRepresentationType.LIST:
            if wgt:
                return self.wgrps
            else:
                return self.ugrps
        elif rpst == GraphRepresentationType.MATRIX:
            if wgt:
                return self._transform(self.wgrps, True)
            else:
                return self._transform(self.ugrps, False)
        assert (False)

    # from GraphRepresentationType.LIST to GraphRepresentationType.MATRIX
    @staticmethod
    def _transform(grps, wgt):
        ret = []
        if wgt:
            for g in grps:
                m = [[0] * len(g) for i in range(len(g))]
                for i in range(len(g)):
                    for j, w in g[i]:
                        m[i][j] = w
                ret.append(m)
        else:
            for g in grps:
                m = [[0] * len(g) for i in range(len(g))]
                for i in range(len(g)):
                    for j in g[i]:
                        m[i][j] = 1
                ret.append(m)
        assert (len(ret) == len(grps))
        return ret


class UndirectedGraph(Graph):
    def __init__(self):
        super(UndirectedGraph, self).__init__()
        self.ugrps = lib_undirected_ugrp
        self.wgrps = lib_undirected_wgrp

    @dec_check_cases(False)
    def _gencase(self, *args):
        return super(UndirectedGraph, self)._gencase(*args)


class UndirectedAcyclicGraph(UndirectedGraph):
    def __init__(self):
        super(UndirectedAcyclicGraph, self).__init__()
        self.ugrps = lib_undirected_acyclic_ugrp
        self.wgrps = lib_undirected_acyclic_wgrp


class DirectedGraph(Graph):
    def __init__(self):
        super(DirectedGraph, self).__init__()
        self.ugrps = lib_directed_ugrp
        self.wgrps = lib_directed_wgrp

    @dec_check_cases(True)
    def _gencase(self, *args):
        return super(DirectedGraph, self)._gencase(*args)


class DirectedAcyclicGraph(DirectedGraph):
    def __init__(self):
        super(DirectedAcyclicGraph, self).__init__()
        self.ugrps = lib_directed_acyclic_ugrp
        self.wgrps = lib_directed_acyclic_wgrp


if __name__ == '__main__':
    grp = UndirectedGraph()
    assert (len(grp.gencase(False, GraphRepresentationType.LIST)) ==
            len(grp.gencase(False, GraphRepresentationType.MATRIX)))
    assert (len(grp.gencase(True, GraphRepresentationType.LIST)) ==
            len(grp.gencase(True, GraphRepresentationType.MATRIX)))
    grp = DirectedGraph()
    assert (len(grp.gencase(False, GraphRepresentationType.LIST)) ==
            len(grp.gencase(False, GraphRepresentationType.MATRIX)))
    assert (len(grp.gencase(True, GraphRepresentationType.LIST)) ==
            len(grp.gencase(True, GraphRepresentationType.MATRIX)))
    print 'done'
