# -*- coding: utf-8 -*-
# problem: string sorting
# solution: LSD, MSD

import random

# algorithm: least-significant-digit-first string sort
# fixed length string
class LSD():
    @staticmethod
    def sort(lst, width):
        alphabet = 256  # number of legal characters by ASCII
        aux = [[] for s in lst]  # auxiliary list stores result in each loop
        # 每次循环都是根据某一位的一次完整排序，且利用到了该排序的稳定性
        for w in range(width - 1, -1, -1):  # traverse string from least significant digit
            count = [0 for i in range(alphabet)]
            # 1) compute frequency counts
            for s in lst:
                count[ord(s[w])] += 1  # 默认alphabet的计数从0开始
            # 2) transfrom counts to indices
            for i in range(1, len(count)):
                count[i] += count[i - 1]
            # 3) distribute the records from lst to aux
            for s in lst:
                aux[count[ord(s[w]) - 1]] = s
                count[ord(s[w]) - 1] += 1
            # 4) store result into lst by exchanging lst with aux reference
            lst, aux = aux, lst
        return lst

    @staticmethod
    def testcase():
        width = 7  # length of input strings
        sample = ['1ICK750', '1ICK750', '1OHV845', '1OHV845', '1OHV845',
                  '2IYE230', '2RLA629', '2RLA629', '3ATW723', '3CIO720',
                  '3CIO720', '4JZY524', '4PGC938']  # sorted
        for i in range(10):
            case = sample[:]
            random.shuffle(case)
            assert (LSD.sort(case, width) == sample)


if __name__ == '__main__':
    LSD.testcase()
