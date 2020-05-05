if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))

from algorithms.utility import *


#########################################################################################
## LeetCode 62, 63
## 给定标识了障碍物的m*n网格，每次只能向右或向下移动一格，求从左上角至右下角的路径总数
# 当没有障碍物时，就是m*n网格内合法的路径总数
class LeetCode63(Problem):
    def check(self, mat):
        return self.check_matrix(mat)

    def solution1(self, mat):
        def recur(i, j):
            if mat[i][j]:
                return 0
            if i == 0 and j == 0:
                return 1
            if i == 0:
                return recur(i, j - 1)
            if j == 0:
                return recur(i - 1, j)

            return recur(i - 1, j) + recur(i, j - 1)

        return recur(len(mat) - 1, len(mat[0]) - 1)

    def solution2(self, mat):
        m, n = len(mat), len(mat[0])
        dp = [[None] * n for _ in range(m)]

        dp[0][0] = 1 if not mat[0][0] else 0
        for i in range(1, m):
            dp[i][0] = dp[i - 1][0] if not mat[i][0] else 0
        for j in range(1, n):
            dp[0][j] = dp[0][j - 1] if not mat[0][j] else 0

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1] if not mat[i][j] else 0

        return dp[-1][-1]

    def solution3(self, mat):
        m, n = len(mat), len(mat[0])
        dp = [0] * n

        if not mat[0][0]:
            dp[0] = 1

        for i in range(m):
            dp[0] = dp[0] if not mat[i][0] else 0
            for j in range(1, n):
                dp[j] = dp[j - 1] + dp[j] if not mat[i][j] else 0

        return dp[-1]


## LeetCode 64
## 给定存满了数字的m*n网格，每次只能向右或向下移动一格，求最小路径和
class LeetCode64(Problem):
    def check(self, mat):
        return self.check_matrix(mat)

    def solution1(self, mat):
        def recur(i, j):
            if i == 0 and j == 0:
                return mat[0][0]
            if i == 0:
                return recur(i, j - 1) + mat[i][j]
            if j == 0:
                return recur(i - 1, j) + mat[i][j]

            return min(recur(i - 1, j), recur(i, j - 1)) + mat[i][j]

        return recur(len(mat) - 1, len(mat[0]) - 1)

    def solution2(self, mat):
        m, n = len(mat), len(mat[0])
        dp = [[None] * n for _ in range(m)]

        dp[0][0] = mat[0][0]
        for i in range(1, m):
            dp[i][0] = dp[i - 1][0] + mat[i][0]
        for j in range(1, n):
            dp[0][j] = dp[0][j - 1] + mat[0][j]

        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + mat[i][j]

        return dp[-1][-1]

    def solution3(self, mat):
        m, n = len(mat), len(mat[0])
        dp = mat[0][:]

        for j in range(1, n):
            dp[j] += dp[j - 1]

        for i in range(1, m):
            dp[0] += mat[i][0]
            for j in range(1, n):
                dp[j] = min(dp[j - 1], dp[j]) + mat[i][j]

        return dp[-1]


## LeetCode 120
## 给定一个三角形，找出自顶向下的最小路径和
class LeetCode120(Problem):
    def check(self, mat):
        return self.check_list(mat)

    def solution1(self, mat):
        def recur(i, j):
            if i == 0:
                return mat[0][0]

            if j == 0:
                return recur(i - 1, j) + mat[i][j]
            if j == i:
                return recur(i - 1, j - 1) + mat[i][j]

            return min(recur(i - 1, j - 1), recur(i - 1, j)) + mat[i][j]

        return min([recur(len(mat) - 1, j) for j in range(len(mat))])

    # top-down
    def solution2(self, mat):
        dp = [[None] * (i + 1) for i in range(len(mat))]

        dp[0][0] = mat[0][0]

        for i in range(1, len(mat)):
            dp[i][0] = dp[i - 1][0] + mat[i][0]
            dp[i][-1] = dp[i - 1][-1] + mat[i][-1]
            for j in range(1, i):
                dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j]) + mat[i][j]

        return min(dp[-1])

    def solution3(self, mat):
        dp = [None] * len(mat)

        dp[0] = mat[0][0]

        for i in range(1, len(mat)):
            dp[i] = dp[i - 1] + mat[i][i]
            for j in range(i - 1, 0, -1):
                dp[j] = min(dp[j - 1], dp[j]) + mat[i][j]
            dp[0] += mat[i][0]

        return min(dp)

    # bottom-up
    def solution4(self, mat):
        dp = mat[-1][:]

        for i in range(len(mat) - 2, -1, -1):
            for j in range(i + 1):
                dp[j] = min(dp[j], dp[j + 1]) + mat[i][j]

        return dp[0]


## LeetCode 221
## 给定仅存储了零和非零的m*n网格，求由非零数字所组成的最大正方形的边长
class LeetCode221(Problem):
    def check(self, mat):
        return self.check_matrix(mat)

    def solution1(self, mat):
        m, n = len(mat), len(mat[0])
        dp = [[None] * n for _ in range(m)]

        for i in range(m):
            dp[i][0] = 1 if mat[i][0] else 0
        for j in range(n):
            dp[0][j] = 1 if mat[0][j] else 0

        for i in range(1, m):
            for j in range(1, n):
                # 正方形dp[i-1][j]和dp[i][j-1]只需向下和向右扩张
                # 正方形dp[i-1][j-1]需要同时向下和向右扩张
                # 对于三者中最小正方形的扩张，总能由其余两个正方形来保证
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1],
                               dp[i - 1][j - 1]) + 1 \
                    if mat[i][j] else 0

        return max(map(max, dp))

    def solution2(self, mat):
        m, n = len(mat), len(mat[0])

        dp = mat[0][:]
        maxlen = max(dp)

        for i in range(1, m):
            diag, dp[0] = dp[0], mat[i][0]
            for j in range(1, n):
                diag, dp[j] = dp[j], min(dp[j], dp[j - 1], diag) + 1 \
                    if mat[i][j] else 0
            maxlen = max(maxlen, max(dp))

        return maxlen


#########################################################################################
## LeetCode 256, 265
## 给定排成一列的m个房子，每个房子可以刷n种颜色
## 已知每个房子刷成各种颜色的花费，要求相邻两个房子不能刷成同种颜色
## 求出最少的花费
class LeetCode265(Problem):
    def check(self, mat):
        return self.check_matrix(mat)

    def solution1(self, mat):
        m, n = len(mat), len(mat[0])
        dp = [[None] * n for _ in range(m)]

        dp[0] = mat[0]

        for i in range(1, m):
            for j in range(n):
                dp[i][j] = min(dp[i - 1][:j] + dp[i - 1][j + 1:]) + mat[i][j]

        return min(dp[-1])


## 国王与金矿
class Problem1(Problem):
    def check(self, mat, n):
        return self.check_matrix(mat)

    def solution1(self, mat, n):
        def recur(mat, n):
            if n == 0:
                return 0
            if len(mat) == 1:
                return mat[0][0] if n >= mat[0][1] else 0

            return max(recur(mat[:-1], n - mat[-1][1]) + mat[-1][0],
                       recur(mat[:-1], n)) \
                if n >= mat[-1][1] else recur(mat[:-1], n)

        return recur(mat, n)

    def solution2(self, mat, n):
        m = len(mat)
        dp = [[None] * (n + 1) for _ in range(m)]

        for i in range(m):
            dp[i][0] = 0
        for j in range(1, n + 1):
            dp[0][j] = mat[0][0] if j >= mat[0][1] else 0

        for i in range(1, m):
            for j in range(1, n + 1):
                dp[i][j] = max(dp[i - 1][j - mat[i][1]] + mat[i][0],
                               dp[i - 1][j]) \
                    if j >= mat[i][1] else dp[i - 1][j]

        return dp[-1][-1]

    def solution3(self, mat, n):
        m = len(mat)
        dp = [None] * (n + 1)

        for j in range(n + 1):
            dp[j] = mat[0][0] if j >= mat[0][1] else 0

        for i in range(1, m):
            for j in range(n, 0, -1):  # 注意反向遍历，以避免过早修改第i-1个金矿
                dp[j] = max(dp[j - mat[i][1]] + mat[i][0], dp[j]) \
                    if j >= mat[i][1] else dp[j]

        return dp[-1]


if __name__ == '__main__':
    Problem.testsuit([
        [LeetCode63, 28, [[0] * 7 for _ in range(3)]],
        [LeetCode63, 2, [[0, 0, 0],
                         [0, 1, 0],
                         [0, 0, 0]]],
        [LeetCode64, 7, [[1, 3, 1],
                         [1, 5, 1],
                         [4, 2, 1]]],
        [LeetCode120, 11, [[2],
                           [3, 4],
                           [6, 5, 7],
                           [4, 1, 8, 3]]],
        [LeetCode221, 2, [[1, 0, 1, 0, 0],
                          [1, 0, 1, 1, 1],
                          [1, 1, 1, 1, 1],
                          [1, 0, 0, 1, 0]]],
        [LeetCode221, 3, [[1, 1, 1, 0],
                          [0, 1, 1, 1],
                          [1, 1, 1, 1],
                          [1, 1, 1, 1]]],
        [LeetCode265, 5, [[1, 5, 3],
                          [2, 9, 4]]],
        [LeetCode265, 10, [[17, 2, 17],
                           [16, 16, 5],
                           [14, 3, 19]]],
        [Problem1, 900, [[200, 3],
                         [300, 4],
                         [350, 3],
                         [400, 5],
                         [500, 5]], 10],
    ])
