# -*- coding: utf-8 -*-

from data_structure.heap import MinHeap


class Huffman():
    class Node():
        def __init__(self, key, value):
            self.left = None
            self.right = None
            self.key = key
            self.value = value

    def main(self, chst):
        assert (len(chst) > 0)
        key = lambda x: x.key
        # new Nodes and make heap
        hp = map(lambda (c, f): self.__class__.Node(f, c), chst)
        hp = MinHeap(hp, key)
        # build tree
        while hp.size() > 1:
            left = hp.pop()
            right = hp.pop()
            node = self.__class__.Node(key(left) + key(right), None)
            node.left = left
            node.right = right
            hp.push(node)
        return hp.pop()

    def testcase(self):
        case = [('a', 45), ('b', 13), ('c', 12), ('d', 16), ('e', 9), ('f', 5)]
        assert (sum(map(lambda x: x[1], case)) == self.main(case).key)
        print 'pass:', self.__class__


if __name__ == '__main__':
    Huffman().testcase()
    print 'done'
