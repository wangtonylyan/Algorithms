# -*- coding: utf-8 -*-

import math
import heapq


# @problem: fib(n) = fib(n-1) + fib(n-2)
class Fibonacci():
    def main_iter(self, n):
        assert (n >= 0)
        if n < 2:
            return n
        i, j = 0, 1  # fib(0), fib(1)
        t = 1
        while t < n:
            i, j = j, i + j
            t += 1
        return j

    def main_recur(self, n):
        assert (n >= 0)

        def recur(n):
            if n < 2:
                return n
            return recur(n - 1) + recur(n - 2)

        return recur(n)

    def testcase(self):
        for n in range(30):
            assert (self.main_iter(n) == self.main_recur(n))
        print 'pass:', self.__class__


# @problem: adds two numbers without using + or any arithmetic operators
class SumWithoutAdd():
    def main_1(self, n1, n2):
        sum = 0
        carry = False
        mask = 1

        while mask <= n1 and mask <= n2:
            bit1 = mask & n1
            bit2 = mask & n2
            if bit1 == bit2 == 0:
                if carry:
                    sum |= mask
                    carry = False
            elif bit1 == bit2 > 0:
                if carry:
                    sum |= mask
                else:
                    carry = True
            elif not carry:
                sum |= mask
            mask <<= 1

        while mask <= n1:
            bit1 = mask & n1
            if (bit1 > 0 and not carry) or (bit1 == 0 and carry):
                sum |= mask
                carry = False
            mask <<= 1

        while mask <= n2:
            bit2 = mask & n2
            if (bit2 > 0 and not carry) or (bit2 == 0 and carry):
                sum |= mask
                carry = False
            mask <<= 1

        if carry:
            sum |= mask

        return sum

    # split apart the "addition" and "carry" operations
    def main_2(self, n1, n2):
        def recur(n1, n2):
            if n2 == 0:  # recurse until nothing to carry
                return n1
            add = (n1 ^ n2)  # add only
            cry = (n1 & n2) << 1  # carry only
            return recur(add, cry)

        return recur(n1, n2)

    def testcase(self):
        for i in range(500):
            for j in range(500):
                assert (self.main_1(i, j) == self.main_2(i, j) == i + j)
        print 'pass:', self.__class__


# @problem: find the kth number such that the only prime factors are 3, 5, and 7
class KthMagicNumber():
    def main(self, k):
        assert (k >= 0)

        magic = []
        que3 = [1 * 3]
        que5 = [1 * 5]
        que7 = [1 * 7]

        while len(magic) <= k:
            m = min(que3[0], que5[0], que7[0])
            magic.append(m)
            if m == que3[0]:
                heapq.heapreplace(que3, m * 3)
                heapq.heappush(que5, m * 5)
                heapq.heappush(que7, m * 7)
            elif m == que5[0]:
                heapq.heapreplace(que5, m * 5)
                heapq.heappush(que7, m * 7)
            elif m == que7[0]:
                heapq.heapreplace(que7, m * 7)

        return magic[-1]

    def testcase(self):
        num = 1000
        pow = int(round(math.pow(num, 1.0 / 3)))  # 3次方根
        lst = []
        for a in range(pow << 4):
            for b in range(pow << 2):
                for c in range(pow << 1):
                    lst.append((3 ** a) * (5 ** b) * (7 ** c))
        lst.sort()
        assert (len(lst) >= num)

        for i in range(num):
            assert (self.main(i) == lst[i + 1])

        print 'pass:', self.__class__


if __name__ == '__main__':
    Fibonacci().testcase()
    SumWithoutAdd().testcase()
    KthMagicNumber().testcase()
