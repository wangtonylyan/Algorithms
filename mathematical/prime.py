# -*- coding: utf-8 -*-

import math


def Sieve_of_Eratosthenes(num):
    lst = [1 for i in range(num + 1)]
    for i in range(3, int(math.sqrt(num) + 1), 2):
        if lst[i] == 1:
            j = i
            while i * j < len(lst):
                lst[i * j] = 0
                j += 2
    ret = [2] if num > 1 else []
    for i in range(3, len(lst), 2):
        if lst[i] == 1:
            ret.append(i)
    return ret


if __name__ == '__main__':
    print Sieve_of_Eratosthenes(100)
    print 'done'
