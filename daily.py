# -*- coding: utf-8 -*-
import random
import time


def testsortint():
    # Python中list的随机访问是非常耗时的，从list.sort()的速度之快就可以看出
    # 内部实现(C语言中)的list遍历与外部遍历的性能差异
    # 换言之，1)要尽可能利用内置的函数，而不是重新造轮子
    # 2)list的随机访问与算术计算相比，要尽可能地偏向于后者
    # bubble: 2879
    # insert: 1385
    # select: 1054
    # heap: 40(sink), 37(float) -- make heap
    # merge: 30(iter), 31(recur)
    # quick: 18.5(iter), 18.2(recur)
    # radix: 10.5
    # count: 2.3
    # list.sort(): 1.5
    def func(lst):
        lst.sort()
        return lst

    times = 500
    strlen = 5000
    total = 0
    lst = [i for i in range(1, strlen + 1)]
    for i in range(times):
        cpy = lst[:]
        random.shuffle(cpy)
        start = time.time() * 1000
        ret = func(cpy)
        end = time.time() * 1000
        total += end - start
        if lst != ret:
            print ret
        assert (lst == ret)

    print 'pass:', func, '-- cost:', total / times


def testsortstr(func):
    def test(case):
        ret = func(case[:])
        case.sort()
        if ret != case:
            print ret
            print case
        assert (ret == case)

    cases = []
    for i in range(200):
        width = random.randint(1, 25) if type == 0 else 0
        case = []
        for j in range(20):
            s = ''
            width = width if type == 0 else random.randint(1, 25)
            for k in range(width):
                s += chr(random.randint(ord('a'), ord('z')))
            case.append(s)
        cases.append(case)

    map(test, cases)


def testdp(func1, func2):
    wgt = 20
    its = [(1, 1), (2, 5), (3, 8), (4, 9), (5, 10), (6, 17), (7, 17), (8, 20), (9, 24), (10, 30)]
    assert (func1(wgt, its[:]) == func2(wgt, its[:]))


def testunionfindset(func):
    case = [4, 8, -1, 3, -1, 9, 2, 6, -1, -1, -1, 1, 7, -1, 5, -1, -1]
    ret = [4, 3, 2, 5, 6, 1, 7, 8]
    t = func(case)
    if t != ret:
        print t
    assert (ret == t)


if __name__ == '__main__':
    testsortint()
    # testsortstr()
    # testdp()
    # testunionfindset()
    print 'done'
