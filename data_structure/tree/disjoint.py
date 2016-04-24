# -*- coding: utf-8 -*-
# 并查集，一种用于表示动态不相交集合(disjoint set)的数据结构
# 此类问题依赖于高效的集合查询与合并操作

# 并查集与图问题
# 1) 若union过程中发现(没有重复)输入的两个节点已有共同的根节点
# 则这两个节点必定已同属于一个集合，对于无向图而言，
# 两者之间必定存在多条通路，包括环路(一个环路可以算作多条通路)
# 2) 若所有union完成后仅剩有一个根节点，则该无向图是连通的
# 其连通分量为1


class DisjointSetList():
    pass


# use a tree to represent each disjoint set
# two heuristics can be used together: (a) union by rank and (b) path compression
# in practice, you can use either of them for simplicity
class DisjointSetForest():
    def __init__(self, num):
        # alphabet = [1,num]
        self.sets = [i for i in range(num + 1)]
        self.ranks = [0] * (num + 1)
        assert (len(self.sets) == len(self.ranks))

    # find the root of a tree
    def find(self, n):
        assert (1 <= n <= len(self.sets))
        while self.sets[n] != n:
            self.sets[n] = self.sets[self.sets[n]]  # (b)
            n = self.sets[n]
        return n

    # merge two trees
    def union(self, n1, n2):
        assert (1 <= n1 <= len(self.sets))
        assert (1 <= n2 <= len(self.sets))
        p1 = self.find(n1)
        p2 = self.find(n2)
        if p1 == p2:
            return p1
        # (a) make the root of the tree with fewer nodes
        # point to the one with more nodes
        # 由于最理想的树高度是1，且节点个数更多的树的高度也往往更高，
        # 因此将节点个数少的树挂在节点多的树下，以不改变后者的高度
        if self.ranks[p1] < self.ranks[p2]:
            self.sets[p1] = p2
            return p2
        else:
            self.sets[p2] = p1
            if self.ranks[p1] == self.ranks[p2]:
                # the rank of p2 doesn't matter any more
                self.ranks[p1] += 1
            return p1

    def testcase(self):
        print 'pass:', self.__class__


# @problem: HDU 1325
# 判断一个有向图是否是一棵树
# 需满足三个条件：a)连通，b)无环，c)入度为1(或0)
class IsItATree():
    def main(self, edgs):
        def find(ds, v):
            if ds[v] == -1:
                ds[v] = v
            while ds[v] != v:
                v = ds[v]
                if ds[v] == -1:
                    ds[v] = v
            return v

        def union(ds, v1, v2):
            p1 = find(ds, v1)
            p2 = find(ds, v2)
            ds[p2] = p1
            return (p1 == p2)  # 无向环，(b)+(c)

        num = max(map(lambda x: max(x[0], x[1]), edgs))  # max vertex id
        ds = [-1] * (num + 1)
        for v1, v2 in edgs:
            if union(ds, v1, v2):
                return False
        num = 0
        for i in range(len(ds)):
            if ds[i] != -1 and ds[i] == i:
                num += 1
        return (num == 1)  # (a)

    def testcase(self):
        def test(case):
            assert (self.main(case[0]) == case[1])

        cases = [([(6, 8), (5, 3), (5, 2), (6, 4), (5, 6)], True),
                 ([(8, 1), (7, 3), (6, 2), (8, 9), (7, 5), (7, 4), (7, 8), (7, 6)], True),
                 ([(3, 8), (6, 8), (6, 4), (5, 3), (5, 6), (5, 2)], False)
                 ]
        map(test, cases)
        print 'pass:', self.__class__


# @problem:
# Maintain a set of elements from the domain [1,n] under the operations INSERT and EXTRACT-MIN.
# Given a sequence of n INSERT and m EXTRACT-MIN calls, where each element is inserted exactly once,
# determine which element is returned by each EXTRACT-MIN call.
# The problem is “off-line” in the sense that it's allowed to process the entire call sequence
# before determining any of the returned elements.
class OfflineMinimum():
    # on-line algorithm: min-heap
    def main_heap(self, seq):
        def sink(hp, low, high):
            it = low << 1 | 1
            while it < high:
                if it + 1 < high and hp[it + 1] < hp[it]:
                    it += 1
                if hp[it] > hp[low]:
                    break
                hp[it], hp[low] = hp[low], hp[it]
                low = it
                it = low << 1 | 1

        def float(hp, low, high):
            it = (low - 1) >> 1
            while it >= high:
                if hp[it] < hp[low]:
                    break
                hp[it], hp[low] = hp[low], hp[it]
                low = it
                it = (low - 1) >> 1

        min, hp = [], []
        for i in seq:
            if i != -1:
                assert (isinstance(i, int))
                hp.append(i)
                float(hp, len(hp) - 1, 0)
            elif len(hp) > 0:
                min.append(hp[0])
                hp[0], hp[-1] = hp[-1], hp[0]
                hp = hp[:-1]
                sink(hp, 0, len(hp))
        return min

    # off-line algorithm
    def main_disjoint(self, seq):
        num = max(seq)
        assert (len(seq) - seq.count(-1) == num)
        # 1) split the sequence by EXTRACT-MIN
        sets, set = [], []
        for i in seq:
            if i != -1:
                set.append(i)
            else:
                sets.append(set)
                set = []
        sets.append(set)
        assert (len(sets) == seq.count(-1) + 1)
        assert (sum(map(lambda x: len(x), sets)) == num)
        # 2) make the disjoint sets
        ds = DisjointSetForest(num)
        ords = []
        for set in sets:
            for i in range(1, len(set)):
                ds.union(set[i], set[0])
            ords.append(set[0] if len(set) > 0 else 0)
        assert (len(ords) == seq.count(-1) + 1)
        # 3) compute the result
        # ords[j]对应于ret[j]，j表示第j次的EXTRACT-MIN操作
        # ords[j]==0，表示该次EXTRACT-MIN操作的区间还未确定
        # ords[j]==None，表示该次EXTRACT-MIN操作的结果已知
        ret = [None] * seq.count(-1)
        for i in range(1, num + 1):
            p = ds.find(i)
            for j in range(len(ords)):
                if ords[j] != None and ords[j] != 0:
                    if ds.find(ords[j]) == p:
                        break
            assert (ds.find(ords[j]) == p)
            if j < len(ords) - 1:
                assert (ret[j] == None)
                ret[j] = i
                # update the disjoint sets
                for k in range(j + 1, len(ords)):
                    if ords[k] != None:
                        if ords[k] == 0:
                            ords[k] = ords[j]
                        else:
                            ords[k] = ds.union(p, ords[k])  # p == ds.find(ords[j])
                        break
                assert (k < len(ords))
                ords[j] = None
        return ret

    def testcase(self):
        # 用-1表示EXTRACT-MIN操作
        case = [4, 8, -1, 3, -1, 9, 2, 6, -1, -1, -1, 1, 7, -1, 5]
        assert (self.main_heap(case) == self.main_disjoint(case))
        print 'pass:', self.__class__


if __name__ == '__main__':
    DisjointSetForest(10).testcase()
    IsItATree().testcase()
    OfflineMinimum().testcase()
    print 'done'
