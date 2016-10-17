# -*- coding: utf-8 -*-

import math


# because the sign bit really matters in bitwise operations
# provides two functions for casting an integer to signed or unsigned type
def signed(n): return n


def unsigned(n): return n


class BitAlgorithm():
    # @problem: set a certain bit
    @staticmethod
    def setBit(bitmap, bitmask):
        return bitmap | bitmask

    # @problem: reset a certain bit
    @staticmethod
    def resetBit(bitmap, bitmask):
        return bitmap & (~bitmask)

    # @problem: count the number of ones in an integer's binary notation
    # @premise: n is an 8-bit unsigned integer
    @staticmethod
    def countSetBits(n):
        assert (n <= int('1' * 8, 2))
        # python中&、+、>>等操作符的优先级不同于C，需要使用额外的括号
        mask = int('01010101', 2)
        n = (n & mask) + ((n >> 1) & mask)
        mask = int('00110011', 2)
        n = (n & mask) + ((n >> 2) & mask)
        mask = int('00001111', 2)
        n = (n & mask) + ((n >> 4) & mask)
        return n

    # @problem: get the rightmost bit which is set
    # @premise: n is a non-negative integer
    @staticmethod
    def getRightmostSetBit(n):
        return n & (~(n - 1))

    # @problem: reset the rightmost bit which is set
    # @premise: n is a non-negative integer
    @staticmethod
    def resetRightmostSetBit(n):
        return n & (n - 1)

    # @problem: detect whether two signed integers have the same signs
    # @premise: n1 and n2 are of signed integer type
    @staticmethod
    def detectOppositeSigns(n1, n2):
        return (n1 ^ n2) < 0  # 关注的是两个数的符号位异或后的结果

    def testcase(self):
        assert (self.countSetBits(85) == 4)
        assert (self.countSetBits(51) == 4)
        assert (self.countSetBits(15) == 4)
        assert (self.countSetBits(1) == 1)
        assert (self.countSetBits(0) == 0)
        assert (self.countSetBits(166) == 4)

        assert (self.detectOppositeSigns(1, 2) is False)
        assert (self.detectOppositeSigns(-1, -2) is False)
        assert (self.detectOppositeSigns(1, 0) is False)
        assert (self.detectOppositeSigns(-1, 0) is True)
        assert (self.detectOppositeSigns(1, -1) is True)

        print 'pass:', self.__class__


class NumberAlgorithm():
    # @problem: detect whether an integer is a power of 2
    # @premise: n is a non-negative integer
    @staticmethod
    def detectPowerOfTwo(n):
        # if n not equals 0 and there's only one bit set
        return n != 0 and (n & (n - 1)) == 0

    # @problem: get the (ceiling or floor) middle of two integers
    @staticmethod
    def getMiddleValue(n1, n2):
        assert (n1 <= n2)
        # 1) 最好的算法
        # http://locklessinc.com/articles/binary_search/
        return (n1 & n2) + (n1 ^ n2) / 2
        # 2) 改进的算法
        # floor
        return n1 + (n2 - n1) / 2
        return n1 + ((unsigned(n2) - unsigned(n1)) >> 1)
        # ceiling
        return n2 - (n2 - n1) / 2
        return n2 - ((unsigned(n2) - unsigned(n1)) >> 1)
        # 3) 最直接的算法
        # @drawback: 两数之和可能超出其数据类型所能表示的范围
        return (n1 + n2) / 2
        # @drawback: 对于区分有无符号的静态类型语言，缺少显式的类型转换
        return (n1 + n2) >> 1
        # @drawback: 引入额外的内存分配和数据拷贝
        return (unsigned(n1) + unsigned(n2)) >> 1

    # @problem: get the absolute value of an integer
    # @premise: n is a 32-bit signed integer
    @staticmethod
    def getAbsoluteValue(n):
        assert (n <= int('1' * 32, 2))
        return (n + (n >> 31)) ^ (n >> 31)
        return (n ^ (n >> 31)) - (n >> 31)
        return n if n >= 0 else -unsigned(n)  # this even works on a non-2s-compliment machine

    # @problem: swap two integers without temporary space
    @staticmethod
    def swapTwoNumbers(n1, n2):
        # 1)
        if n1 != n2:  # otherwise the XOR logic will fail
            n1 ^= n2
            n2 ^= n1
            n1 ^= n2
        return (n1, n2)
        # 2)
        n1 += n2
        n2 = n1 - n2
        n1 = n1 - n2
        return (n1, n2)
        # 3)
        n1 -= n2
        n2 += n1
        n1 = n2 - n1
        return (n1, n2)

    # @problem: compute modulus division by a power of 2
    # @premise: d is a power of 2
    @staticmethod
    def getModulusByPowerOfTwo(n, d):
        assert (d > 1 and d & (d - 1) == 0)  # d is a power of 2
        return n & (d - 1)

    # @problem: find a power of two greater than or equal to a number
    # @premise: n is a 16-bit number
    @staticmethod
    def getNextPowerOfTwo(n):
        assert (n <= int('11111111', 2))
        # 思路就是将二进制n的最高有效位置为0，随后将其右边的比特位全部置为1
        # 最后再加上1即可，此处的优化思路同完全背包中的第一种解法
        n -= 1
        # 通过或运算将每次位移的结果都"累积"了起来，最终的结果就等同于进行了15次位移
        n |= n >> 1  # n>>0 | n>>1
        n |= n >> 2  # (n>>0)>>2 | (n>>1)>>2
        n |= n >> 4  # (n>>0)>>4 | (n>>1)>>4 | (n>>0>>2)>>4 | (n>>1>>2)>>4
        n |= n >> 8
        n += 1
        assert (n == 1 << int(math.ceil(math.log(n, 2))))
        return n

    def testcase(self):
        assert (self.getAbsoluteValue(1) == 1)
        assert (self.getAbsoluteValue(-1) == 1)
        assert (self.getAbsoluteValue(0) == 0)

        assert (self.swapTwoNumbers(1, 2) == (2, 1))
        assert (self.swapTwoNumbers(-1, -2) == (-2, -1))
        assert (self.swapTwoNumbers(1, 0) == (0, 1))
        assert (self.swapTwoNumbers(-1, 0) == (0, -1))
        assert (self.swapTwoNumbers(-1, 1) == (1, -1))

        assert (self.getModulusByPowerOfTwo(15, 2) == 1)
        assert (self.getModulusByPowerOfTwo(16, 4) == 0)
        assert (self.getModulusByPowerOfTwo(18, 8) == 2)

        print 'pass', self.__class__


if __name__ == '__main__':
    BitAlgorithm().testcase()
    NumberAlgorithm().testcase()
    print 'done'
