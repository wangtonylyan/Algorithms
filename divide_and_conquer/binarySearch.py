# -*- coding: utf-8 -*-


class BinarySearch():
    # @premise: list has been sorted in increasing order
    def main(self, lst, val):
        low = 0
        high = len(lst) - 1
        while low <= high:
            mid = low + ((high - low) >> 1)
            if lst[mid] < val:
                low = mid + 1
            elif lst[mid] > val:
                high = mid - 1
            else:
                return True
        return False

    def testcase(self):
        lst = [1, 2, 3]
        for i in lst:
            assert (self.main(lst, i))
        lst = [1, 2, 3, 4]
        for i in lst:
            assert (self.main(lst, i))
        print 'pass:', self.__class__


# 插补查找是以数据分布的近似均匀为前提，通过比例运算来求出类似二分查找中的中间值
# 进而分治，所以其本原则与二分查找是相同的
# On average the interpolation search makes about log(log(n)) comparisons (if the elements are uniformly distributed).
# In the worst case (for instance where the numerical values of the keys increase exponentially) it can make up to O(n) comparisons.
class InterpolationSearch(BinarySearch):
    def main(self, lst, val):
        low = 0
        high = len(lst) - 1
        while low < high and lst[low] <= val <= lst[high]:
            mid = low + (val - lst[low]) * (high - low) / (lst[high] - lst[low])
            if lst[mid] < val:
                low = mid + 1
            elif lst[mid] > val:
                high = mid - 1
            else:
                return True
        if low == high and lst[low] == val:
            return True
        return True


# @problem: Given a sorted array of distinct elements,
# and the array is rotated at an unknown position.
# Find minimum element in the array.
# 例如[1,2,3,4,5]在第二个位置被旋转后为[3,4,5,1,2]，函数返回1
# 类似的问题还有：
# @problem_1: Given an array of n distinct integers sorted in ascending order,
# write a function that returns a Fixed Point in the array.
# Fixed Point in an array is an index i such that arr[i] is equal to i.
# Note that integers in array can be negative.
class FindMinInRotatedArray():
    def main(self, lst):
        assert (lst and isinstance(lst, list) and len(lst) > 0)
        low = 0
        high = len(lst) - 1
        while low < high:
            mid = low + ((high - low) >> 1)
            if lst[mid] > lst[high]:
                low = mid + 1
            elif lst[mid] < lst[low]:
                high = mid
            else:
                high = low
        assert (low == high)
        assert (min(lst) == lst[low])
        return lst[low]

    def testcase(self):
        def test(lst):
            for i in range(len(lst)):
                temp = lst[i:] + lst[0:i]
                assert (self.main(temp) == min(temp))

        map(test, [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4]])
        print 'pass:', self.__class__


if __name__ == '__main__':
    BinarySearch().testcase()
    InterpolationSearch().testcase()
    FindMinInRotatedArray().testcase()
    print 'done'
