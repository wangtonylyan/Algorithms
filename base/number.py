# -*- coding: utf-8 -*-

import random
import unittest


# self.assertEqual(1, 1)
# self.assertTrue(1)
# self.assertFalse(0)
# self.assertRaises(TypeError)
class NumberTestCase(unittest.TestCase):
    def __init__(self, alphabet=[0, 10000]):
        super().__init__()
        self.config = {
            'minlen': 1,
            'maxlen': 50,
            'alphabet': alphabet,
        }

    @classmethod
    def setUpClass(cls):
        # generate test cases
        self.cases = []
        for _ in range():
            pass

    def setUp(self):
        print('setup')

    def tearDown(self):
        print('teardown')


class NumberTest(Test):
    @classmethod
    def _gencase(cls, fixed=False, minLen=1, maxLen=50, each=50, total=100, dup=True):
        cases = []
        for _ in range(total):
            case = []
            width = random.randint(minLen, maxLen) if fixed else None
            for _ in range(each):
                width = width if fixed else random.randint(minLen, maxLen)
                if dup:
                    case.append([random.randint(0, Number.alphabet)
                                 for _ in range(width)])
                else:
                    assert (width <= Number.alphabet + 1)
                    low = random.randint(0, Number.alphabet - width)
                    lst = [_ for _ in range(low, low + width)]
                    random.shuffle(lst)
                    case.append(lst)
            cases.append(case)
        return cases


if __name__ == '__main__':
    cases = NumberTest()._gencase()
    for case in cases:
        # print case
        assert (isinstance(case, list) and len(case) > 0)
        for lst in case:
            assert (isinstance(lst, list) and len(lst) > 0)
            assert (all(isinstance(i, int) and 0 <=
                        i <= Number.alphabet for i in lst))
    # print len(cases)
    # print 'done'

    unittest.main(verbosity=2)
