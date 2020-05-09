if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))

from algorithms.utility import *


# 从收益的角度，无论开/平仓，买入和卖出分别为负数和正数，两者之和就是收益

#########################################################################################
## 给定一个数组，其记录了同一只股票每天的价格，同一时间最多只能保留一笔交易，
## 在最多执行n次交易的前提下，求所能获取的最大利润
class LeetCode188(Problem):
    def check(self, lst, n):
        assert n > 0
        return self.check_list_nonempty(lst), n

    # 动态规划的通解，标准的三维动态规划问题
    def algo1(self, lst, n):
        m = len(lst)
        dp = [[[None, None] for _ in range(n + 1)]
              for _ in range(m + 1)]

        # 每次只需记录一笔交易，且需要区分出初始情况与非初始的当前最优
        # 对于买入开仓的初始值，可选取小于-max(lst)的任意数
        # 即可保证dp[][][1]+lst[]和dp[][][1]的初始值总是最小的，也就永不构成当前最优解
        for i in range(m + 1):
            dp[i][0] = [0, -max(lst) - 1]
        for j in range(n + 1):
            dp[0][j] = [0, -max(lst) - 1]

        for i in range(1, m + 1):  # 交易天数
            for j in range(1, n + 1):  # 最大买入次数
                # 不考虑dp[i][j-1]的情况，因为同一天买入卖出和卖出买入是没有收益的
                dp[i][j][0] = max(dp[i - 1][j][1] + lst[i - 1],  # 卖出平仓
                                  dp[i - 1][j][0])
                dp[i][j][1] = max(dp[i - 1][j - 1][0] - lst[i - 1],  # 买入开仓
                                  dp[i - 1][j][1])

        return dp[-1][-1][0]


## 给定一个数组，其记录了同一只股票每天的价格，同一时间最多只能保留一笔交易，
## 在最多执行1次交易的前提下，求所能获取的最大利润
class LeetCode121(Problem):
    def check(self, lst):
        return self.check_list_nonempty(lst)

    # 基于动态规划的通解，无需规划第二维度上的交易次数，即有n=1
    def algo1(self, lst):
        dp = [[None, None] for _ in range(len(lst))]

        dp[0] = [0, -lst[0]]

        for i in range(1, len(lst)):
            dp[i][0] = max(dp[i - 1][1] + lst[i], dp[i - 1][0])
            # 由于只能进行一次交易，因此前一天平仓的收益必定为零
            dp[i][1] = max(0 - lst[i], dp[i - 1][1])

        return dp[-1][0]

    # 空间上的优化
    def algo1_1(self, lst):
        dp = [0, -lst[0]]

        for i in range(1, len(lst)):
            dp[0] = max(dp[1] + lst[i], dp[0])
            dp[1] = max(-lst[i], dp[1])

        return dp[0]

    # 反向规划，dp[0]和dp[1]分别为最后一天卖出和买入的收益
    # 卖出收益，非真实所得，因此最终的收益为dp[1]
    def algo1_2(self, lst):
        dp = [lst[-1], 0]

        for i in range(len(lst) - 2, -1, -1):
            # dp[i][0] = max(dp[i+1][1]+lst[i], dp[i+1][0])
            # dp[i][1] = max(dp[i+1][0]-lst[i], dp[i+1][1])
            dp[0] = max(lst[i], dp[0])  # 卖出开仓，尽可能地卖出高价
            dp[1] = max(dp[0] - lst[i], dp[1])  # 买入平仓，仅可能地获取高收益

        return dp[1]

    # 常规思维，将输入数组看作是一个上下波动的函数曲线，求最大落差
    def algo2(self, lst):
        def recur(lst):
            if len(lst) == 1:
                return 0, lst[0]

            maxdif, minval = recur(lst[:-1])

            if lst[-1] < minval:
                minval = lst[-1]
            elif lst[-1] - minval > maxdif:
                maxdif = lst[-1] - minval

            return maxdif, minval

        maxdif, _ = recur(lst)
        return maxdif

    # 由上述的递归实现可见，从左至右的单次遍历中，只需同时维护最大差和最小值即可
    def algo2_1(self, lst):
        maxdif, minval = 0, lst[0]

        for i in range(1, len(lst)):
            if lst[i] < minval:
                minval = lst[i]
            elif lst[i] - minval > maxdif:
                maxdif = lst[i] - minval

        return maxdif

    # 对于algo2，似乎还可以用移动窗口的思想来理解
    def algo3(self, lst):
        pass


## 给定一个数组，其记录了同一只股票每天的价格，同一时间最多只能保留一笔交易，
## 在最多执行2次交易的前提下，求所能获取的最大利润
class LeetCode123(Problem):
    def check(self, lst):
        assert len(lst) > 1
        return lst

    # 基于动态规划的通解，且有n=2
    def algo1(self, lst):
        dp = [[[None, None] for _ in range(2)]
              for _ in range(len(lst))]

        # 与通解相同的是，第一天无论允许多少次交易，都为以下情况
        dp[0][0] = [0, -lst[0]]
        dp[0][1] = [0, -lst[0]]

        for i in range(1, len(lst)):
            dp[i][0][0] = max(dp[i - 1][0][1] + lst[i], dp[i - 1][0][0])
            dp[i][0][1] = max(0 - lst[i], dp[i - 1][0][1])

        for i in range(1, len(lst)):
            dp[i][1][0] = max(dp[i - 1][1][1] + lst[i], dp[i - 1][1][0])
            dp[i][1][1] = max(dp[i - 1][0][0] - lst[i], dp[i - 1][1][1])

        return dp[-1][-1][0]

    # 常规思路，仅适用于最多交易两次的情况
    def algo2(self, lst):
        if len(lst) == 2:
            return max(lst[1] - lst[0], 0)

        dp1 = [0] * len(lst)
        maxdif, minval = 0, lst[0]

        for i in range(1, len(lst) - 1):
            if lst[i] < minval:
                minval = lst[i]
            elif lst[i] - minval > maxdif:
                maxdif = lst[i] - minval
            dp1[i] = maxdif

        dp2 = [0] * len(lst)
        maxdif, maxval = 0, lst[-1]

        for i in range(len(lst) - 2, 0, -1):
            if lst[i] > maxval:
                maxval = lst[i]
            elif maxval - lst[i] > maxdif:
                maxdif = maxval - lst[i]
            dp2[i] = maxdif

        # 同一天无需进行两次交易，即买入卖出和卖出买入
        # 但当dp1[i]和dp2[i]分别就是第i天平仓卖出和开仓买入为最优解时
        # 就相当于将一次交易拆分成了两次，并不影响最后的结果
        for i in range(1, len(lst) - 1):
            dp1[i] += dp2[i]

        return max(dp1)


## 给定一个数组，其记录了同一只股票每天的价格，同一时间最多只能保留一笔交易，
## 在不限交易次数的前提下，求所能获取的最大利润
class LeetCode122(Problem):
    def check(self, lst):
        return self.check_list_nonempty(lst)

    # 常规思路，额外地满足了，交易次数最少的情况
    def algo1(self, lst):
        maxval, minval, maxdiff = lst[0], lst[0], 0

        for i in range(1, len(lst)):
            if lst[i - 1] > lst[i]:
                maxdiff += maxval - minval
                maxval = minval = lst[i]
            else:
                maxval = lst[i]

        return maxdiff + (maxval - minval)

    def algo1_1(self, lst):
        maxdiff = 0

        for i in range(1, len(lst)):
            if lst[i - 1] < lst[i]:
                maxdiff += lst[i] - lst[i - 1]  # 贪婪

        return maxdiff


if __name__ == '__main__':
    Problem.testsuit([
        [LeetCode121, 5, [7, 1, 5, 3, 6, 4]],
        [LeetCode121, 0, [7, 6, 4, 3, 1]],
        [LeetCode122, 7, [7, 1, 5, 3, 6, 4]],
        [LeetCode122, 4, [1, 2, 3, 4, 5]],
        [LeetCode122, 0, [7, 6, 4, 3, 1]],
        [LeetCode123, 6, [3, 3, 5, 0, 0, 3, 1, 4]],
        [LeetCode123, 4, [1, 2, 3, 4, 5]],
        [LeetCode188, 7, [3, 2, 6, 5, 0, 3], 2],
        [LeetCode188, 2, [2, 4, 1], 2],
    ])
