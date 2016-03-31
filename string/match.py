# -*- coding: utf-8 -*-
# problem: string matching, string searching
# solution: brute force, Rabin-Karp, KMP
# 返回值是所有匹配子字符串的偏移量

def check_param(func):
    def f(self, s, p):
        assert (s and isinstance(s, str))
        assert (p and isinstance(p, str))
        assert (len(s) >= len(p))
        return func(self, s, p)

    return f


class BruteForce():
    @check_param
    def match(self, str, pat):
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
class RabinKarp():
    def __init__(self):
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

    @check_param
    def match(self, str, pat):
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


class Automata():
    def __init__(self):
        pass

    @check_param
    def match(self, str, pat):
        pass


if __name__ == '__main__':
    string = 'ababcabc'
    pattern = 'abc'
    bf = BruteForce()
    ret = bf.match(string, pattern)
    print ret
    rk = RabinKarp()
    assert (ret == rk.match(string, pattern))
