# -*- coding: utf-8 -*-

def dec_check_unweighted(undrct=False):
    def f1(func):
        def f2(*args):
            cases = func(*args)
            assert (isinstance(cases, list))
            for case in cases:
                assert (isinstance(case, list))
                if undrct:
                    num = 0
                    for i in range(len(case)):
                        for j in case[i]:
                            for k in case[j]:
                                if k == i:
                                    num += 1
                                    break
                    assert (num == sum(map(len, case)))
                else:
                    pass
            return cases

        return f2

    return f1


def dec_check_weighted(undrct=False):
    def f1(func):
        def f2(*args):
            cases = func(*args)
            assert (isinstance(cases, list))
            for case in cases:
                assert (isinstance(case, list))
                if undrct:
                    num = 0
                    for i in range(len(case)):
                        for j, w in case[i]:
                            for k, v in case[j]:
                                if k == i:
                                    assert (w == v >= 0)
                                    num += 1
                                    break
                    assert (num == sum(map(len, case)))
                else:
                    for i in range(len(case)):
                        for j, w in case[i]:
                            assert (w >= 0)
            return cases

        return f2

    return f1


class Graph(object):
    def __init__(self):
        pass

    def testcase(self):
        assert (False)

    def _testcase(self, test, cases):
        map(test, cases)
        print 'pass:', self.__class__, '-', len(cases)

    def gencase_unweighted(self):
        assert (False)

    def gencase_weighted(self):
        assert (False)


undirected_acyclic_ugrp = [
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

undirected_ugrp = undirected_acyclic_ugrp + [
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

undirected_acyclic_wgrp = [
]

undirected_wgrp = undirected_acyclic_wgrp + [
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


class UndirectedGraph(Graph):
    def __init__(self):
        super(UndirectedGraph, self).__init__()

    @dec_check_unweighted(True)
    def gencase_unweighted(self):
        return undirected_ugrp

    @dec_check_weighted(True)
    def gencase_weighted(self):
        return undirected_wgrp


class UndirectedAcyclicGraph(UndirectedGraph):
    def __init__(self):
        super(UndirectedAcyclicGraph, self).__init__()

    @dec_check_unweighted(True)
    def gencase_unweighted(self):
        return undirected_acyclic_ugrp

    @dec_check_weighted(True)
    def gencase_weighted(self):
        return undirected_acyclic_wgrp


directed_acyclic_ugrp = [
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

directed_ugrp = directed_acyclic_ugrp + [
]

directed_acyclic_wgrp = [
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
directed_wgrp = directed_acyclic_wgrp + [
]


class DirectedGraph(Graph):
    def __init__(self):
        super(DirectedGraph, self).__init__()

    @dec_check_unweighted(False)
    def gencase_unweighted(self):
        return directed_ugrp

    @dec_check_weighted(False)
    def gencase_weighted(self):
        return directed_wgrp


class DirectedAcyclicGraph(DirectedGraph):
    def __init__(self):
        super(DirectedAcyclicGraph, self).__init__()

    @dec_check_unweighted(False)
    def gencase_unweighted(self):
        return directed_acyclic_ugrp

    @dec_check_weighted(False)
    def gencase_weighted(self):
        return directed_acyclic_wgrp


if __name__ == '__main__':
    print len(UndirectedGraph().gencase_unweighted())
    print len(UndirectedGraph().gencase_weighted())
    print len(DirectedGraph().gencase_unweighted())
    print len(DirectedGraph().gencase_weighted())
    print 'done'
