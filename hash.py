# -*- coding: utf-8 -*-
# algorithm: hash

# hash value is in range of 32-bit

# @param: integer
class IntegerHash():
    def __init__(self):
        pass

    # 1)除法散列法
    def hash1(self, integer):
        hashVal = integer % 16
        return hashVal & 0xFFFFFFFF

    # 2)平方散列法
    def hash2(self, integer):
        hashVal = (integer * integer) >> 28
        return hashVal & 0xFFFFFFFF

    # 3)Fibonacci散列法，由平方散列法演化而来，乘以的不是自身而是一个与黄金分割有关的“理想数”
    def hash3(self, integer):
        hashVal = (integer * 2654435769) >> 28  # 32位理想数就是2654435769
        return hashVal & 0xFFFFFFFF


# @param: string
# A one-way hash is a an algorithm that is constructed in such a way
# that deriving the original string (set of strings, actually) is virtually impossible
class StringHash():
    def __init__(self):
        # 1)algorithm 1 initialization
        pass
        # 2)algorithm 2 initialization
        pass
        # 3)algorithm 3 initialization
        # 查表法，只需初始化一次
        self.cryptTable = self._initCryptTable()

    # 此算法仅仅是可以用，但分布不均，造成大量冲突
    def hash1(self, string):
        hashVal = 0xF1E2D3C4
        for c in string:
            hashVal <<= 1
            hashVal += ord(c)
            hashVal &= 0xFFFFFFFF
        return hashVal

    # 此算法得到的hash值分布比较均匀
    def hash2(self, string):
        hashVal = 0x00000000
        for c in string:
            hashVal += (hashVal << 5) + ord(c)
            hashVal &= 0xFFFFFFFF
        return hashVal

    # the algorithm used in MPQ format file designed by Blizzard
    # http://sfsrealm.hopto.org/inside_mopaq/
    # 此算法速度快，分布均匀
    # @type = [0,1,2]，同一个字符串根据不同的type可以得出三个不同的hash值
    def hash3(self, string, type=0):
        hashVal = 0x7FED7FED
        seed = 0xEEEEEEEE
        string = string.upper()
        for c in string:
            hashVal = self.cryptTable[(type << 8) + ord(c)] ^ (hashVal + seed)
            hashVal &= 0xFFFFFFFF
            seed += ord(c) + hashVal + (seed << 5) + 3
        return hashVal

    @staticmethod
    def _initCryptTable():
        table = [0 for i in range(0x500)]
        seed = 0x00100001
        for i in range(0x100):
            index = i
            for j in range(5):
                seed = (seed * 125 + 3) % 0x2AAAAB
                temp1 = (seed & 0xFFFF) << 0x10
                seed = (seed * 125 + 3) % 0x2AAAAB
                temp2 = seed & 0xFFFF
                table[index] = (temp1 | temp2) & 0xFFFFFFFF
                index += 0x100
        return table


if __name__ == '__main__':
    s1 = 'arr\\units.dat'
    s2 = 'unit\\neutral\\acritter.grp'
    sh = StringHash()
    assert (sh.hash1(s1) == 0x5a858026)
    assert (sh.hash1(s2) == 0x694CD020)
    assert (sh.hash3(s1) == 0xF4E6C69D)
    assert (sh.hash3(s2) == 0xA26067F3)
