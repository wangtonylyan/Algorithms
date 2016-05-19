# -*- coding: utf-8 -*-
# minimum(-weight) spanning tree problem
# 生成树都只有V-1条边，所谓的最小是指权重
# Kruskal从“边”的角度入手，Prim从“点”的角度入手


class MinimumSpanningTree(object):
    def __init__(self, grp):
        self.grp = grp

    def testcase(self):
        case = [
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
        # check test case
        num = 0
        for i in range(len(case)):
            for j, w1 in case[i]:
                for k, w2 in case[j]:
                    if k == i:
                        assert (w1 == w2 > 0)
                        num += 1
                        break
        assert (num == sum(map(len, case)))
        # run test case
        ret = self._testcase(case)
        # check result
        assert (len(ret) == len(case) - 1)
        assert (sum(map(lambda x: x[1], ret)) == 37)
        print 'pass:', self.__class__


class Kruskal(MinimumSpanningTree):
    def __init__(self, grp=[]):
        super(Kruskal, self).__init__(grp)

    def main(self):
        def find(ds, n):
            while ds[n] != n:
                ds[n] = ds[ds[n]]
                n = ds[n]
            return n

        def union(ds, n1, n2):
            p1 = find(ds, n1)
            p2 = find(ds, n2)
            if p1 != p2:
                ds[p2] = p1
            return p1

        # 1) build edges
        edge = []
        for i in range(len(self.grp)):
            for j, w in self.grp[i]:
                flg = True
                for e, v in edge:
                    if cmp((min(i, j), max(i, j)), e) == 0:
                        flg = False
                        break
                if flg:
                    edge.append(((min(i, j), max(i, j)), w))
        assert (len(edge) == sum(map(len, self.grp)) / 2)
        # 2) sort edges
        cnt = [0] * (max(map(lambda x: x[1], edge)) + 1)
        sort = [None] * len(edge)
        for e, w in edge:
            cnt[w] += 1
        for i in range(len(cnt) - 1):
            cnt[i + 1] += cnt[i]
        for e, w in edge:
            sort[cnt[w - 1]] = (e, w)
            cnt[w - 1] += 1
        # 3) build mst by selecting edges
        mst = []
        sets = [i for i in range(len(self.grp) + 1)]  # disjoint set
        for (i, j), w in sort:
            if find(sets, i) != find(sets, j):
                union(sets, i, j)
                mst.append(((i, j), w))
        assert (len(mst) == len(self.grp) - 1)
        return mst

    def _testcase(self, case):
        return self.__class__(case).main()


class Prim(MinimumSpanningTree):
    def __init__(self, grp=[]):
        super(Prim, self).__init__(grp)

    # 从树中的节点开始搜索
    def main_1(self, src=0):
        def _sink(hp, low, high, key=lambda x: x[1]):
            it = low << 1 | 1
            while it < high:
                if it + 1 < high and key(hp[it + 1]) < key(hp[it]):
                    it += 1
                if key(hp[it]) > key(hp[low]):
                    break
                hp[it], hp[low] = hp[low], hp[it]
                low = it
                it = low << 1 | 1

        def _pop(hp, low, high):
            assert (low <= high)
            hp[low], hp[high] = hp[high], hp[low]
            _sink(hp, low, high)
            return hp[high]

        def _extract_min(src):
            assert (vtx[src] >= 0)
            dst, wgt = _pop(self.grp[src], 0, vtx[src])
            vtx[src] -= 1
            i = 0
            while i < vtx[dst] + 1:
                if self.grp[dst][i][0] == src:
                    _pop(self.grp[dst], i, vtx[dst])
                    vtx[dst] -= 1
                    break
                i += 1
            return (dst, wgt)

        # 1) build min-heap based on self.grp
        vtx = [len(self.grp[i]) - 1 for i in range(len(self.grp))]
        for i in range(len(self.grp)):
            for j in range(vtx[i] >> 1, -1, -1):
                _sink(self.grp[i], j, vtx[i] + 1)
        # 2) build mst by popping heap
        sets = [0] * len(vtx)
        sets[src] = 1
        mst = []
        while len(mst) < len(vtx) - 1:
            min, src = None, None
            for v in range(len(sets)):
                if sets[v] == 1 and vtx[v] >= 0:
                    while vtx[v] >= 0:
                        dst = self.grp[v][0][0]
                        if sets[dst] == 0:
                            break
                        _extract_min(v)
                        vtx[v] -= 1
                    if vtx[v] >= 0 and (min == None or min[1] > self.grp[v][0][1]):
                        min = self.grp[v][0]
                        src = v
            assert (min != None and src != None)
            dst, wgt = _extract_min(src)
            assert (dst == min[0] and wgt == min[1])
            sets[dst] = 1
            mst.append(((src, dst), wgt))
        assert (sum(sets) == len(sets))
        return mst

    # 从树外的节点开始搜索
    def main_2(self, src=0):
        vtx = [0] * len(self.grp)
        vtx[src] = 1
        closest = [None] * len(self.grp)
        for i in range(len(self.grp)):
            if i != src:
                for j, w in self.grp[i]:
                    if j == src and (closest[i] == None or closest[i][1] > w):
                        closest[i] = (j, w)

        mst = []
        while len(mst) < len(vtx) - 1:
            m = None
            for i in range(len(vtx)):
                if vtx[i] == 0 and closest[i] != None:
                    if m == None or closest[m][1] > closest[i][1]:
                        m = i
            assert (m != None)
            mst.append(((m, closest[m][0]), closest[m][1]))
            vtx[m] = 1
            # incremental approach
            for i in range(len(vtx)):
                if vtx[i] == 0:
                    for j, w in self.grp[i]:
                        if j == m:
                            if closest[i] == None or closest[i][1] > w:
                                closest[i] = (j, w)
                            break
        assert (sum(vtx) == len(vtx))
        return mst

    def _testcase(self, case):
        num = lambda mst: sum(map(lambda x: x[1], mst))
        g = self.__class__(case)
        ret = g.main_2()
        for i in range(len(g.grp)):
            assert (num(g.main_1(i)) == num(g.main_2(i)) == num(ret))
        return ret


if __name__ == '__main__':
    Kruskal().testcase()
    Prim().testcase()
    print 'done'
