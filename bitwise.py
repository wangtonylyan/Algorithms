# -*- coding: utf-8 -*-

#the sign bit really matters in bitwise operations

#cast an integet to signed or unsigned type
def signed(n): return n
def unsigned(n): return n


# @problem: count the number of ones in an integer's binary notation
# @premise: n is an 8-bit unsigned integer
def countOnesInBinary(n):
    # python中&、+、>>等操作符的优先级不同于C，要加括号，不然出错
    n = (n & 85) + ((n >> 1) & 85)  # 85=01010101
    n = (n & 51) + ((n >> 2) & 51)  # 51=00110011
    n = (n & 15) + ((n >> 4) & 15)  # 15=00001111
    return n


def countOnesInBinaryTestCase():
    print countOnesInBinary(85)  # 4
    print countOnesInBinary(51)  # 4
    print countOnesInBinary(15)  # 4
    print countOnesInBinary(1)  # 1
    print countOnesInBinary(0)  # 0
    print countOnesInBinary(166)  # 4


# @problem: detect whether two signed integers have the same signs
# @premise: n1 and n2 are of signed integer type
def detectIfOppositeSigns(n1, n2):
    return ((n1 ^ n2) < 0) #异或的是两个整型的符号位



# @premise: n is a non-negative integer
def theRightmostSetBit(n):
    # @problem: detect whether an integer is a power of 2
    def detectIfPowerOfTwo(n):
        #if n not equals 0 and there's only one bit set
        return n and not (n &(n-1))

    # @problem: get the rightmost bit which is set
    def getRightmostBit(n):
        return n & (~(n-1))

    # @problem: reset the rightmost bit which is set
    def resetRightmostBit(n):
        return n & (n-1)

# @problem: compute the absolute value of an integer
# @premise: n is a 32-bit signed integer
def computeAbsoluteValue(n):
    #1)
    ret = n if n >= 0 else -unsigned(n)# this even works on a non-2s-compliment machine
    #2)
    mask = n >> 31
    ret = (n + mask) ^ mask
    #3)
    ret = (n ^ mask) - mask
    return ret


def func(n):
    bitmap = 85

    # 2) set and reset a certain bit
    bitmap |= bit
    bitmap &= ~bit


if __name__ == '__main__':
#    countOnesInBinaryTestCase()

    print computeAbsoluteValue(-1)
