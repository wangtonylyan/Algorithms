# -*- coding: utf-8 -*-
# problem: substring search
# solution: KMP

string = "abcababcabababc";
pattern = "abababc";


def kmp_by_jmp():
    # 1)generate jump array
    # jmp[i]等于使得pattern[0:k]==pattern[i-k:i]成立的最大k值
    jmp = [0]
    for i in range(1, len(pattern)):  # index of pattern and jmp
        if jmp[i - 1] < i - 1 and pattern[jmp[i - 1]] == pattern[i - 1]:
            jmp.append(jmp[i - 1] + 1)
        else:
            jmp.append(0)
    # 2)optimize jump array
    for i in range(1, len(pattern)):
        j = jmp[i]
        while j > 0 and pattern[j] == pattern[i]:
            j = jmp[j]
        jmp[i] = j
    # 3)search substring
    i = 0  # index of string
    j = 0  # index of pattern
    while True:
        if j == len(pattern):
            return i - j
        elif i == len(string):
            return i
        if string[i] == pattern[j]:
            i += 1
            j += 1
        elif j == 0:
            i += 1
        else:
            j = jmp[j]


def kmp_by_dfa():
    alph = ['a', 'b', 'c', 'd']
    dfa = [[0 for col in range(len(pattern))] for row in range(len(alph))]
    # 1)generate dfa
    # 2)search substring
    i = 0  # index of string
    j = 0  # index of pattern
    while True:
        if j == len(pattern):
            return i - j
        elif i == len(string):
            return i
        if string[i] == pattern[j]:
            j += 1
        elif j != 0:
            j = dfa[string[i]]
        i += 1  # always increasing


if __name__ == '__main__':
    print kmp_by_jmp()
    print 'done'
