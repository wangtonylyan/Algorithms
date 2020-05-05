if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))

from algorithms.utility import *


## 给定一个十进制数字，判断其是否为回文数
class LeetCode9(Problem):
    def solution1(self, n):
        if n < 0:
            return False
        if n != 0 and n % 10 == 0:
            return False

        rev = 0
        while n > rev:
            rev = rev * 10 + n % 10
            n //= 10

        return n == rev or n == rev // 10

    def solution2(self, n):
        # 回文数 == 整个字符串都是回文
        return str(n) == str(n)[::-1]


## 给定一个字符串，求其中的最长回文子串
class LeetCode5(Problem):
    def check(self, lst):
        return self.check_list(lst)

    # 根据回文的特点，寻找中心，并向两侧扩散
    def solution1(self, lst):
        if len(lst) < 2 or lst == lst[::-1]:
            return lst

        start, end, i = 0, 0, 0

        while i < len(lst):
            j = i
            while j + 1 < len(lst) and lst[j] == lst[j + 1]:
                # 由于是从左至右遍历字符串，因此只需考虑向后扩张的情况
                j += 1

            # 由于连续的相同字符只能作为回文的中心，因此下一次循环可以跳过整个当前中心
            k = j

            while i - 1 >= 0 and j + 1 < len(lst) and lst[i - 1] == lst[j + 1]:
                i, j = i - 1, j + 1

            if j - i > end - start:
                start, end = i, j

            i = k + 1

        return lst[start:end + 1]


if __name__ == "__main__":
    Problem.testsuit([
        [LeetCode5, 'b', 'bace'],
        [LeetCode5, 'bab', 'babad'],
        [LeetCode5, 'anana', 'bananas'],
        [LeetCode5, 'aaaaa', 'daaaaa'],
        [LeetCode9, True, 1],
        [LeetCode9, True, 121],
        [LeetCode9, False, -121],
    ])
