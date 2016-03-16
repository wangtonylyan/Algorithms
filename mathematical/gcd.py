# -*- coding: utf-8 -*-
# problem: greatest common divisor

def Euclidean(a, b):
    x, y = max(a, b), min(a, b)
    while y != 0:
        x, y = y, x % y
    return x


if __name__ == '__main__':
    assert (Euclidean(1, 3) == 1)
    assert (Euclidean(10, 20) == 10)
    assert (Euclidean(13, 7) == 1)
    assert (Euclidean(945, 2415) == 105)
    print 'done'
