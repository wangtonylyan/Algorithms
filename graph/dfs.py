# -*- coding: utf-8 -*-

class LakeCounting():
    def main_dfs(self, grp):
        def recur(i, j):
            if 0 <= i < len(grp) and 0 <= j < len(grp[0]) and grp[i][j] == 1:
                grp[i][j] = 0
                recur(i, j + 1)
                recur(i + 1, j + 1)
                recur(i + 1, j)
                recur(i + 1, j - 1)

        num = 0
        for i in range(len(grp)):
            for j in range(len(grp[0])):
                if grp[i][j] == 1:
                    num += 1
                    recur(i, j)

        return num

    def testcase(self):
        case = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0],
                [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                ]
        assert (self.main_dfs(case) == 3)
        print 'pass:', self.__class__


if __name__ == '__main__':
    LakeCounting().testcase()
    print 'done'
