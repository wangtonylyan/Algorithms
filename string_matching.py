# -*- coding: utf-8 -*-
# problem: string matching
# solution: brute force, Rabin-Karp, KMP

alphabet = 256  # ASCII
prime = 127


def check_param(func):
    def f(self, string, pattern):
        assert (string and isinstance(string, str))
        assert (pattern and isinstance(pattern, str))
        assert (len(string) >= len(pattern))
        return func(self, string, pattern)

    return f


class BruteForce():
    @check_param
    def matching(self, str, pat):
        ret = []
        # searching
        for i in range(0, len(str) - len(pat) + 1):
            assert (i + len(pat) <= len(str))
            j = 0
            while j < len(pat) and str[i + j] == pat[j]:
                j += 1
            if j == len(pat):
                ret.append(i)
        return ret


class RabinKarp():
    def __init__(self):
        self.alphabet = 256  # ASCII
        self.prime = 127

    # 从第一个字符起，对str中每len(pat)个字符组成的子字符串进行哈希
    # 为了降低算法的时间复杂度，对于哈希计算有以下两点优化：
    # (a) 在searching的每次迭代中计算，而不是在preprocessing就全部计算完
    # (b) 除第一次哈希外，随后的每次哈希都将基于之前一次的结果
    def hash(self, str, subLen):
        assert (subLen <= len(str))

        iter = 1
        for i in range(1, subLen):
            iter = (iter * self.alphabet) % self.prime
        assert (iter == pow(self.alphabet, subLen - 1) % self.prime)

        ret = 0
        for c in str[:subLen]:
            ret = (self.alphabet * ret + ord(c)) % self.prime
        yield ret  # hash value of the first subLen-length substring in str
        for i in range(1, len(str) - subLen + 1):
            ret = (self.alphabet * (ret - ord(str[i]) * iter) + ord(str[i + subLen - 1])) % self.prime
            yield ret

    @check_param
    def matching(self, str, pat):
        ret = []
        # step1) preprocessing
        phash = self.hash(pat, len(pat))
        shash = self.hash(str, len(pat))
        # step2) searching
        for i in range(0, len(str) - len(pat) + 1):
            if phash == shash:
                if str[i:i + len(pat)] == pat:
                    ret.append(i)
            shash = self.hash.send(str[i + 1:i + 1 + len(pat)])
        return ret


if __name__ == '__main__':
    string = 'ababcabc'
    pattern = 'abc'
    bf = BruteForce()
    ret = bf.matching(string, pattern)
    print ret
    rk = RabinKarp()
    #    ret == rk.matching(string, pattern)
    #    print ret
