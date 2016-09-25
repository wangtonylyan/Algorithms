# -*- coding: utf-8 -*-
# 只有叶子节点才存储有效信息，中间结点不存储任何信息
# 这样就保证了任意一个字符的编码不会是其他字符编码的前缀

import copy
from data_structure.heap.binary import MinBinaryHeap
from data_structure.queue import Queue


class HuffmanCode():
    class Node():
        def __init__(self, key, value, left=None, right=None):
            self.left = left
            self.right = right
            self.key = key
            self.value = value

    def main(self, chst):
        assert (isinstance(chst, dict) and len(chst) > 2)  # makes sense
        # build Huffman tree
        hp = MinBinaryHeap(map(lambda (c, f): self.__class__.Node(f, c), chst.items()), lambda x: x.key)
        while len(hp) > 1:
            left = hp.pop()
            right = hp.pop()
            node = self.__class__.Node(left.key + right.key, None, left, right)
            hp.push(node)
        # check tree and prepare for code generation
        assert (len(hp) == 1)
        node = hp.pop()
        assert (node.key == sum(map(lambda x: x[1], chst.items())) and node.value is None)
        node.key = None
        # generate Huffman code by traversing Huffman tree
        que = Queue()
        que.push(node)
        while len(que) > 0:
            node = que.pop()
            if node.value is not None:
                assert (isinstance(node.key, str) and isinstance(node.value, str))
                chst[node.value] = node.key
                assert (node.left is None and node.right is None)
            elif node.key is None:  # node is root
                if node.left:
                    node.left.key = '0'
                    que.push(node.left)
                if node.right:
                    node.right.key = '1'
                    que.push(node.right)
            else:
                assert (isinstance(node.key, str))
                if node.left:
                    node.left.key = node.key + '0'
                    que.push(node.left)
                if node.right:
                    node.right.key = node.key + '1'
                    que.push(node.right)
        return chst

    def testcase(self):
        def test(case):
            ret = self.main(copy.deepcopy(case))
            print ret
            assert (isinstance(ret, dict) and ret.keys() == case.keys())
            for k, v in ret.items():
                assert (isinstance(k, str) and isinstance(v, str))

        # dict = {character:frequency/number}
        cases = [{'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5},
                 {'a': 2, 'b': 2, 'c': 2}]
        map(test, cases)
        print 'pass:', self.__class__


if __name__ == '__main__':
    HuffmanCode().testcase()
    print 'done'
