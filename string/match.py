# -*- coding: utf-8 -*-
# problem: string matching/searching
# solution: brute force, KMP, BM, Rabin-Karp
# 返回值是所有匹配子字符串的偏移量


import random
import re
from base.string import String, StringTest
from suffix import EnhancedSuffixArray


class StringMatch(String, StringTest):
    def __init__(self):
        super(StringMatch, self).__init__()
        self.funcs = [self.main_bruteForce, self.main]

    def main_bruteForce(self, txt, pat):
        # search
        ret = []
        for i in range(len(txt) - len(pat) + 1):
            j = 0
            while j < len(pat) and txt[i + j] == pat[j]:
                j += 1
            if j == len(pat):
                ret.append(i)
        return ret

    def main(self, txt, pat):
        assert False

    def _gencase(self, total=500):
        cases = [
            ('abcabceabcde', 'abcd'),
            ('aaababaabc', 'abc'),
            ('abcabcabcabc', 'abc'),
            ('aaaaaaaaaa', 'aaaa'),
            ('abcabceababcabcabcd', 'abcabcd'),
            ('eabcabcabc', 'eabcabcabc'),
            ('baabcaaabcaaabcaaa', 'aabcaaabca'),
            ('aabaabcaxaabaabcy', 'aabaa'),
            ('zbzzbzczbczzz', 'z'),
        ]

        for i in range(total):
            s = ''
            for j in range(total):
                s += chr(random.randint(ord('a'), ord('d')))
            patlen = random.randint(1, 20)
            assert patlen < len(s)
            start = random.randint(0, len(s) - patlen)
            assert start + patlen <= len(s)
            p = s[start:start + patlen]
            assert len(s) >= len(p) and s.find(p) != -1
            cases.append((s, p))
        return cases

    def testcase(self):
        def test(case):
            assert len(self.funcs) > 0
            ret = self.funcs[0](case[0], case[1])  # the brute-force algorithm
            assert len(ret) > 0  # necessary only for current test cases
            assert all(f(case[0], case[1]) == ret for f in self.funcs[1:])

        self._testcase(test, self._gencase())


class ZAlgorithm(StringMatch):
    def __init__(self):
        super(ZAlgorithm, self).__init__()

    def _preprocess_fundamental(self, pat):
        tab = [0] * len(pat)  # (0,-1], length
        low, high = 0, 0  # [low,high) is a prefix of 'pat'
        # @invariant: variable 'high' is the farthest index to the right
        # 目的是为了在从左至右的遍历顺序下，尽可能多地预知右边仍未被访问到的字符
        # 简而言之'high'越大，对于'tab'中已有数据的可利用率就越高
        for i in range(1, len(pat)):
            assert low < i and low <= high <= len(pat)
            if i < high:
                assert pat[i:high] == pat[i - low:high - low]
                assert high == len(pat) or pat[high] != pat[high - low]
                if high - i > tab[i - low]:
                    assert pat[i:i + tab[i - low]] == pat[i - low:i - low + tab[i - low]] == pat[:tab[i - low]]
                    assert pat[i + tab[i - low]] == pat[i - low + tab[i - low]] != pat[tab[i - low]]
                    tab[i] = tab[i - low]
                    continue
                elif high - i < tab[i - low]:
                    assert high == len(pat) or pat[high] != pat[high - i]
                    tab[i] = high - i
                    continue
                else:
                    j = high - i
            else:
                j = 0

            while j < len(pat) - i and pat[i + j] == pat[j]:
                j += 1
            tab[i] = j
            low, high = i, i + tab[i]
        return tab

    def main(self, txt, pat):
        assert '$' not in txt
        concat = pat + '$' + txt
        tab = self._preprocess_fundamental(concat)
        ret = []
        for i in range(len(pat) + 1, len(tab)):
            if tab[i] == len(pat):
                ret.append(i - (len(pat) + 1))
        return ret


class KnuthMorrisPratt(ZAlgorithm):
    def __init__(self):
        super(KnuthMorrisPratt, self).__init__()

    def _preprocess_jmp_fundamental(self, pat):
        tab = self._preprocess_fundamental(pat)  # (0,-1], length
        jmp = [0] * len(pat)  # [0,-1], length
        for i in range(len(pat) - 1, 0, -1):
            if tab[i] > 0:
                jmp[i + tab[i] - 1] = tab[i]
        return jmp

    def _preprocess_jmp_classical(self, pat):
        # jmp[i]是使得pat[0:k]==pat[i+1-k:i+1]的最大k值
        jmp = [0] * len(pat)  # [0,-1], length, but will be used as index
        i, j = 0, jmp[0]
        while i < len(pat) - 1:
            assert j <= i
            if pat[j] == pat[i + 1]:
                i += 1
                j += 1
                jmp[i] = j
            elif j > 0:
                j = jmp[j - 1]
            else:
                i += 1
                assert jmp[i] == j == 0
        return jmp

        # 以下构建'jmp'的方式更为直观
        # jmp[i]是使得pat[0:k]==pat[i-k:i]的最大k值
        jmp = [0] * (len(pat) + 1)  # (0,-1], length
        for i in range(1, len(pat)):
            j = jmp[i]
            while j > 0 and pat[j] != pat[i]:
                j = jmp[j]
            if pat[j] == pat[i]:
                jmp[i + 1] = j + 1
        return jmp[1:]  # not necessary, just for compatibility

    # deterministic finite state string matcher
    def _preprocess_jmp_realtime(self, pat):
        pass

    def main(self, txt, pat):
        # 1) preprocess
        # jmp = self._preprocess_jmp_fundamental(pat)  # worst
        jmp = self._preprocess_jmp_classical(pat)  # better
        # jmp = self._preprocess_jmp_realtime(pat)  # best
        # 2) search
        ret = []
        i, j = 0, jmp[0]
        while i < len(txt) - len(pat) + 1:
            while j < len(pat) and txt[i + j] == pat[j]:
                j += 1
            if j == 0:
                i += 1
                continue
            elif j == len(pat):
                ret.append(i)
            i += j - jmp[j - 1]
            j = jmp[j - 1]
        return ret


class BoyerMoore(ZAlgorithm):
    def __init__(self):
        super(BoyerMoore, self).__init__()

    def main_bruteForce(self, txt, pat):
        # search
        ret = []
        for i in range(len(pat) - 1, len(txt)):
            j = 0
            while j < len(pat) and txt[i - j] == pat[len(pat) - 1 - j]:
                j += 1
            if j == len(pat):
                ret.append(i - j + 1)
        return ret

    def _preprocess_fundamental_reversed(self, pat):
        tab = [0] * len(pat)  # [0,-1), length
        low, high = len(pat) - 1, len(pat) - 1
        for i in range(len(pat) - 2, -1, -1):
            assert low <= high and i < high
            if i > low:
                if i - low != tab[len(pat) - 1 - (high - i)]:
                    tab[i] = min(i - low, tab[len(pat) - 1 - (high - i)])
                    continue
                else:
                    j = len(pat) - 1 - (i - low)
            else:
                j = len(pat) - 1

            while j >= len(pat) - 1 - i and pat[i - (len(pat) - 1 - j)] == pat[j]:
                j -= 1
            tab[i] = len(pat) - 1 - j  # mismatch at 'j'
            low, high = i - tab[i], i
        assert tab == self._preprocess_fundamental(pat[::-1])[::-1]
        return tab

    def _preprocess_badCharacter(self, pat):
        bad = [[] for _ in range(self.alphabet)]  # [0,-1], index
        for i in range(len(pat) - 1, -1, -1):
            # all occurrences of 'pat[i]', rightmost first
            bad[self.ord(pat[i])].append(i)
        return bad

    def _preprocess_goodSuffix(self, pat):
        tab = self._preprocess_fundamental_reversed(pat)  # [0,-1), length
        # 'sfx'和'pfx'数组中的缺省值为-1表示不存在符合条件的前后缀
        # 此时整个'pat'可移至当前已比较过的所有'txt'字符的右边
        sfx = [-1] * len(pat)  # (0,-1], index
        for i in range(len(pat) - 1):
            assert i < tab[i] or pat[i - tab[i]] != pat[len(pat) - 1 - tab[i]]
            if tab[i] > 0:
                sfx[len(pat) - tab[i]] = i
        pfx = [-1] * len(pat)  # (0,-1], index
        if tab[0] == 1:
            pfx[len(pat) - 1] = 0
        for i in range(1, len(pat) - 1):
            pfx[len(pat) - (i + 1)] = i if tab[i] == i + 1 else pfx[len(pat) - i]
        assert all(pfx[i] + 1 <= len(pat) - i for i in range(1, len(pat)))
        return sfx, pfx

    def main(self, txt, pat):
        # 1) preprocess
        # 预处理表描述内容的方式有两种：索引值或长度值，两者没有本质上的区别，可以相互转换
        # 但其在生成和搜索过程中处理的方式会略有不同，此算法不同实现上的主要区别就在于此
        # 当前实现统一基于索引值，在pfxs的处理上可能会增加一些计算量
        bads = self._preprocess_badCharacter(pat)
        sfxs, pfxs = self._preprocess_goodSuffix(pat)
        # 2) search
        ret = []
        i = 0
        while i < len(txt) - len(pat) + 1:
            j = len(pat) - 1
            while j >= 0 and txt[i + j] == pat[j]:
                j -= 1
            if j == -1:  # find the occurrence of 'pat' in 'txt'
                ret.append(i)
                # pfxs[0]没有意义，pfxs[1]则是最长前缀(同样适用于缺省值-1)
                i += len(pat) - 1 - pfxs[1] if len(pfxs) > 1 else 1
            else:
                assert txt[i + j] != pat[j]
                # bad character shift rule
                bad = bads[self.ord(txt[i + j])]
                k = 0  # closest to the left of 'j'
                while k < len(bad) and bad[k] > j:
                    k += 1
                assert k == len(bad) or bad[k] != j
                bcShift = j - bad[k] if k < len(bad) else j + 1
                # good suffix shift rule
                if j == len(pat) - 1:
                    gsShift = 1
                elif sfxs[j + 1] >= 0:
                    gsShift = len(pat) - 1 - sfxs[j + 1]
                elif pfxs[j + 1] >= 0:  # else:
                    gsShift = len(pat) - 1 - pfxs[j + 1]
                else:  # optional else
                    gsShift = len(pat)
                # make the maximum shift
                i += max(bcShift, gsShift)
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
        self.prime = 6999997

    def _hash(self, str, strLen):
        assert strLen <= len(str)
        # 1) prepare
        factor = 1  # == d^(m-1)
        for i in range(1, strLen):
            factor = (factor * self.alphabet) % self.prime
        assert factor == pow(self.alphabet, strLen - 1) % self.prime
        # 2) caculate hash value of the first strLen-length substring in str
        ret = 0
        for c in str[:strLen]:
            ret = (self.alphabet * ret + ord(c)) % self.prime
        yield ret
        # 3) calculate hash value of the i-th strLen-length substring in str
        for i in range(1, len(str) - strLen + 1):
            ret = (self.alphabet * (ret - ord(str[i - 1]) * factor) + ord(str[i + strLen - 1])) % self.prime
            yield ret

    def main(self, txt, pat):
        # 1) preprocess
        pHash = self._hash(pat, len(pat)).next()
        sHashFunc = self._hash(txt, len(pat))
        # 2) search
        ret = []
        for i in range(0, len(txt) - len(pat) + 1):
            if pHash == sHashFunc.next():  # spurious hit
                if txt[i:i + len(pat)] == pat:
                    ret.append(i)
        return ret


class SuffixArrayBased(StringMatch):
    def __init__(self):
        super(SuffixArrayBased, self).__init__()
        obj = EnhancedSuffixArray()
        self.sfxFunc = obj.main_2
        self.lcpFunc = obj.main_lcp_Kasai

    # binary search, O(mlogn)
    def main_1(self, txt, pat):
        sfx = self.sfxFunc(txt)
        low, high = 0, len(sfx) - 1
        while low <= high:
            mid = low + (high - low) / 2
            # 比较的是pat与sfx的前缀
            if sfx[mid] + len(pat) < len(txt):
                ret = cmp(pat, txt[sfx[mid]:sfx[mid] + len(pat)])
            else:
                ret = cmp(pat, txt[sfx[mid]:])
            if ret < 0:
                high = mid - 1
            elif ret > 0:
                low = mid + 1
            else:
                return sfx[mid]
        return None

    # binary search, O(m+logn)
    def main_2(self, txt, pat):
        sfx = self.sfxFunc(txt)
        lcp = self.lcpFunc(txt, sfx)

    def testcase(self):
        def test(case):
            ret1 = self.main_1(case[0], case[1])
            # ret2 = self.main_2(case[0], case[1])
            assert 0 <= ret1 < len(case[0]) and ret1 + len(case[1]) <= len(case[0])
            # assert 0 <= ret2 < len(case[0]) and ret2 + len(case[1]) <= len(case[0])
            assert case[0][ret1:ret1 + len(case[1])] == case[1]  # == case[0][ret2:ret2 + len(case[1])]

        self._testcase(test, self._gencase(total=300))


class PatternWithWildcard():
    def main(self, txt, pat):
        for i in range(len(txt)):
            j = 0
            stk = []
            while True:
                if j >= len(pat) or (j == len(pat) - 1 and pat[j] == '*'):
                    return True
                elif i >= len(txt):  # backtracking
                    if len(stk) > 0:
                        i, j = stk[-1]
                        i += 1
                        if i >= len(txt):
                            stk.pop()
                        else:
                            stk[-1] = (i, j)
                    else:
                        break
                elif pat[j] == '*':
                    j += 1
                    stk.append((i, j))
                elif txt[i] == pat[j]:
                    i += 1
                    j += 1
                else:
                    i = len(txt)

        return False

    def testcase(self):
        def test(case):
            assert self.main(case[0], case[1]) == True if re.search(case[1], case[0]) else False

        cases = [('cabccbbcbacab', 'ab*ba*c'),
                 ('abcabcabcde', 'abcd'),
                 ]
        map(test, cases)
        print('pass:', self.__class__)


if __name__ == '__main__':
    ZAlgorithm().testcase()
    KnuthMorrisPratt().testcase()
    BoyerMoore().testcase()
    RabinKarp().testcase()
    SuffixArrayBased().testcase()

    PatternWithWildcard().testcase()
    print('done')
