# -*- coding: utf-8 -*-
# problem: superclass linearization
# solution: C3
# application: mro (method resolution order) in Python

def car(lst):
    return lst[0]


def cdr(lst):
    return lst[1:]


# @param: a class object (either classic or new-style)
# @return: a list equals the new-style class object's mro member function
def mro(clsobj):
    def merge(llst):
        ret = []
        i = 0
        while i < len(llst):
            llst = filter(lambda x: True if len(x) > 0 else False, llst)
            # llst = [m for m in llst if len(m) > 0]
            if len(llst) == 0:
                break
            if reduce(lambda t, x: t and x, map(lambda x: False if car(llst[i]) in cdr(x) else True, llst), True):
                p = car(llst[i])
                ret.append(p)
                map(lambda x: x.pop(0) if car(x) == p else x, llst)
                i = 0
            else:
                i += 1
        return ret

    def merge2(llst):
        ret = []
        flag = True
        while flag:
            flag = False
            llst = [m for m in llst if len(m) > 0]
            for i in range(len(llst)):
                tar = llst[i][0]
                flag2 = True
                for j in range(i + 1, len(llst)):
                    if tar in llst[j][1:]:
                        flag2 = False
                        break
                if flag2:
                    ret.append(tar)
                    for j in range(len(llst)):
                        if llst[j][0] == tar:
                            llst[j] = llst[j][1:]
                    flag = True
                    break
        return ret

    return merge2([[clsobj]] + map(mro, clsobj.__bases__) + [list(clsobj.__bases__)])  # clsobj.__bases__ is a tuple


def testcase1():
    class O(object): pass

    class A(O): pass

    class B(O): pass

    class C(O): pass

    class D(O): pass

    class E(O): pass

    class K1(A, B, C): pass

    class K2(D, B, E): pass

    class K3(D, A): pass

    class Z(K1, K2, K3): pass

    print mro(Z)
    print Z.mro()
    assert (mro(Z) == Z.mro())


if __name__ == '__main__':
    testcase1()
