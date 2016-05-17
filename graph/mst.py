# -*- coding: utf-8 -*-
# minimum(-weight) spanning tree problem
# 生成树都只有V-1条边，所谓的最小是指权重


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
        ret = self.__class__(case).main()
        assert (len(ret) == len(case) - 1)
        assert (sum(map(lambda x: x[1], ret)) == 37)
        print 'pass:', self.__class__


class Kruskal(MinimumSpanningTree):
    def __init__(self, grp=[]):
        super(Kruskal, self).__init__(grp)
        # Kruskal算法从“边”的角度入手
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
        self.edge = edge

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

        # 1) sort edges
        cnt = [0] * (max(map(lambda x: x[1], self.edge)) + 1)
        sort = [None] * len(self.edge)
        for e, w in self.edge:
            cnt[w] += 1
        for i in range(len(cnt) - 1):
            cnt[i + 1] += cnt[i]
        for e, w in self.edge:
            sort[cnt[w - 1]] = (e, w)
            cnt[w - 1] += 1
        # 2) select edges
        mst = []
        sets = [i for i in range(len(self.grp) + 1)]  # disjoint set
        for (i, j), w in sort:
            if find(sets, i) != find(sets, j):
                union(sets, i, j)
                mst.append(((i, j), w))
        assert (len(mst) == len(self.grp) - 1)
        return mst


class Prim(MinimumSpanningTree):
    def __init__(self, grp=[]):
        super(Prim, self).__init__(grp)
        # Prim算法从“点”的角度入手
        self.vtx = [None] * (len(self.grp))
        for i in range(len(self.grp)):
            for j in range((len(self.grp[i]) - 1) >> 1, -1, -1):
                self._sink(self.grp[i], j, len(self.grp[i]))
            self.vtx[i] = len(self.grp[i]) - 1

    def _sink(self, hp, low, high, key=lambda x: x[1]):
        it = low << 1 | 1
        while it < high:
            if it + 1 < high and key(hp[it + 1]) < key(hp[it]):
                it += 1
            if key(hp[it]) > key(hp[low]):
                break
            hp[it], hp[low] = hp[low], hp[it]
            low = it
            it = low << 1 | 1

    def _pop(self, hp, low, high):
        assert (low <= high)
        hp[low], hp[high] = hp[high], hp[low]
        self._sink(hp, low, high)
        return hp[high]

    def main(self):
        src = 0
        a, w = self._pop(self.grp[src], 0, self.vtx[src])
        self.vtx[src] -= 1
        for i in range(len(self.vtx[a])):
            if self.grp[a][i][0] == src:
                self.grp[a][i], self.grp[a][self.vtx[a]] = self.grp[a][-1], self.grp[a][i]
                self._sink(self.grp[a], i, )
                self.vtx[a] -= 1
                break

        mst = [((src, m[0]), m[1])]
        sets = [mst[0][0][0], mst[0][0][1]]

        print self.grp[src], self.vtx[src]
        print self.grp[m[1]], self.vtx[m[1]]
        return
        while len(mst) < len(self.vtx) - 1:
            m = None
            for i in range(len(sets)):
                self.grp[sets[i]][0][1]
            for v in sets:
                self.grp[v][0]
            for (i, j), w in mst:
                for t in self.grp[i]:
                    if self.vtx[t[0]] == 0:
                        self.vtx[t[0]] = 1
                        m = ((i, t[0]), t[1]) if m == None or m[1] > t[1] else m

            mst.append(m)

        print mst
        return mst


if __name__ == '__main__':
    Kruskal().testcase()
    Prim().testcase()
    print 'done'
