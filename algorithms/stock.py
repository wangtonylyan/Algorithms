if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))

from algorithms.utility import *


#########################################################################################
## 给定一个数组，其记录了同一只股票每天的价格，同一时间最多只能保留一笔交易，
## 在最多执行1次交易的前提下，求所能获取的最大利润
class LeetCode121(Problem):
    def check(self, lst):
        return self.check_list(lst)

    def solution1(self, lst):
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

    # 由上述的递归实现可见，从左至右的单次遍历中
    # 只需同时维护最大差和最小值即可
    def solution2(self, lst):
        maxdif, minval = 0, lst[0]

        for i in range(1, len(lst)):
            if lst[i] < minval:
                minval = lst[i]
            elif lst[i] - minval > maxdif:
                maxdif = lst[i] - minval

        return maxdif

    # 对于solution2，似乎还可以用移动窗口的思想来理解
    def solution3(self, lst):
        pass


## 给定一个数组，其记录了同一只股票每天的价格，同一时间最多只能保留一笔交易，
## 在不限交易次数的前提下，求所能获取的最大利润
class LeetCode122(Problem):
    def check(self, lst):
        return self.check_list(lst)

    def solution1(self, lst):
        maxval, minval, maxdiff = lst[0], lst[0], 0

        for i in range(1, len(lst)):
            if lst[i - 1] > lst[i]:
                maxdiff += maxval - minval
                maxval = minval = lst[i]
            else:
                maxval = lst[i]

        return maxdiff + (maxval - minval)


## 给定一个数组，其记录了同一只股票每天的价格，同一时间最多只能保留一笔交易，
## 在最多执行2次交易的前提下，求所能获取的最大利润
class LeetCode123(Problem):
    def check(self, lst):
        assert len(lst) > 1

    # 此算法借鉴了LeetCode121的实现思路，恰好适合于最多交易两次的情况
    def solution1(self, lst):
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

    # 考虑采用通用的三维动规解法，并结合n=2加以优化
    def solution2(self, lst):
        pass


## 给定一个数组，其记录了同一只股票每天的价格，同一时间最多只能保留一笔交易，
## 在最多执行n次交易的前提下，求所能获取的最大利润
class LeetCode188(Problem):
    def check(self, lst, n):
        assert len(lst) > 0 and n > 0

    def solution1(self, lst, n):
        m = len(lst)
        dp = [[[None, None] for _ in range(n + 1)]
              for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = [0, ninfty]
        for j in range(n + 1):
            dp[0][j] = [0, ninfty]

        for i in range(1, m + 1):  # 交易天数
            for j in range(1, n + 1):  # 最大买入次数
                dp[i][j][0] = max(dp[i - 1][j][1] + lst[i - 1],  # 卖出平仓
                                  dp[i - 1][j][0])
                dp[i][j][1] = max(dp[i - 1][j - 1][0] - lst[i - 1],  # 买入开仓
                                  dp[i - 1][j][1])

        return dp[-1][-1][0]


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
