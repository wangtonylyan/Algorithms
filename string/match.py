# -*- coding: utf-8 -*-
# problem: string matching, string searching
# solution: brute force, Rabin-Karp, KMP
# 返回值是所有匹配子字符串的偏移量

import random, re
from string import String


class StringMatch(String):
    def __init__(self):
        super(StringMatch, self).__init__()
        self.funcs = [self.main_bruteForce]

    def main_bruteForce(self, str, pat):
        # search
        ret = []
        for i in range(len(str) - len(pat) + 1):
            j = 0
            while j < len(pat) and str[i + j] == pat[j]:
                j += 1
            if j == len(pat):
                ret.append(i)
        return ret

    def _preprocess_bruteForce(self, pat):
        tab = [0] * len(pat)
        for i in range(1, len(pat)):
            j = 0
            while j < len(pat) - i and pat[i + j] == pat[j]:
                j += 1
            tab[i] = j  # length
        return tab

    def _preprocess_fundamental(self, pat):
        tab = [0] * len(pat)
        low, high = 0, 0  # [low,high) is a prefix of pat
        # @invariant: variable high is the farthest index to the right
        # 目的是为了在从左至右的遍历顺序下，尽可能多地预知右边仍未被访问到的字符
        # 简而言之high越右，tab可复用的几率就越高
        for i in range(1, len(pat)):
            assert (low < i and low <= high <= len(pat))
            if i < high:
                assert (pat[i:high] == pat[i - low:high - low])
                assert (high == len(pat) or pat[high] != pat[high - low])
                if high - i > tab[i - low]:
                    assert (pat[i:i + tab[i - low]] == pat[i - low:i - low + tab[i - low]] == pat[:tab[i - low]])
                    assert (pat[i + tab[i - low]] == pat[i - low + tab[i - low]] != pat[tab[i - low]])
                    tab[i] = tab[i - low]
                    continue
                else:
                    j = high - i
            else:
                j = 0

            while j < len(pat) - i and pat[i + j] == pat[j]:
                j += 1
            tab[i] = j  # length
            low, high = i, i + j
        return tab

    def testcase(self):
        def test(case):
            assert (self._preprocess_bruteForce(case[0]) == self._preprocess_fundamental(case[0]))
            assert (self._preprocess_bruteForce(case[1]) == self._preprocess_fundamental(case[1]))

            assert (len(self.funcs) > 0)
            ret = self.funcs[0](case[0], case[1])  # the brute-force algorithm
            assert (len(ret) > 0)  # only for current cases
            assert (all(f(case[0], case[1]) == ret for f in self.funcs[1:]))

        cases = [
            ('abcabceabcde', 'abcd'),
            ('aaababaabc', 'abc'),
            ('abcabcabcabc', 'abc'),
            ('aaaaaaaaaa', 'aaaa'),
            ('abcabceababcabcabcd', 'abcabcd'),
            ('eabcabcabc', 'eabcabcabc'),
            ('baabraaabraaabraaa', 'aabraaabra'),
            ('aabaabcaxaabaabcy', 'aabaa'),
            ('zbzzbzczbczzz', 'z'),
        ]

        for i in range(500):
            s = ''
            for j in range(300):
                s += chr(random.randint(ord('a'), ord('z')))
            patlen = random.randint(1, 20)
            start = random.randint(0, len(s) - patlen)
            assert (start + patlen <= len(s))
            p = s[start:start + patlen]
            assert (len(s) >= len(p) and s.find(p) != -1)
            cases.append((s, p))

        self._testcase(test, cases)


class KnuthMorrisPratt(StringMatch):
    def __init__(self):
        super(KnuthMorrisPratt, self).__init__()


class BoyerMoore(StringMatch):
    def __init__(self):
        super(BoyerMoore, self).__init__()
        self.funcs.append(self.main)

    def main_bruteForce(self, str, pat):
        # search
        ret = []
        for i in range(len(pat) - 1, len(str)):
            j = 0
            while j < len(pat) and str[i - j] == pat[len(pat) - 1 - j]:
                j += 1
            if j == len(pat):
                ret.append(i - j + 1)
        return ret

    def _preprocess_badCharacter(self, pat):
        bad = [[] for _ in range(self.alphabet)]
        for i in range(len(pat) - 1, -1, -1):
            # all occurrences of pat[i], rightmost first
            bad[ord(pat[i]) - ord('a')].append(i)  # index
        return bad

    def _preprocess_goodSuffix(self, pat):
        tab = self._preprocess_fundamental(pat[::-1])  # string reversal
        tab.reverse()  # list reversal

        sfx = [0] * len(pat)
        for i in range(len(pat) - 1):
            assert (i < tab[i] or pat[i - tab[i]] != pat[len(pat) - 1 - tab[i]])
            if tab[i] > 0:
                sfx[len(pat) - tab[i]] = i  # index

        pfx = [0] * len(pat)
        for i in range(len(pat) - 1):
            if tab[i] == i + 1:
                for j in range(len(pat) - tab[i] + 1):
                    pfx[j] = i  # index
        all(pfx[i] + 1 <= len(pat) - i for i in range(len(pfx) - 1))
        return sfx, pfx

    def main(self, str, pat):
        # 1) preprocess
        # 预处理表描述内容的方式有两种：索引值或长度值，两者没有本质上的区别，可以相互转换
        # 但其在生成和搜索过程中处理的方式会略有不同，此算法在实现上的主要区别就在于此
        # 当前实现统一基于索引值，在pfxs的处理上可能会增加一些计算量
        bads = self._preprocess_badCharacter(pat)
        sfxs, pfxs = self._preprocess_goodSuffix(pat)
        # 2) search
        ret = []
        i = 0
        while i < len(str) - len(pat) + 1:
            j = len(pat) - 1
            while j >= 0 and str[i + j] == pat[j]:
                j -= 1
            if j == -1:  # find the occurrence of pat in str
                ret.append(i)
                # as if str[i] and pat[0] mismatch
                i += len(pat) - 1 - pfxs[1] if len(pfxs) > 1 else 1
            else:
                # use the "bad character shift rule"
                assert (str[i + j] != pat[j])
                bad = bads[ord(str[i + j]) - ord('a')]
                k = 0  # closest to the left of j
                while k < len(bad) and bad[k] > j:
                    k += 1
                assert (k == len(bad) or bad[k] != j)
                bcShift = j - bad[k] if k < len(bad) else 1
                # use the "good suffix shift rule"
                if j == len(pat) - 1:
                    gsShift = 1
                elif sfxs[j + 1] > 0:
                    gsShift = len(pat) - 1 - sfxs[j + 1]
                else:
                    gsShift = len(pat) - 1 - pfxs[j + 1]
                # make the maximum shift
                i += max(bcShift, gsShift, 1)
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
        self.prime = 6999997

    def _hash(self, str, strLen):
        assert (strLen <= len(str))
        # 1) prepare
        factor = 1  # == d^(m-1)
        for i in range(1, strLen):
            factor = (factor * self.alphabet) % self.prime
        assert (factor == pow(self.alphabet, strLen - 1) % self.prime)
        # 2) caculate hash value of the first strLen-length substring in str
        ret = 0
        for c in str[:strLen]:
            ret = (self.alphabet * ret + ord(c)) % self.prime
        yield ret
        # 3) calculate hash value of the i-th strLen-length substring in str
        for i in range(1, len(str) - strLen + 1):
            ret = (self.alphabet * (ret - ord(str[i - 1]) * factor) + ord(str[i + strLen - 1])) % self.prime
            yield ret

    def main(self, str, pat):
        # 1) preprocess
        pHash = self._hash(pat, len(pat)).next()
        sHashFunc = self._hash(str, len(pat))
        # 2) search
        ret = []
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
    KnuthMorrisPratt().testcase()
    BoyerMoore().testcase()
    RabinKarp().testcase()
    PatternWithWildcard().testcase()
    print 'done'
