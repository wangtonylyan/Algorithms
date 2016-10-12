# -*- coding: utf-8 -*-


class Interval(object):
    __slots__ = ['left', 'right']

    def __init__(self, left, right):
        # left-closed and right-open, [left, right)
        assert (left < right)
        super(Interval, self).__init__()
        self.left = left
        self.right = right

    def overlap(self, itv):
        assert (isinstance(itv, Interval))
        return (self.left < itv.right and self.right > itv.left)

    def contain(self, itv):
        assert (isinstance(itv, Interval))
        return (self.left <= itv.left and self.right >= itv.right)


if __name__ == '__main__':
    print 'done'
