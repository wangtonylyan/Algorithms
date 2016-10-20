# -*- coding: utf-8 -*-

import random
import math
from mathematical.bitwise import BitAlgorithm, NumberAlgorithm


# @problem: Could one design a college admissions process,
# or a job recruiting process, that was self-enforcing?
class StableMatching():
    def main_GaleShapley(self, map1, map2):
        assert (len(map1) == len(map2))
        set1 = [None] * len(map1)
        set2 = [None] * len(map2)
        while None in set1:
            for i in range(len(set1)):
                if set1[i] == None:
                    assert (len(map1[i]) > 0)
                    while len(map1[i]) > 0:
                        j = map1[i][0]
                        map1[i] = map1[i][1:]
                        if set2[j] == None:
                            set1[i], set2[j] = j, i
                            break
                        elif map2[j].index(i) < map2[j].index(set2[j]):
                            set1[set2[j]] = None
                            set1[i], set2[j] = j, i
                            break
                    break  # optional

        ret = []
        for i in range(len(set1)):
            ret.append((i, set1[i]))
        return ret

    def testcase(self):
        def test((map1, map2)):
            def check(matching):
                for i, j in matching:
                    assert (i in map2[j] and j in map1[i])
                    for k in range(map1[i].index(j)):
                        for m, n in matching:
                            if n == k:
                                break
                        assert (n == k)
                        assert (map2[k].index(m) < map2[k].index(i))

            check(self.main_GaleShapley(map1[:], map2[:]))

        cases = []
        for _ in range(100):
            lst = [i for i in range(random.randint(2, 50))]
            map1, map2 = [], []
            for _ in range(len(lst)):
                random.shuffle(lst)
                map1.append(lst[:])
                random.shuffle(lst)
                map2.append(lst[:])
            assert (len(map1) == len(map2) == len(lst) > 0)
            cases.append((map1, map2))

        map(test, cases)
        print 'pass:', self.__class__


class Josephus():
    def main_recur(self, n):
        def recur(n):
            if n == 1:
                return 1
            if n % 2 == 0:
                return 2 * recur(n / 2) - 1
            else:
                return 2 * recur(n / 2) + 1

        return recur(n)

    def main_formula(self, n):
        return 2 * (n - 2 ** int(math.log(n, 2))) + 1

    def main_bitwise(self, n):
        # get the leftmost bit
        if n == BitAlgorithm.getRightmostSetBit(n):
            m = n
        else:
            m = NumberAlgorithm.getNextPowerOfTwo(n) >> 1
            assert (m < n)
        # get rest bits except the leftmost one
        n &= m - 1
        return n << 1 | 1

    def testcase(self):
        for i in range(1, 256):
            assert (self.main_recur(i) == self.main_formula(i) == self.main_bitwise(i))


if __name__ == '__main__':
    # StableMatching().testcase()
    Josephus().testcase()
    print 'done'
