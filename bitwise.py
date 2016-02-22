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
        # python中&、+、>>等操作符的优先级不同于C，要加括号，不然出错
        n = (n & 85) + ((n >> 1) & 85)  # 85=01010101
        n = (n & 51) + ((n >> 2) & 51)  # 51=00110011
        n = (n & 15) + ((n >> 4) & 15)  # 15=00001111
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


class NumberProblem():
    # @problem: compute the mid of two integers
    # 此问题常见于二分的分治算法中
    @staticmethod
    def computeMidValue(m, n):
        assert (m <= n)
        # 1) 最简单的计算方式
        return (m + n) / 2
        # 方式1的不完善改进
        # 当m+n的值超出其数据类型时，就会导致错误
        return (m + n) >> 1
        # 2) 将m和n强制类型转换成无符号整型
        # 这样虽然节省了除法计算的消耗
        # 但可能会增加额外的内存分配和数据拷贝
        # 最终的实际执行效率未必会有所提高
        return (unsigned(m) + unsigned(n)) >> 1
        # 3) 最有效的计算方式
        return m + (n - m) / 2
        return m + ((n - m) >> 1)

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


if __name__ == '__main__':
    sbp = SettedBitProblem()
    sbp.testCase()
    np = NumberProblem()
    np.testCase()
