# -*- coding: utf-8 -*-
# problem: string matching, string searching
# solution: brute force, Rabin-Karp, KMP
# 返回值是所有匹配子字符串的偏移量

import random
import re


class StringMatch(object):
    def __init__(self):
        self.funcs = []

    def testcase(self):
        def test(func):
            assert (s.find(p) == func(s, p)[0])

        for i in range(100):
            s = ''
            for j in range(500):
                s += chr(random.randint(ord('a'), ord('z')))
            patlen = random.randint(1, len(s))
            start = random.randint(0, len(s) - patlen)
            assert (start + patlen <= len(s))
            p = s[start:start + patlen]
            assert (len(s) >= len(p) and s.find(p) != -1)
            map(test, self.funcs)
        print 'pass:', self.__class__


class BruteForce(StringMatch):
    def __init__(self):
        super(BruteForce, self).__init__()
        self.funcs.append(self.main)

    def main(self, str, pat):
        ret = []
        # search
        for i in range(0, len(str) - len(pat) + 1):
            assert (i + len(pat) <= len(str))
            j = 0
            while j < len(pat) and str[i + j] == pat[j]:
                j += 1
            if j == len(pat):
                ret.append(i)
        return ret


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


class Automata(StringMatch):
    def __init__(self):
        super(Automata, self).__init__()
        self.funcs.append(self.main)

    def main(self, str, pat):
        return [str.find(pat)]


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
            if re.search(case[1], case[0]):
                assert (self.main(case[0], case[1]) == True)
            else:
                assert (self.main(case[0], case[1]) == False)

        cases = [('cabccbbcbacab', 'ab*ba*c'),
                 ('abcabcabcde', 'abcd'),
                 ]
        map(test, cases)
        print 'pass:', self.__class__


if __name__ == '__main__':
    BruteForce().testcase()
    RabinKarp().testcase()
    Automata().testcase()
    PatternWithWildcard().testcase()
    print 'done'
