# -*- coding: utf-8 -*-


class Huffman():
    class Node():
        def __init__(self, key, value):
            self.left = None
            self.right = None
            self.key = key
            self.value = value

    def __init__(self):
        pass

    def main(self, chst):
        assert (len(chst) > 0)
        key = lambda x: x.key

        def float(hp, low, high):
            it = (low - 1) >> 1
            while it >= high:
                if key(hp[it]) < key(hp[low]):
                    break
                hp[low], hp[it] = hp[it], hp[low]
                low = it
                it = (low - 1) >> 1

        def sink(hp, low, high):
            t = hp[low]
            p = low
            it = low << 1 | 1
            while it < high:
                if it + 1 < high and key(hp[it + 1]) < key(hp[it]):
                    it += 1
                hp[low] = hp[it]
                low = it
                it = low << 1 | 1
            hp[low] = t
            float(hp, low, p)

        def pop(hp):
            hp[0], hp[-1] = hp[-1], hp[0]
            ret = hp.pop()
            if len(hp) > 1:
                sink(hp, 0, len(hp))
            return ret

        def push(hp, n):
            hp.append(n)
            float(hp, len(hp) - 1, 0)

        # new Nodes
        hp = []
        for c, f in chst:
            hp.append(self.__class__.Node(f, c))
        # make heap
        for i in range(1, len(hp)):
            float(hp, i, 0)
        # build tree
        while len(hp) > 1:
            left = pop(hp)
            right = pop(hp)
            node = self.__class__.Node(key(left) + key(right), None)
            node.left = left
            node.right = right
            push(hp, node)
        # return root
        return hp[0]

    def testcase(self):
        case = [('a', 45), ('b', 13), ('c', 12), ('d', 16), ('e', 9), ('f', 5)]
        assert (sum(map(lambda x: x[1], case)) == self.main(case).key)
        print 'pass:', self.__class__


if __name__ == '__main__':
    Huffman().testcase()
    print 'done'
