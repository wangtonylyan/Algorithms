# -*- coding: utf-8 -*-

# because the sign bit really matters in bitwise operations
# provides two functions for casting an integer to signed or unsigned type
def signed(n): return n


def unsigned(n): return n


class SettedBitProblem():
    # @problem: set or reset a certain bit
    @staticmethod
    def setOrReset(bitmap, bit):
        bitmap |= bit  # set
        bitmap &= ~bit  # reset

    # @problem: count the number of ones in an integer's binary notation
    # @premise: n is an 8-bit unsigned integer
    @staticmethod
    def countSettedBitsNumber(n):
        assert (n <= int('11111111', 2))
        # python中&、+、>>等操作符的优先级不同于C，要加括号，不然出错
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
    def getRightmostSettedBit(n):
        return n & (~(n - 1))

    # @problem: reset the rightmost bit which is set
    # @premise: n is a non-negative integer
    @staticmethod
    def resetRightmostSettedBit(n):
        return n & (n - 1)

    # @problem: detect whether an integer is a power of 2
    # @premise: n is a non-negative integer
    @staticmethod
    def detectPowerOfTwo(n):
        # if n not equals 0 and there's only one bit set
        return n and not (n & (n - 1))

    # @problem: detect whether two signed integers have the same signs
    # @premise: n1 and n2 are of signed integer type
    @staticmethod
    def detectOppositeSigns(n1, n2):
        return ((n1 ^ n2) < 0)  # 异或的是两个整型的符号位

    def testCase(self):
        assert (self.countSettedBitsNumber(85) == 4)
        assert (self.countSettedBitsNumber(51) == 4)
        assert (self.countSettedBitsNumber(15) == 4)
        assert (self.countSettedBitsNumber(1) == 1)
        assert (self.countSettedBitsNumber(0) == 0)
        assert (self.countSettedBitsNumber(166) == 4)

        assert (self.detectOppositeSigns(1, 2) == False)
        assert (self.detectOppositeSigns(-1, -2) == False)
        assert (self.detectOppositeSigns(1, 0) == False)
        assert (self.detectOppositeSigns(-1, 0) == True)
        assert (self.detectOppositeSigns(1, -1) == True)

        print 'pass:', self.__class__


class NumberProblem():
    # @problem: compute the (ceiling or floor) middle of two integers
    # 此问题常见于二分的分治算法中
    @staticmethod
    def computeMidValue(m, n):
        assert (m <= n)
        # 1) 最简单的计算方式
        # 缺陷在于m+n的结果有可能超出其数据类型
        return (m + n) / 2
        # 2）对于方式1的不完善改进
        # 继承了方式1的缺陷，且在某些静态语言中，
        # 由于还区分有无符号，因此还应显式地进行类型转换
        return (m + n) >> 1
        # 相比于方式1，这样虽然节省了除法计算的消耗
        # 但可能会增加额外的内存分配和数据拷贝
        # 最终的实际执行效率未必会有所提高
        return (unsigned(m) + unsigned(n)) >> 1
        # 3) 较好的计算方式
        return m + (n - m) / 2  # floor
        return n - (n - m) / 2  # ceiling
        # 视数据类型中是否区分有无符号而定
        return m + ((n - m) >> 1)
        return n - ((n - m) >> 1)
        # 4) 更好的计算方式
        # http://locklessinc.com/articles/binary_search/
        return (m & n) + (m ^ n) / 2

    # @problem: compute the absolute value of an integer
    # @premise: n is a 32-bit signed integer
    @staticmethod
    def computeAbsoluteValue(n):
        # 1)
        abs1 = n if n >= 0 else -unsigned(n)  # this even works on a non-2s-compliment machine
        # 2)
        mask = n >> 31
        abs2 = (n + mask) ^ mask
        # 3)
        mask = n >> 31
        abs3 = (n ^ mask) - mask
        return (abs1, abs2, abs3)

    # @problem: swap two integers without temporary space
    @staticmethod
    def swap(n1, n2):
        def f1(n1, n2):
            n1 += n2
            n2 = n1 - n2
            n1 = n1 - n2
            return (n1, n2)

        def f2(n1, n2):
            n1 -= n2
            n2 += n1
            n1 = n2 - n1
            return (n1, n2)

        def f3(n1, n2):
            if n1 != n2:  # the XOR logic will fail
                n1 ^= n2
                n2 ^= n1
                n1 ^= n2
            return (n1, n2)

        return (f1(n1, n2), f2(n1, n2), f3(n1, n2))

    # @problem: compute modulus division by a power of 2
    # @premise: d is a power of 2
    @staticmethod
    def modulusByPowerOfTwo(n, d):
        assert (d > 1 and d & (d - 1) == 0)  # d is a power of 2
        return n & (d - 1)

    # @problem: find a power of two greater than or equal to a number
    # @premise: n is a 16-bit number
    @staticmethod
    def nextHighestPowerOfTwo(n):
        # 思路就是将二进制n的最高有效位置为0，随后将其右边的比特位全部置为1
        # 最后再加上1即可，此处的优化思路同完全背包中的第一种解法
        n -= 1
        # 通过或运算将每次位移的结果都"累积"了起来，最终的结果就等同于进行了15次位移
        n |= n >> 1  # n>>0 | n>>1
        n |= n >> 2  # (n>>0)>>2 | (n>>1)>>2
        n |= n >> 4  # (n>>0)>>4 | (n>>1)>>4 | (n>>0>>2)>>4 | (n>>1>>2)>>4
        n |= n >> 8
        n += 1
        return n

    def testCase(self):
        assert (self.computeAbsoluteValue(1) == (1, 1, 1))
        assert (self.computeAbsoluteValue(-1) == (1, 1, 1))
        assert (self.computeAbsoluteValue(0) == (0, 0, 0))

        assert (self.swap(1, 2) == ((2, 1), (2, 1), (2, 1)))
        assert (self.swap(-1, -2) == ((-2, -1), (-2, -1), (-2, -1)))
        assert (self.swap(1, 0) == ((0, 1), (0, 1), (0, 1)))
        assert (self.swap(-1, 0) == ((0, -1), (0, -1), (0, -1)))
        assert (self.swap(-1, 1) == ((1, -1), (1, -1), (1, -1)))

        assert (self.modulusByPowerOfTwo(15, 2) == 1)
        assert (self.modulusByPowerOfTwo(16, 4) == 0)
        assert (self.modulusByPowerOfTwo(18, 8) == 2)

        print 'pass', self.__class__


if __name__ == '__main__':
    SettedBitProblem().testCase()
    NumberProblem().testCase()
