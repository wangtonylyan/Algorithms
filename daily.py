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
                tab[i][j] = max(tab[i - its[j - 1][0]][j - 1] + its[j - 1][1] if i >= its[j - 1][0] else 0,
                                tab[i][j - 1])

        return tab[-1][-1]

    def func2(wgt, its):
        tab = [0] * (wgt + 1)
        for i in range(len(its)):
            for j in range(wgt, 0, -1):
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
        def main_Kruskal(grp):
            edge = []
            for i in range(len(grp)):
                for j, w in grp[i]:
                    m, n = min(i, j), max(i, j)
                    if ((m, n), w) not in edge:
                        edge.append(((m, n), w))
            assert (len(edge) == sum(map(len, grp)) / 2)

            cnt = [0] * (max(map(lambda x: x[1], edge)) + 1)
            for (i, j), w in edge:
                cnt[w] += 1
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            cpy = edge[:]
            for (i, j), w in cpy:
                edge[cnt[w - 1]] = ((i, j), w)
                cnt[w - 1] += 1

            def find(ds, n):
                while ds[n] != n:
                    n = ds[n]
                return n

            def union(ds, n1, n2):
                p1 = find(ds, n1)
                p2 = find(ds, n2)
                if p1 != p2:
                    ds[p2] = p1
                return p1

            ds = [i for i in range(len(grp))]
            ret = []
            for (i, j), w in edge:
                if find(ds, i) != find(ds, j):
                    union(ds, i, j)
                    ret.append(w)
            print ret
            return sum(ret)

        def main_Prim(grp, src):
            vtx = [0] * len(grp)
            dis = [None] * len(grp)
            vtx[src] = 1
            dis[src] = 0
            for i, w in grp[src]:
                dis[i] = w

            ret = []
            for v in range(len(grp) - 1):
                m = None
                for i in range(len(grp)):
                    if vtx[i] == 0 and dis[i] != None and (m == None or dis[m] > dis[i]):
                        m = i

                assert (m != None)
                ret.append(dis[m])
                vtx[m] = 1

                for i, w in grp[m]:
                    if vtx[i] == 0 and (dis[i] == None or dis[i] > w):
                        dis[i] = w
            print ret
            return sum(ret)

        ret = main_Kruskal(grp)
        for i in range(len(grp)):
            assert (main_Prim(grp, i) == ret)
        return ret

    def shortest(grp, src):
        def f1(grp, src):
            dis = [None] * len(grp)
            dis[src] = 0
            for v in range(len(grp) - 1):
                for i in range(len(grp)):
                    if dis[i] != None:
                        for j, w in grp[i]:
                            if dis[j] == None or dis[j] > dis[i] + w:
                                dis[j] = dis[i] + w
            print dis
            return sum(dis)

        def f2(grp, src):
            def sort(grp):
                vtx = [0] * len(grp)
                for i in range(len(grp)):
                    for j, w in grp[i]:
                        vtx[j] += 1
                stk = []
                for i in range(len(grp)):
                    if vtx[i] == 0:
                        stk.append(i)
                ret = []
                while len(stk) > 0:
                    i = stk.pop()
                    for j, w in grp[i]:
                        vtx[j] -= 1
                        if vtx[j] == 0:
                            stk.append(j)
                    ret.append(i)
                return ret

            dis = [None] * len(grp)
            dis[src] = 0
            for i in sort(grp):
                if dis[i] != None:
                    for j, w in grp[i]:
                        if dis[j] == None or dis[j] > dis[i] + w:
                            dis[j] = dis[i] + w
            print dis
            return sum(dis)

        def f3(grp, src):
            def sort(grp, src):
                vtx = [0] * len(grp)
                vtx[src] = 1
                stk = [src]
                time = 1
                ret = [None] * len(grp)
                while len(stk) > 0:
                    i = stk[-1]
                    if vtx[i] == 1:
                        vtx[i] = 2
                        for j, w in grp[i]:
                            if vtx[j] == 0:
                                vtx[j] = 1
                                stk.append(j)
                                vtx[i] = 1
                                break
                    else:
                        assert (vtx[i] == 2)
                        stk.pop()
                        ret[-time] = i
                        time += 1
                return ret

            dis = [None] * len(grp)
            dis[src] = 0
            ret = sort(grp, src)
            for i in ret:
                if dis[i] != None:
                    for j, w in grp[i]:
                        if dis[j] == None or dis[j] > dis[i] + w:
                            dis[j] = dis[i] + w

            print dis
            return sum(dis)

        def f4(grp, src):
            vtx = [0] * len(grp)
            vtx[src] = 1
            dis = [None] * len(grp)
            dis[src] = 0
            for i, w in grp[src]:
                dis[i] = w

            ret = []
            for v in range(len(grp) - 1):
                m = None
                for i in range(len(grp)):
                    if vtx[i] == 0 and dis[i] != None:
                        if m == None or dis[m] > dis[i]:
                            m = i
                if m == None:
                    break
                vtx[m] = 1
                ret.append(dis[m])

                for i, w in grp[m]:
                    if vtx[i] == 0:
                        if dis[i] == None or dis[i] > dis[m] + w:
                            dis[i] = dis[m] + w
            print ret
            return sum(ret)

        ret = f1(grp, src)
        assert (ret == f2(grp, src) == f3(grp, src) == f4(grp, src))
        return ret

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
    print '-' * 25
    assert (shortest(dag, 0) == 119)


if __name__ == '__main__':
    # testsortint()
    # testsortstr()
    # testdynamic()
    # testunionfindset()
    # testgraph()
    print 'done'
