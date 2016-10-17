# -*- coding: utf-8 -*-
# interval trichotomy for two intervals i and j that hold exactly one of the following three properties:
# (a) i and j overlap
# (b) i is to the left of j, i.e. i.high <= j.low
# (c) i is to the right of j, i.e. i.low >= j.high


class Interval(object):
    __slots__ = ['low', 'high']

    def __init__(self, low, high):
        # left-closed and right-open, [low, high)
        assert (low < high)
        super(Interval, self).__init__()
        self.low = low
        self.high = high

    def __len__(self):
        return (self.high - self.low)

    def overlap(self, itv):
        assert (isinstance(itv, Interval))
        return (self.low < itv.high and self.high > itv.low)
        return (max(self.high, itv.high) - min(self.low, itv.low) < len(self) + len(itv))  # by distance

    def contain(self, itv):
        assert (isinstance(itv, Interval))
        return (self.low <= itv.low and self.high >= itv.high)


if __name__ == '__main__':
    print 'done'
