# -*- coding: utf-8 -*-

import copy
import random
import time
from data_structure.heap.binary import MinBinaryHeap
from data_structure.disjoint import DisjointSetForest


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

    times = 300
    strlen = 500
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
        cpy = its[:]
        for w, v in its:
            k = 1
            while (w << (k + 1)) - w <= wgt:
                cpy.append((w << k, v << k))
                k += 1
            if (w << k) - w <= wgt - w:
                k = (wgt - (w << k) + w) / w
                assert (k > 0)
                cpy.append((w * k, v * k))
        its = cpy

        tab = [[0] * (len(its) + 1) for _ in range(wgt + 1)]
        for i in range(1, wgt + 1):
            for j in range(1, len(its) + 1):
                tab[i][j] = max(tab[i - its[j - 1][0]][j - 1] + its[j - 1][1] if i >= its[j - 1][0] else 0,
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
            cpy = copy.deepcopy(its)
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
        def main_1(grp):
            edge = []
            for i in range(len(grp)):
                for j, w in grp[i]:
                    m, n = min(i, j), max(i, j)
                    if (m, n, w) not in edge:
                        edge.append((m, n, w))
            assert (len(edge) == sum(map(len, grp)) / 2)
            edge.sort(key=lambda x: x[2])
            ret = []
            ds = DisjointSetForest(len(grp))
            for i, j, w in edge:
                if ds.find(i) != ds.find(j):
                    ret.append(w)
                    ds.union(i, j)
            assert (len(ret) == len(grp) - 1)
            return sum(ret)

        def main_2(grp, src):
            vtx = [0] * len(grp)
            dis = [None] * len(grp)
            hp = MinBinaryHeap(key=lambda x: x[1])
            dis[src] = 0
            vtx[src] = 1
            for i, w in grp[src]:
                dis[i] = w
                hp.push((i, dis[i]))
            while len(hp) > 0:
                i, w = hp.pop()
                if vtx[i] == 1 or dis[i] < w:
                    continue
                vtx[i] = 1
                for j, v in grp[i]:
                    if vtx[j] == 0 and (dis[j] == None or dis[j] > v):
                        dis[j] = v
                        hp.push((j, dis[j]))
            return sum(dis)

        ret = main_1(grp)
        for i in range(len(grp)):
            assert (main_2(grp, i) == ret)
        return ret

    def shortest(grp, src):
        def f1(grp, src):
            dis = [None] * len(grp)
            dis[src] = 0
            for _ in range(len(grp)):
                for i in range(len(grp)):
                    if dis[i] != None:
                        for j, w in grp[i]:
                            if dis[j] == None or dis[j] > dis[i] + w:
                                if _ == len(grp) - 1:
                                    return None
                                dis[j] = dis[i] + w
            return sum(dis)

        def f2(grp, src):
            def sort(grp):
                dgr = [0] * len(grp)
                for i in range(len(grp)):
                    for j, w in grp[i]:
                        dgr[j] += 1
                st = set()
                for i in range(len(grp)):
                    if dgr[i] == 0:
                        st.add(i)
                ret = []
                while len(st) > 0:
                    i = st.pop()
                    for j, w in grp[i]:
                        dgr[j] -= 1
                        if dgr[j] == 0:
                            st.add(j)
                    ret.append(i)
                return ret if len(ret) == len(grp) else None

            seq = sort(grp)
            if seq == None:
                return None
            dis = [None] * len(grp)
            dis[src] = 0
            for i in seq:
                if dis[i] is not None:
                    for j, w in grp[i]:
                        if dis[j] is None or dis[j] > dis[i] + w:
                            dis[j] = dis[i] + w
            return sum(dis)

        def f3(grp, src):
            def sort(grp):
                vtx = [0] * len(grp)
                for i in range(len(grp)):
                    for j, w in grp[i]:
                        vtx[j] += 1
                stk = []
                for i in range(len(grp)):
                    if vtx[i] == 0:
                        vtx[i] = 1
                        stk.append(i)
                    else:
                        vtx[i] = 0
                ret = []
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
                            elif j in stk:
                                return None
                    else:
                        assert (vtx[i] == 2)
                        stk.pop()
                        ret = [i] + ret
                return ret if len(ret) == len(grp) else None

            seq = sort(grp)
            if seq == None:
                return None
            dis = [None] * len(grp)
            dis[src] = 0
            for i in seq:
                if dis[i] is not None:
                    for j, w in grp[i]:
                        if dis[j] is None or dis[j] > dis[i] + w:
                            dis[j] = dis[i] + w
            return sum(dis)

        def f4(grp, src):
            vtx = [0] * len(grp)
            vtx[src] = 1
            dis = [None] * len(grp)
            dis[src] = 0
            hp = MinBinaryHeap(key=lambda x: x[1])
            for i, w in grp[src]:
                dis[i] = w
                hp.push((i, dis[i]))
            ret = []
            while len(hp) > 0:
                i, w = hp.pop()
                if vtx[i] == 1 or w > dis[i]:
                    continue
                vtx[i] = 1
                for j, v in grp[i]:
                    if vtx[j] == 0 and (dis[j] is None or dis[j] > dis[i] + v):
                        dis[j] = dis[i] + v
                        hp.push((j, dis[j]))
                ret.append(w)
            return sum(ret)

        ret = f1(grp, src)
        assert (ret == f4(grp, src) == f2(grp, src) == f3(grp, src))
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


def testmatch():
    from string.match import StringMatch

    class KMP(StringMatch):
        def __init__(self):
            super(KMP, self).__init__()

        def main(self, txt, pat):
            jmp = [0] * len(pat)
            i, j = 0, jmp[0]
            while i < len(pat) - 1:
                if pat[j] == pat[i + 1]:
                    i += 1
                    j += 1
                    jmp[i] = j
                elif j > 0:
                    j = jmp[j - 1]
                else:
                    i += 1
            ret = []
            i, j = 0, 0
            while i < len(txt) - len(pat) + 1:
                while j < len(pat) and txt[i + j] == pat[j]:
                    j += 1
                if j == len(pat):
                    ret.append(i)
                elif j == 0:
                    i += 1
                    continue
                i += j - jmp[j - 1]
                j = jmp[j - 1]
            return ret

    class BM(StringMatch):
        def __init__(self):
            super(BM, self).__init__()

        def main(self, txt, pat):
            def preprocess(pat):
                tab = [0] * len(pat)
                low, high = 0, 0
                for i in range(1, len(pat)):
                    if i < high:
                        if high - i > tab[i - low]:
                            tab[i] = tab[i - low]
                            continue
                        else:
                            j = high - i
                    else:
                        j = 0

                    while j < len(pat) - i and pat[i + j] == pat[j]:
                        j += 1
                    tab[i] = j
                    low, high = i, i + tab[i]
                return tab

            tab = [0] * len(pat)
            low, high = len(pat) - 1, len(pat) - 1
            for i in range(len(pat) - 2, -1, -1):
                if i > low:
                    if i - low > tab[len(pat) - 1 - (high - i)]:
                        tab[i] = tab[len(pat) - 1 - (high - i)]
                        continue
                    else:
                        j = len(pat) - 1 - (i - low)
                else:
                    j = len(pat) - 1
                while j >= len(pat) - 1 - i and pat[i - (len(pat) - 1 - j)] == pat[j]:
                    j -= 1
                tab[i] = len(pat) - 1 - j
                low, high = i - tab[i], i
            assert (tab == preprocess(pat[::-1])[::-1])

            bad = [[] for _ in range(self.alphabet)]
            for i in range(len(pat) - 1, -1, -1):
                bad[self.ord(pat[i])].append(i)

            sfx = [-1] * len(pat)
            for i in range(len(pat) - 1):
                if tab[i] > 0:
                    sfx[len(pat) - tab[i]] = i

            pfx = [-1] * len(pat)
            if tab[0] == 1:
                pfx[len(pat) - 1] = 0
            for i in range(1, len(pat) - 1):
                if tab[i] == i + 1:
                    pfx[len(pat) - (i + 1)] = i
                else:
                    pfx[len(pat) - (i + 1)] = pfx[len(pat) - i]

            ret = []
            i = 0
            while i < len(txt) - len(pat) + 1:
                j = len(pat) - 1
                while j >= 0 and txt[i + j] == pat[j]:
                    j -= 1
                if j == -1:
                    ret.append(i)
                    i += len(pat) - 1 - pfx[1] if len(pat) > 1 else 1
                else:
                    bd = bad[self.ord(txt[i + j])]
                    k = 0
                    while k < len(bd) and bd[k] > j:
                        k += 1
                    st1 = j - bd[k] if k < len(bd) else j + 1

                    if j == len(pat) - 1:
                        st2 = 1
                    elif sfx[j + 1] >= 0:
                        st2 = len(pat) - 1 - sfx[j + 1]
                    else:
                        st2 = len(pat) - 1 - pfx[j + 1]

                    i += max(st1, st2)
            return ret

    KMP().testcase()
    BM().testcase()


def testsuffix():
    from string.suffix import EnhancedSuffixArray

    class ESA(EnhancedSuffixArray):
        def __init__(self):
            super(ESA, self).__init__()

        def main_2(self, str):
            class Node():
                def __init__(self, index, rank0, rank1):
                    self.index = index
                    self.rank0 = rank0
                    self.rank1 = rank1

            def cmp(x, y):
                if x.rank0 < y.rank0 or (x.rank0 == y.rank0 and x.rank1 < y.rank1):
                    return -1
                return 1

            gap = 1
            sfx = [Node(i, self.ord(str[i]), self.ord(str[i + gap]) if i + gap < len(str) else -1)
                   for i in range(len(str))]
            inv = [None] * len(str)
            sfx.sort(cmp=cmp)
            gap <<= 1
            while gap < len(str):
                pre = sfx[0].rank0
                sfx[0].rank0 = 0
                inv[sfx[0].index] = 0
                for i in range(1, len(str)):
                    if sfx[i].rank0 == pre and sfx[i].rank1 == sfx[i - 1].rank1:
                        pre = sfx[i].rank0
                        sfx[i].rank0 = sfx[i - 1].rank0
                    else:
                        pre = sfx[i].rank0
                        sfx[i].rank0 = sfx[i - 1].rank0 + 1
                    inv[sfx[i].index] = i
                for i in range(len(str)):
                    if sfx[i].index + gap < len(str):
                        sfx[i].rank1 = sfx[inv[sfx[i].index + gap]].rank0
                    else:
                        sfx[i].rank1 = -1
                sfx.sort(cmp=cmp)
                gap <<= 1

            sfx = [s.index for s in sfx]
            lcp = [None] * len(str)
            for i in range(len(str)):
                inv[sfx[i]] = i
            k = 0
            for i in range(len(str)):
                if inv[i] == len(str) - 1:
                    k = 0
                    lcp[len(str) - 1] = 0
                    continue
                j = sfx[inv[i] + 1]
                while i + k < len(str) and j + k < len(str) and str[i + k] == str[j + k]:
                    k += 1
                lcp[inv[i]] = k
                if k > 0:
                    k -= 1
            assert (lcp == self.main_lcp_Kasai(str, sfx))
            return sfx

    ESA().testcase()


def testsplay():
    from data_structure.tree.binary.bst import SelfBalancingBinarySearchTree, BinarySearchTreeTest

    class SplayTree(SelfBalancingBinarySearchTree):
        def __init__(self):
            super(SplayTree, self).__init__()

        def splay(self, spt, key):
            assert (spt is not None and key is not None)
            root = self.__class__.Node(None, None)
            left = right = root
            while spt.key != key:
                if key < spt.key:
                    if spt.left is None:
                        break
                    if key < spt.left.key:
                        spt = self._rotateRight_(spt)
                        if spt.left is None:
                            break
                    right.left = spt
                    right = right.left
                    spt = spt.left
                else:
                    if spt.right is None:
                        break
                    if key > spt.right.key:
                        spt = self._rotateLeft_(spt)
                        if spt.right is None:
                            break
                    left.right = spt
                    left = left.right
                    spt = spt.right
            left.right = spt.left
            right.left = spt.right
            spt.left = root.right
            spt.right = root.left
            assert (spt.left is None or spt.left.key < key)
            assert (spt.right is None or spt.right.key > key)
            return spt

        def insert(self, key, value):
            if not self.root:
                self.root = self.__class__.Node(key, value)
            else:
                self.root = self.splay(self.root, key)
                if self.root.key == key:
                    self.root.value = value
                else:
                    node = self.__class__.Node(key, value)
                    if key < self.root.key:
                        node.right = self.root
                        node.left = self.root.left
                        self.root.left = None
                    else:
                        node.left = self.root
                        node.right = self.root.right
                        self.root.right = None
                    self.root = node

        def delete(self, key):
            if self.root:
                self.root = self.splay(self.root, key)
                if not self.root.left:
                    self.root = self.root.right
                else:
                    self.root.left = self.splay(self.root.left, key)
                    assert (self.root.left.right is None)
                    self.root.left.right = self.root.right
                    self.root = self.root.left

    BinarySearchTreeTest(SplayTree, 1000).delete()


if __name__ == '__main__':
    # testsortint()
    # testsortstr()
    # testdynamic()

    # testunionfindset()
    # testgraph()

    # testmatch()
    # testsuffix()
    # testsplay()
    print 'done'
