# -*- coding: utf-8 -*-


# @problem: vector rotation
# rotate a vector in linear time and constant space
class VectorRotation():
    def __init__(self):
        self.funcs = [self.main_reverse,
                      self.main_swap_recur,
                      self.main_swap_iter]

    def main_reverse(self, lst, shift):
        assert (0 <= shift <= len(lst))

        def reverse(low, high):
            assert (0 <= low <= high <= len(lst))
            for i in range((high - low) >> 1):
                lst[low + i], lst[high - 1 - i] = lst[high - 1 - i], lst[low + i]

        reverse(0, shift)
        reverse(shift, len(lst))
        reverse(0, len(lst))
        return lst

    def main_swap_recur(self, lst, shift):
        def swap(low, high, shift):
            if high - low < 2 or shift == 0:
                return False
            h = low + shift
            l = high - shift
            assert (h <= l)
            lst[low:h], lst[l:high] = lst[l:high], lst[low:h]
            if h == l:
                return False
            return True

        def shiftLeft(low, high, shift):
            if not swap(low, high, shift):
                return
            high -= shift
            if 0 <= low + shift <= high - shift:
                shiftLeft(low, high, shift)
            else:
                shiftRight(low, high, high - shift - low)

        def shiftRight(low, high, shift):
            if not swap(low, high, shift):
                return
            low += shift
            if 0 <= low + shift <= high - shift:
                shiftRight(low, high, shift)
            else:
                shiftLeft(low, high, high - shift - low)

        low, high = 0, len(lst)
        if low + shift <= high - shift:
            shiftLeft(low, high, shift)
        else:
            shiftRight(low, high, high - shift)
        return lst

    def main_swap_iter(self, lst, shift):
        low, high = 0, len(lst)
        left = True
        while low < high and shift > 0:
            h = low + shift
            l = high - shift
            if h <= l:  # rotate anyway
                lst[low:h], lst[l:high] = lst[l:high], lst[low:h]
                if left:
                    high = l
                else:
                    low = h
            else:
                shift = high - shift - low
                left = not left
        return lst

    def testcase(self):
        num = 900
        lst = [i for i in range(num)]
        for s in range(num + 1):
            assert (reduce(lambda x, y: x if x == y(lst[:], s) else None,
                           self.funcs[1:], self.funcs[0](lst[:], s)) != None)

        print 'pass:', self.__class__


if __name__ == '__main__':
    VectorRotation().testcase()
