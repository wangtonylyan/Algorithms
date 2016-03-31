# -*- coding: utf-8 -*-


import random


# 可重叠
class LongestRepeatedSubsequence():
    def __init__(self):
        # 局限于数字以便于counting sort的实现
        self.alphabet = 10  # [0,9]

    @staticmethod
    def _longestCommonPrefix(lst1, lst2):
        for i in range(min(len(lst1), len(lst2))):
            if lst1[i] != lst2[i]:
                return i
        return min(len(lst1), len(lst2))

    def main_brute_force(self, lst):
        s = []
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                n = self._longestCommonPrefix(lst[i:], lst[j:])
                if n > len(s):
                    s = lst[i:i + n]
        return s

    def main_suffix_sort(self, lst):
        def radixSort(llst):
            for i in range(max(map(len, llst)) - 1, -1, -1):
                cnt = [0] * (self.alphabet + 1)
                for lst in llst:
                    if i < len(lst):
                        cnt[lst[i] + 1] += 1
                for j in range(len(cnt) - 1):
                    cnt[j + 1] += cnt[j]
                cpy = llst[:]
                for lst in cpy:
                    ind = lst[i] if i < len(lst) else -1
                    llst[cnt[ind]] = lst
                    cnt[ind] += 1
                assert (cnt[-1] == len(llst))

        sfx = []
        for i in range(len(lst)):
            sfx.append(lst[i:])
        radixSort(sfx)
        s = []
        for i in range(len(sfx) - 1):
            n = self._longestCommonPrefix(sfx[i], sfx[i + 1])
            if n > len(s):
                s = sfx[i][:n]
        return s

    def testcase(self):
        def test(case):
            s1 = self.main_brute_force(case)
            s2 = self.main_suffix_sort(case)
            assert (len(s1) == len(s2))

        cases = []
        for i in range(15):
            lst = [random.randint(0, 9) for i in range(random.randint(50, 100))]
            random.shuffle(lst)
            cases.append(lst)
        map(test, cases)
        print 'pass:', self.__class__


if __name__ == '__main__':
    LongestRepeatedSubsequence().testcase()
