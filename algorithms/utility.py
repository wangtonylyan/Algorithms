import re

pinfty = float('+inf')  # positive infinity
ninfty = float('-inf')  # negative infinity


# Python有内置函数id()，但其返回的是对象的唯一标识号
def identity(x, *args, **kwargs):
    return x


def const(x):
    return lambda _: x


class Problem:
    def __init__(self):
        self.solutions = list(filter(lambda x: re.match('^algo.*', x), dir(self)))

    def check(self, *args):
        return tuple(args)

    @staticmethod
    def check_list_nonempty(lst):
        assert len(lst) > 0
        return lst[:]  # avoid in-place modification

    @staticmethod
    def check_matrix_nonempty(mat):
        m, n = len(mat), len(mat[0])
        assert m > 0 and n > 0 and all(map(lambda x: len(x) == n, mat))
        return [mat[i][:] for i in range(len(mat))]

    def run(self, *args):
        assert len(self.solutions) > 0
        print('-' * 20)
        print(self.solutions)

        def apply(f):
            r = self.check(*args)
            return getattr(self, f)(*r) if isinstance(r, tuple) \
                else getattr(self, f)(r)
        ret = map(apply, self.solutions)

        ret = list(filter(lambda x: x is not None, ret))
        assert len(ret) > 0

        if not all(map(lambda x: x == ret[0], ret)):
            print('solutions: ', ret)
            print('-' * 20)
            assert False
        else:
            print(ret[0])
            print('-' * 20)
        return ret[0]

    @staticmethod
    def testsuit(suit):
        for testcase in suit:
            assert len(testcase) >= 2
            cls, rlt, args = testcase[0], testcase[1], testcase[2:]
            ret = cls().run(*args)
            if rlt is not None:
                assert ret == rlt
