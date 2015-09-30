# -*- coding: utf-8 -*-


# @problem: count the number of ones in an interger's binary notation
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


def func(n):
    bitmap = 85

    # 1) get the rightmost bit which is set
    bit = bitmap & (~(bitmap - 1))
    bitmap &= (bitmap - 1)  # reset the rightmost bit which is set

    # 2) set and reset a certain bit
    bitmap |= bit
    bitmap &= ~bit


if __name__ == '__main__':
    countOnesInBinaryTestCase()
