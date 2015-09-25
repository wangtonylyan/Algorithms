# -*- coding: utf-8 -*-

# @premise: n is an 8-bit unsigned integer
def count(n):
    # python中&、+、>>等操作符的优先级不同于C，要加括号，不然出错
    # 85=01010101
    n = (n & 85) + ((n >> 1) & 85)
    # 51=00110011
    n = (n & 51) + ((n >> 2) & 51)
    # 15=00001111
    n = (n & 15) + ((n >> 4) & 15)
    return n


if __name__ == '__main__':
    print count(85)
    print count(51)
    print count(15)
    print count(1)
    print count(0)
    print count(166)  # 4
    print 'done'
