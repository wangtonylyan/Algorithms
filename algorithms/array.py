if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))

from algorithms.utility import Problem


## LeetCode 121
## 给定序列，求lst[j]-lst[i]的最大值，要求i<=j
class Problem1(Problem):
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
        for i in lst:
            if i < minval:
                minval = i
            elif i - minval > maxdif:
                maxdif = i - minval
        return maxdif


if __name__ == '__main__':
    Problem.testsuit([
        [Problem1, 5, [7, 1, 5, 3, 6, 4]],
        [Problem1, 0, [7, 6, 4, 3, 1]],
    ])
