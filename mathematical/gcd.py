# -*- coding: utf-8 -*-
# problem: greatest common divisor

def Euclidean(a, b):
    x, y = max(a, b), min(a, b)
    while x > 0 and y > 0 and x % y != 0:
        x = x % y
        x, y = y, x
    return y


if __name__ == '__main__':
    assert (Euclidean(945, 2415) == 105)
    print 'done'
