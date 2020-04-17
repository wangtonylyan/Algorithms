# -*- coding: utf-8 -*-
# algorithm: hash
# hash value is in range of 32-bit
# 为什么哈希算法中经常需要对质数进行取余运算？可参考如下：
# https://segmentfault.com/q/1010000000593741
# http://www.myexception.cn/arithmetic/1954979.html


# @param: integer
class IntegerHash():
    def __init__(self):
        pass

    # 1）取余哈希法
    def hash_1(self, int):
        val = int % 16
        return val & 0xFFFFFFFF

    # 2）平方哈希法
    def hash_2(self, int):
        val = (int * int) >> 28
        return val & 0xFFFFFFFF

    # 3）Fibonacci哈希法，由平方哈希法演化而来，乘以的不是自身而是一个与黄金分割有关的“理想数”
    def hash_3(self, int):
        val = (int * 2654435769) >> 28  # 32位理想数就是2654435769
        return val & 0xFFFFFFFF


# @param: string
# A one-way hash is a an algorithm that is constructed in such a way
# that deriving the original string (set of strings, actually) is virtually impossible
class StringHash():
    def __init__(self):
        # hash_3:
        # 字符集大小，也即该字符集中的字符所占据的数值上限
        self.alphabet = 128  # 7-bit ASCII
        # (a) 为避免由于字符串过长或字符集过大
        # 从而导致所得哈希值过大，超出数据类型
        # 应将所有哈希值都对该质数进行取余
        # (b) 该质数越大将则哈希冲突的可能性越小
        # 综上，最合理的质数应满足：
        # 其与字符集大小的乘积接近且小于计算机字长
        self.prime = 6999997  # 32-bit word

        # hash_4: 查表法，只需初始化一次
        self.cryptTable = [0 for i in range(0x500)]
        seed = 0x00100001
        for i in range(0x100):
            index = i
            for j in range(5):
                seed = (seed * 125 + 3) % 0x2AAAAB
                temp1 = (seed & 0xFFFF) << 0x10
                seed = (seed * 125 + 3) % 0x2AAAAB
                temp2 = seed & 0xFFFF
                self.cryptTable[index] = (temp1 | temp2) & 0xFFFFFFFF
                index += 0x100

    # 此算法仅仅是可以用，但分布不均，造成大量冲突
    def hash_1(self, str):
        val = 0xF1E2D3C4
        for c in str:
            val <<= 1
            val += ord(c)
            val &= 0xFFFFFFFF
        return val

    # 此算法得到的hash值分布比较均匀
    def hash_2(self, str):
        val = 0
        for c in str:
            val += (val << 5) + ord(c)
            val &= 0xFFFFFFFF
        return val

    # 令m为输入字符串长度，d为字符集大小
    # hash(s) = s[0]*d^(m-1) + ... + s[k]*d^(m-1-k) + ... + s[m-1]*d^0
    # 该算法可理解为：以d为进制
    # 并将s中的每个字符(在字符集中)所被标识的数值作为d进制数的一个数位
    # 最终得到的哈希值就是一个“d进制”数
    def hash_3(self, str):
        val = 0
        for c in str:
            val = (val * self.alphabet + ord(c)) % self.prime
        return val  # 取余就已保证了哈希值不会大于32位

    # the algorithm used in MPQ format file designed by Blizzard
    # http://sfsrealm.hopto.org/inside_mopaq/
    # 此算法速度快，分布均匀
    # @type = [0,1,2]，同一个字符串根据不同的type可以得出三个不同的hash值
    def hash_4(self, str, type=0):
        val = 0x7FED7FED
        seed = 0xEEEEEEEE
        str = str.upper()
        for c in str:
            val = self.cryptTable[(type << 8) + ord(c)] ^ (val + seed)
            val &= 0xFFFFFFFF
            seed += ord(c) + val + (seed << 5) + 3
        return val


if __name__ == '__main__':
    s1 = 'arr\\units.dat'
    s2 = 'unit\\neutral\\acritter.grp'
    sh = StringHash()
    assert (sh.hash_1(s1) == 0x5a858026)
    assert (sh.hash_1(s2) == 0x694CD020)
    assert (sh.hash_4(s1) == 0xF4E6C69D)
    assert (sh.hash_4(s2) == 0xA26067F3)
