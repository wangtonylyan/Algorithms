# -*- coding: utf-8 -*-
import random
import time


def testsortint():
    # Python中list的随机访问是非常耗时的，从list.sort()的速度之快就可以看出
    # 内部实现(C语言中)的list遍历与外部遍历的性能差异
    # 换言之，1)要尽可能利用内置的函数，而不是重新造轮子
    # 2)list的随机访问与算术计算相比，要尽可能地偏向于后者
    # bubble: 2879
    # insert: 1385
    # select: 1054
    # heap: 35(sink alone), 30(sink based on float)
    # merge: 30(iter), 31(recur)
    # quick: 18.5(iter), 18.2(recur)
    # radix: 10.5
    # count: 2.3
    # list.sort(): 1.5
    def func(lst):
        lst.sort()
        return lst

    times = 500
    strlen = 5000
    total = 0
    lst = [i for i in range(1, strlen + 1)]
    for i in range(times):
        cpy = lst[:]
        random.shuffle(cpy)
        start = time.time() * 1000
        ret = func(cpy)
        end = time.time() * 1000
        total += end - start
        if lst != ret:
            print ret
        assert (lst == ret)

    print 'pass:', func, '-- cost:', total / times


def testsortstr():
    # LSD: 13
    # MSD: 1.4
    # list.sort(): 0.04
    def func(lst):
        lst.sort()
        return lst

    times = 500
    length = 100
    num = 200
    total = 0
    for i in range(times):
        case = []
        for j in range(num):
            s = ''
            width = random.randint(1, length)
            for k in range(width):
                s += chr(random.randint(ord('a'), ord('z')))
            case.append(s)
        cpy = case[:]
        start = time.time()
        ret = func(cpy)
        end = time.time()
        total += (end - start) * 1000
        case.sort()
        if ret != case:
            print ret
        assert (ret == case)
    print 'pass:', func, '-- cost:', total / times


def testdynamic():
    def func1(wgt, its):
        tab = [[0] * (len(its) + 1) for i in range(wgt + 1)]
        for i in range(1, wgt + 1):
            for j in range(1, len(its) + 1):
                tab[i][j] = max(tab[i - its[j - 1][0]][j] + its[j - 1][1] if i >= its[j - 1][0] else 0,
                                tab[i][j - 1])
        return tab[-1][-1]

    def func2(wgt, its):
        tab = [0] * (wgt + 1)
        for i in range(len(its)):
            for j in range(1, wgt + 1):
                tab[j] = max(tab[j - its[i][0]] + its[i][1] if j >= its[i][0] else 0,
                             tab[j])
        return tab[-1]

    weight = 100
    items = [(1, 1), (2, 5), (3, 8), (4, 9), (5, 10), (6, 17), (7, 17), (8, 20), (9, 24), (10, 30)]

    def test(func, wgt, its):
        times = 10
        total = 0
        for i in range(times):
            cpy = its[:]
            start = time.time()
            ret = func(wgt, cpy)
            end = time.time()
            total += (end - start) * 1000
        return ret, total / times

    total1, total2 = 0, 0
    for wgt in range(weight):
        r1, t1 = test(func1, wgt, items)
        r2, t2 = test(func2, wgt, items)
        assert (r1 == r2)
        total1 += t1
        total2 += t2
    print 'pass:', func1, '-- cost:', total1
    print 'pass:', func2, '-- cost:', total2


def testunionfindset():
    def func(lst):
        pass

    case = [4, 8, -1, 3, -1, 9, 2, 6, -1, -1, -1, 1, 7, -1, 5, -1, -1]
    ret = [4, 3, 2, 6, 8, 1, 5, 7]
    assert (case.count(-1) == len(ret))
    t = func(case)
    if t != ret:
        print t
    assert (ret == t)


def testgraph():
    def mst(grp):
        pass

    def shortest(grp, src):
        pass

    ugrp = [
        [(1, 4), (7, 8)],
        [(0, 4), (2, 8), (7, 11)],
        [(1, 8), (8, 2), (3, 7), (5, 4)],
        [(2, 7), (4, 9), (5, 14)],
        [(3, 9), (5, 10)],
        [(2, 4), (3, 14), (4, 10), (6, 2)],
        [(5, 2), (7, 1), (8, 6)],
        [(0, 8), (1, 11), (8, 7), (6, 1)],
        [(2, 2), (6, 6), (7, 7)]
    ]

    dag = [
        [(1, 4), (7, 8)],
        [(2, 8), (7, 11)],
        [(8, 2), (3, 7), (5, 4)],
        [(4, 9), (5, 14)],
        [(5, 10)],
        [(6, 2)],
        [(7, 1), (8, 6)],
        [],
        []
    ]

    assert (mst(ugrp) == 37)
    assert (shortest(dag, 0) == 119)


if __name__ == '__main__':
    # testsortint()
    # testsortstr()
    # testdynamic()
    # testunionfindset()
    # testgraph()
    print 'done'
