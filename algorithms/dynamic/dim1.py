if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))

from algorithms.utility import *


#########################################################################################
## LeetCode 70
## 给定n级阶梯，每次1或2级，总共有几种达顶方式
class Problem1(Problem):
    def check(self, n):
        assert n >= 1

    def solution1(self, n):
        def recur(n):
            if n <= 2:
                return n

            return recur(n - 1) + recur(n - 2)

        return recur(n)

    def solution2(self, n):
        dp = [None] * (n + 1)

        dp[0], dp[1], dp[2] = 0, 1, 2

        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]  # 斐波那契

        return dp[-1]

    def solution3(self, n):
        if n <= 2:
            return n

        i, j = 1, 2

        for _ in range(3, n + 1):
            i, j = j, i + j

        return j


## LeetCode 746
## 给定每个阶梯的花费，每次1或2级，求达顶时的最小路径和
class Problem1_1(Problem):
    def check(self, lst):
        assert len(lst) >= 2

    def solution1(self, lst):
        dp = [None] * len(lst)

        dp[0], dp[1] = lst[0], lst[1]

        for i in range(2, len(lst)):
            dp[i] = min(dp[i - 2] + lst[i], dp[i - 1] + lst[i])

        return min(dp[-2], dp[-1])

    def solution2(self, lst):
        if len(lst) <= 2:
            return min(lst)

        i, j = lst[0], lst[1]

        for k in range(2, len(lst)):
            i, j = j, min(i, j) + lst[k]

        return min(i, j)


## LeetCode 53
## 给定序列，找到连续子序列的最大和
class Problem2(Problem):
    def check(self, lst):
        return self.check_list(lst)

    def solution1(self, lst):
        dp = [None] * len(lst)

        dp[0] = lst[0]

        for i in range(1, len(lst)):
            dp[i] = max(dp[i - 1], 0) + lst[i]

        return max(dp)

    def solution2(self, lst):
        maxval, last = lst[0], lst[0]

        for i in range(1, len(lst)):
            last = max(last, 0) + lst[i]
            maxval = max(maxval, last)

        return maxval


## LeetCode 300
## 给定序列，找到最长递增子序列
class Problem2_1(Problem):
    def check(self, lst):
        return self.check_list(lst)

    def solution1(self, lst):
        dp = [1] * len(lst)

        for i in range(1, len(lst)):
            for j in range(i - 1, -1, -1):
                if lst[i] > lst[j]:
                    dp[i] = max(dp[j] + 1, dp[i])

        return max(dp)


## LeetCode 198, 213
## 给定环，其中包含了每个房子内的现金金额
## 要求相邻两个房子不能同时被偷，求可被偷到的最大金额
class Problem3(Problem):
    def check(self, lst):
        assert len(lst) >= 4  # 三个及以下的情况，都只能偷一个

    # 此问题的难点在于两处：环形排列，以及非相邻的约束

    # 对于前者，有以下三种可能，以x表示偷，-表示不偷
    # -...-, x...-, -...x
    # 策略是将环转换成两个子序列，分别以序列的方式进行动态规划
    # lst[0:n-1]将覆盖可能1和2，lst[1:n]将覆盖可能1和3

    # 对于后者，仅考虑最后四个房子的前提下，有以下四种可能
    # --x-, x-x-, -x-x, x--x

    # 实现1：dp[i]记录第i个房子被偷时的最大金额，此时依赖的子结构是dp[i-3]和dp[i-2]
    def solution1(self, lst):
        dp1, dp2 = [None] * len(lst), [None] * len(lst)

        dp1[0], dp1[1], dp1[2] = lst[0], lst[1], lst[0] + lst[2]
        for i in range(3, len(lst) - 1):
            dp1[i] = max(dp1[i - 3], dp1[i - 2]) + lst[i]

        dp2[1], dp2[2], dp2[3] = lst[1], lst[2], lst[1] + lst[3]
        for i in range(4, len(lst)):
            dp2[i] = max(dp2[i - 3], dp2[i - 1]) + lst[i]

        return max(dp1[:-1] + dp2[1:])

    # 实现2：dp[i]记录前i个房子的最优解，此时依赖的子结构是dp[i-2]和dp[i-1]
    # 对于dp[i-2]，由于第i-1个房子不偷，因此必然有dp[i]=dp[i-2]+lst[i]
    # 对于dp[i-1]，只需考虑第i-1个房子被偷的情况，因此有有dp[i]=dp[i-1]
    def solution2(self, lst):
        dp1, dp2 = [None] * len(lst), [None] * len(lst)

        dp1[0], dp1[1] = lst[0], max(lst[0], lst[1])
        for i in range(2, len(lst) - 1):
            dp1[i] = max(dp1[i - 2] + lst[i], dp1[i - 1])

        dp2[1], dp2[2] = lst[1], max(lst[1], lst[2])
        for i in range(3, len(lst)):
            dp2[i] = max(dp2[i - 2] + lst[i], dp2[i - 1])

        return max(dp1[-2], dp2[-1])


if __name__ == '__main__':
    Problem.testsuit([
        [Problem1, 89, 10],
        [Problem1_1, 15, [10, 15, 20]],
        [Problem1_1, 6, [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]],
        [Problem2, 6, [-2, 1, -3, 4, -1, 2, 1, -5, 4]],
        [Problem2_1, 4, [10, 9, 2, 5, 3, 7, 20, 18]],
        [Problem3, 4, [1, 2, 3, 1]],
        [Problem3, 16, [7, 2, 1, 9, 3]],
    ])
