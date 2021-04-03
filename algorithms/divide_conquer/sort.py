if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('.'))

from algorithms.utility import *


class Sorting(Problem):
    def check(self, lst):
        return self.check_list_nonempty(lst)


class ComparisonBasedSorting(Sorting):
    def heap(self, lst):
        pass


class NonComparisonBasedSorting(Sorting):
    def algo_counting(self, lst):
        pass

    def algo_radix(self, lst):
        pass

    def algo_bucket(self, lst):
        pass


if __name__ == "__main__":
    Problem.testsuit([
        [ComparisonBasedSorting, [1, 2, 3, 4, 5], [5, 1, 3, 2, 4]],
        [ComparisonBasedSorting, [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]],
    ])
