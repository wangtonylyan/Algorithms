# -*- coding: utf-8 -*-
# problem: longest increasing subsequence
# solution: dynamic programming

seq = [9, 2, 3, 4, 1, 4, 4, 3, 2, 1]
tab = [[-1 for col in range(len(seq))] for row in range(len(seq))]


def lis():
    # tab[i][j] ~ tab[i-1][j-1] or tab[i-1][j] or tab[i][j-1]
    for i in range(len(seq)):  # number of sequence
        for j in range(len(seq)):  # length of subsequence
            if i < j:
                tab[i][j] = -1
            elif j == 0:
                if i == 0 or tab[i - 1][j] > seq[i]:
                    tab[i][j] = seq[i]
                else:
                    tab[i][j] = tab[i - 1][j]
            else:
                # tab[i][j-1] <= tab[i-1][j-1] < tab[i-1][j]
                if tab[i][j - 1] == -1 or tab[i - 1][j - 1] == -1:
                    tab[i][j] = -1
                elif tab[i - 1][j] == -1:
                    if seq[i] >= tab[i - 1][j - 1]:  # not strictly increasing
                        tab[i][j] = seq[i]
                    else:
                        tab[i][j] = -1
                else:  # none of the three are nil
                    if seq[i] < tab[i - 1][j - 1] or seq[i] > tab[i - 1][j]:
                        tab[i][j] = tab[i - 1][j]
                    else:
                        tab[i][j] = seq[i]  # not strictly increasing


if __name__ == '__main__':
    lis()
    for i in range(len(seq)):
        for j in range(len(seq)):
            print tab[i][j], '\t',
        print
