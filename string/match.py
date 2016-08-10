# -*- coding: utf-8 -*-
# problem: string matching, string searching
# solution: brute force, Rabin-Karp, KMP
# 返回值是所有匹配子字符串的偏移量

import random, re
from string import String


class StringMatch(String):
    def __init__(self):
        super(StringMatch, self).__init__()
        self.funcs = [
            self.main_brute_force,
            # self.main_automata,
        ]

    def testcase(self):
        def test(case):
            s, p = case
            ret = s.find(p)
            assert (all(f(s, p)[0] == ret for f in self.funcs))

        cases = []
        for i in range(100):
            s = ''
            for j in range(500):
                s += chr(random.randint(ord('a'), ord('z')))
            patlen = random.randint(1, len(s))
            start = random.randint(0, len(s) - patlen)
            assert (start + patlen <= len(s))
            p = s[start:start + patlen]
            assert (len(s) >= len(p) and s.find(p) != -1)
            cases.append((s, p))
        self._testcase(test, cases)

    def main_brute_force(self, str, pat):
        ret = []
        # search
        for i in range(len(str) - len(pat) + 1):
            j = 0
            while j < len(pat) and str[i + j] == pat[j]:
                j += 1
            if j == len(pat):
                ret.append(i)
        return ret

    def preprocess(self, str):
        tab = [0] * len(str)
        left, right = 0, 0  # [left,right) is a prefix of str
        # @invariant: 'right' index is the farthest to the right
        # 目的是为了在从左至右的遍历顺序下，尽可能多地预知右边仍未被访问到的字符
        # 简而言之'right'越远/右，tab的可复用几率就越高
        for i in range(1, len(str)):
            assert (left < i and left <= right)
            if i < right:
                assert (str[i:right] == str[i - left:right - left])
                assert (str[right] != str[right - left])
                if right - i > tab[i - left]:
                    assert (str[i + tab[i - left]] == str[i - left + tab[i - left]] != tab[i - left])
                    tab[i] = tab[i - left]
                    continue
                else:
                    j = tab[i - left]
            else:
                j = 0

            while j < len(str) - i and str[j] == str[i + j]:
                j += 1
            tab[i] = j
            left, right = i, i + j

        return tab


# 该算法的设计思想，就是利用哈希在暴力算法的基础上先进行一轮筛选
# 从第一个字符起，对目标字符串中每个与模式字符串长度相同的连续子字符进行哈希
# 通过比较每个子字符串与模式字符串的哈希值，以判断是否需要逐个字符地比较
# 这就对哈希算法提出了两点要求：
# 令m为模式字符串长度，d为字符集大小，s为目标字符串
# (a) 哈希算法本身必须是高效的，不然还不如暴力算法
# hash(s[i:i+m]) = s[i]*d^(m-1) + ... + s[i+j]*d^(m-1-j) + ... + s[i+m-1]*d^0
# 采用字符串哈希算法中的第三种：hash.StringHash.hash_3()
# (b) 对于每个子字符串的哈希值的计算，应避免遍历整个子字符串
# 通过前后两个相邻子字符串之间哈希值的递推关系式
# hash(s[i+1:i+1+m]) = (hash(s[i:i+m]) - s[i]*d^(m-1))*d + s[i+m]
class RabinKarp(StringMatch):
    def __init__(self):
        super(RabinKarp, self).__init__()
        self.funcs.append(self.main)
        self.alphabet = 128  # 7-bit ASCII
        self.prime = 6999997

    def hash(self, str, strLen):
        assert (strLen <= len(str))
        # prepare
        factor = 1  # == d^(m-1)
        for i in range(1, strLen):
            factor = (factor * self.alphabet) % self.prime
        assert (factor == pow(self.alphabet, strLen - 1) % self.prime)
        # caculate hash value of the first strLen-length substring in str
        ret = 0
        for c in str[:strLen]:
            ret = (self.alphabet * ret + ord(c)) % self.prime
        yield ret
        # calculate hash value of the i-th strLen-length substring in str
        for i in range(1, len(str) - strLen + 1):
            ret = (self.alphabet * (ret - ord(str[i - 1]) * factor) + ord(str[i + strLen - 1])) % self.prime
            yield ret

    def main(self, str, pat):
        ret = []
        # step1) preprocess
        pHash = self.hash(pat, len(pat)).next()
        sHashFunc = self.hash(str, len(pat))
        # step2) search
        for i in range(0, len(str) - len(pat) + 1):
            if pHash == sHashFunc.next():  # spurious hit
                if str[i:i + len(pat)] == pat:
                    ret.append(i)
        return ret


class PatternWithWildcard():
    def main(self, str, pat):
        for i in range(len(str)):
            j = 0
            stk = []
            while True:
                if j >= len(pat) or (j == len(pat) - 1 and pat[j] == '*'):
                    return True
                elif i >= len(str):  # backtracking
                    if len(stk) > 0:
                        i, j = stk[-1]
                        i += 1
                        if i >= len(str):
                            stk.pop()
                        else:
                            stk[-1] = (i, j)
                    else:
                        break
                elif pat[j] == '*':
                    j += 1
                    stk.append((i, j))
                elif str[i] == pat[j]:
                    i += 1
                    j += 1
                else:
                    i = len(str)

        return False

    def testcase(self):
        def test(case):
            assert (self.main(case[0], case[1]) == True if re.search(case[1], case[0]) else False)

        cases = [('cabccbbcbacab', 'ab*ba*c'),
                 ('abcabcabcde', 'abcd'),
                 ]
        map(test, cases)
        print 'pass:', self.__class__


if __name__ == '__main__':
    StringMatch().testcase()
    PatternWithWildcard().testcase()

    s = StringMatch()
    assert (s.preprocess('aabaabcaxaabaabcy')[9] == 7)
    assert (s.preprocess('aabcaabxaaz')[4:9] == [3, 1, 0, 0, 2])
    print 'done'
