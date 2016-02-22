# -*- coding: utf-8 -*-


class BinarySearch():
    def __init__(self):
        pass

    # @premise: lst has been sorted increasingly
    @staticmethod
    def main(lst, val):
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

    def check(self):
        lst = [1, 2, 3]
        for i in lst:
            assert (self.main(lst, i))
        lst = [1, 2, 3, 4]
        for i in lst:
            assert (self.main(lst, i))

    # [Problem]
    # Given a sorted array of distinct elements, and the array is rotated at an unknown position.
    # Find minimum element in the array.
    # 例如[1,2,3,4,5]在第二个位置被旋转后为[3,4,5,1,2]，函数返回1
    def findMinInRotatedArray(self):
        def func(lst):
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

        lst = [1, 2, 3, 4]
        for i in range(len(lst)):
            temp = lst[i:] + lst[0:i]
            assert (func(temp) == min(temp))


if __name__ == '__main__':
    bs = BinarySearch()
    bs.check()
    bs.findMinInRotatedArray()
    print 'done'
