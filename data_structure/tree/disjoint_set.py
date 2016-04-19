# -*- coding: utf-8 -*-
# disjoint set，不相交集合，并查集
# alphabet = [1,num]


class DisjointSetLinkedList():
    def __init__(self):
        self.sets = []


# use a tree to represent each disjoint set
# use two heuristics together: (a) union by rank and (b) path compression
# in practice, you can use either of them for simplicity
class DisjointSetForest():
    def __init__(self, num):
        self.sets = [i for i in range(num + 1)]
        self.ranks = [0] * (num + 1)
        assert (len(self.sets) == len(self.ranks))

    # find the root of node
    def find(self, elem):
        assert (1 <= elem <= len(self.sets))
        it = elem
        if it > 0 and self.sets[it] != it:
            self.sets[it] = self.sets[self.sets[it]]  # (b)
            it = self.sets[it]
        return it

    def union(self, elem1, elem2):
        r1 = self.find(elem1)
        r2 = self.find(elem2)
        if r1 == r2:
            return
        # (a)
        if self.ranks[r1] < self.ranks[r2]:
            self.sets[r1] = r2
        elif self.ranks[r1] > self.ranks[r2]:
            self.sets[r2] = r1
        else:
            self.sets[r1] = r2
            # only the rank of a tree root matters
            self.ranks[r2] += 1


if __name__ == '__main__':
    UnionFind.testcase()
