# -*- coding: utf-8 -*-
# @problem: graphic sort
# topological ordering: for every directed edge uv, vertex u must come before vertex v
# This ordering only exists for a dag.

from base.graph import DirectedAcyclicGraphTest


class TopologicalSort(DirectedAcyclicGraphTest):
    def __init__(self):
        super(TopologicalSort, self).__init__(False)

    def main_Kahn(self, grp):
        dgr = [0] * len(grp)  # in-degree
        for i in range(len(grp)):
            for j in grp[i]:
                dgr[j] += 1
        # 保存入度为0的节点的容器
        # 由于仅当一个节点的入度首次为0时，该节点才会被存入此容器
        # 即意味着在其前的节点都已经确定了拓扑顺序
        # 因此该算法不依赖于此容器的具体类型，包括set、queue、stack等
        # 采用不同的容器类型会导致最终得到的拓扑顺序不唯一
        # 换言之，对于任意时刻该容器中的所有节点，彼此之间不存在唯一的拓扑顺序
        vtx = set()
        for i in range(len(grp)):
            if dgr[i] == 0:
                vtx.add(i)
        sort = []
        while len(vtx) > 0:
            i = vtx.pop()  # 将入度已为0的节点i从图中删除
            for j in grp[i]:  # 方式是删除所有以节点i为起始点的有向边
                dgr[j] -= 1
                if dgr[j] == 0:
                    vtx.add(j)
            sort.append(i)
        return sort if len(sort) == len(grp) else None

    def main_dfs(self, grp):
        vtx = [0] * len(grp)
        for i in range(len(grp)):
            for j in grp[i]:
                vtx[j] += 1  # in-degree
        stk = []
        for i in range(len(grp)):
            if vtx[i] == 0:
                vtx[i] = 1  # initial state
                stk.append(i)
            else:
                vtx[i] = 0
        sort = [None] * len(grp)
        ind = 0
        while len(stk) > 0:
            i = stk[-1]
            assert (vtx[i] > 0)
            if vtx[i] == 1:
                vtx[i] = 2
                for j in grp[i]:
                    if vtx[j] == 0:
                        vtx[j] = 1
                        stk.append(j)
                        vtx[i] = 1
                        break
                    elif j in stk:  # the current stk is exactly a path
                        return None  # loop exists
            else:
                assert (vtx[i] == 2)
                stk.pop()
                ind += 1
                sort[-ind] = i
        assert (ind == len(grp))
        return sort

    def testcase(self):
        def test(case):
            def check(ret):
                for i in range(len(ret)):
                    for j in ret[:i]:
                        assert (j not in case[ret[i]])

            ret1 = self.main_Kahn(case)
            ret2 = self.main_dfs(case)
            assert (len(ret1) == len(ret2) == len(case))
            map(check, [ret1, ret2])

        self._testcase(test, self._gencase())


if __name__ == '__main__':
    TopologicalSort().testcase()
    print 'done'
