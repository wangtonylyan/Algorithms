# -*- coding: utf-8 -*-
# @problem: graphic sort
# topological ordering: for every directed edge uv, vertex u must come before vertex v
# This ordering only exists for a dag.


from collections import deque


class TopologicalSort():
    def main_Kahn(self, grp):
        # 1)
        vtx = [0] * len(grp)  # in-degree
        for i in range(len(grp)):
            for j in grp[i]:
                vtx[j] += 1
        # 保存入度为0的节点的容器
        # 由于仅当一个节点的入度首次为0时，该节点才会被存入此容器
        # 即意味着在其前的节点都已经确定了拓扑顺序
        # 因此该算法不依赖于此容器的具体类型，包括set、queue、stack等
        # 采用不同的容器类型会导致最终得到的拓扑顺序不唯一
        # 换言之，对于任意时刻该容器中的所有节点，彼此之间不存在唯一的拓扑顺序
        que = deque()
        for i in range(len(grp)):
            if vtx[i] == 0:
                que.append(i)
        # 2)
        sort = []
        while len(que) > 0:
            i = que.popleft()  # 将入度已为0的节点i从图中删除
            for j in grp[i]:  # 方式是删除所有以节点i为起始点的有向边
                vtx[j] -= 1
                if vtx[j] == 0:
                    que.append(j)
            sort.append(i)
        # 3)
        return sort if len(sort) == len(grp) else None

    def main_dfs(self, grp):
        # 1)
        indg = [0] * len(grp)  # in-degree
        for i in range(len(grp)):
            for j in grp[i]:
                indg[j] += 1
        # 2)
        vtx = [0] * len(grp)
        sort = [None] * len(grp)
        time = 1
        for src in range(len(grp)):
            if indg[src] == 0:
                assert (vtx[src] == 0)
                stk = [src]
                vtx[src] = 1
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
                            elif j in stk:  # 整个stk就是一条路径
                                return None  # loop exists
                    else:
                        assert (vtx[i] == 2)
                        stk.pop()
                        # 3)
                        sort[-time] = i  # sort.insert(0, i)
                        time += 1
        return sort

    def testcase(self):
        def test(case):
            assert (self.main_Kahn(case) == self.main_dfs(case))

        cases = [
            [[1, 7], [2, 7], [8, 3, 5], [4, 5], [5], [6], [7, 8], [], []],
        ]
        map(test, cases)
        print 'pass:', self.__class__


if __name__ == '__main__':
    TopologicalSort().testcase()
    print 'done'
