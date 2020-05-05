pinfty = float('+inf')  # positive infinity
ninfty = float('-inf')  # negative infinity


def identity(x):
    return x


def const(x):
    return lambda _: x


class Problem:
    def __init__(self):
        # 执行以solution为前缀名的函数，并记录结果
        # 比较所有结果是否相等
        pass

    def check(self, testcase):
        assert testcase

    def check_list(self, lst):
        assert len(lst) > 0

    def check_matrix(self, mat):
        m, n = len(mat), len(mat[0])
        assert m > 0 and n > 0 and all(map(lambda x: len(x) == n, mat))

    def run(self, *args):
        self.check(*args)
        ret = [self.solution1(*args),
               self.solution2(*args),
               self.solution3(*args), ]

        ret = list(filter(lambda x: x is not None, ret))
        assert len(ret) > 0

        print('-' * 20)
        if not all(map(lambda x: x == ret[0], ret)):
            print('solutions: ', ret)
            assert False
        else:
            print(ret[0])
            print('-' * 20)
        return ret[0]

    def solution1(self, *args):
        pass

    def solution2(self, *args):
        pass

    def solution3(self, *args):
        pass

    @staticmethod
    def testsuit(suit):
        for testcase in suit:
            assert len(testcase) >= 2
            cls, rlt, args = testcase[0], testcase[1], testcase[2:]
            ret = cls().run(*args)
            if rlt is not None:
                assert ret == rlt
