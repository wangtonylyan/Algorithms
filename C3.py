# -*- coding: utf-8 -*-
# @problem: superclass linearization
# @solution: C3
# @application: mro (method resolution order) in Python


class MethodResolutionOrder():
    # @param: a class object (either classic or new-style)
    # @return: a list equals the new-style class object's mro member function
    def main(self, clsobj):
        def c3_1(llst):
            ret = []
            i = 0
            while i < len(llst):
                llst = filter(lambda x: True if len(x) > 0 else False, llst)
                if len(llst) == 0:
                    break
                if reduce(lambda t, x: t and x, map(lambda x: False if llst[i][0] in x[1:] else True, llst), True):
                    p = llst[i][0]
                    ret.append(p)
                    map(lambda x: x.pop(0) if x[0] == p else x, llst)
                    i = 0
                else:
                    i += 1
            return ret

        def c3_2(llst):
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

        # clsobj.__bases__ is a tuple
        mro1 = c3_1([[clsobj]] + map(self.main, clsobj.__bases__) + [list(clsobj.__bases__)])
        mro2 = c3_2([[clsobj]] + map(self.main, clsobj.__bases__) + [list(clsobj.__bases__)])
        assert (mro1 == mro2)
        return mro1

    def testcase(self):
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

        mro1 = self.main(Z)
        mro2 = Z.mro()
        print mro1
        print mro2
        assert (mro1 == mro2)

        print 'pass:', self.__class__


if __name__ == '__main__':
    MethodResolutionOrder().testcase()
