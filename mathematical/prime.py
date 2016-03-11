# -*- coding: utf-8 -*-


def Sieve_of_Eratosthenes(num):
    lst = [1 for i in range(num + 1)]
    for i in range(2, len(lst) / 2 + 1):
        if lst[i] == 1:
            j = i
            while i * j < len(lst):
                lst[i * j] = 0
                j += 1
    ret = []
    for i in range(2, len(lst)):
        if lst[i] == 1:
            ret.append(i)
    return ret


if __name__ == '__main__':
    print Sieve_of_Eratosthenes(100)
