# -*- coding: utf-8 -*-

import math


# vector
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)


class LineSegment():
    def intersect(self, (p1, p2), (p3, p4)):
        def crossProduct(p1, p2):
            return p1.x * p2.y - p1.y * p2.x

        def onSegment(p, (p1, p2)):
            if min(p1.x, p2.x) <= p.x <= max(p1.x, p2.x) and min(p1.y, p2.y) <= p.y <= max(p1.y, p2.y):
                return True
            return False

        d1 = crossProduct(p2 - p1, p3 - p1)
        d2 = crossProduct(p2 - p1, p4 - p1)
        d3 = crossProduct(p4 - p3, p1 - p3)
        d4 = crossProduct(p4 - p3, p2 - p3)
        # 两条线段交叉，或一条线段(至少)有一个顶点在另一条线段之上
        if (d1 * d2 < 0 and d3 * d4 < 0) \
                or (d1 == 0 and onSegment(p3, (p1, p2))) \
                or (d2 == 0 and onSegment(p4, (p1, p2))) \
                or (d3 == 0 and onSegment(p1, (p3, p4))) \
                or (d4 == 0 and onSegment(p2, (p3, p4))):
            return True
        return False


if __name__ == '__main__':
    LineSegment().intersect((Point(1, 2), Point(3, 4)), (Point(5, 4), Point(3, 1)))
    print 'done'
