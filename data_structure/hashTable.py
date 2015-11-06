# -*- coding: utf-8 -*-
# data structure: hash table

# 1) collision resolution
# linear probing: 下一个空位
# seperate chaining: 链表
# 2) parallism
# 第一次哈希入链表，第二次哈希入哈希表

import hash

# implementation: linear probing hash table based on parallel arrays
class HashTable1():
    def __init__(self):
        self.hashObj = hash.StringHash()  # the key should be a string
        # stores keys and values in parallel arrays
        self.size = 0x01 << 4  # size of arrays
        self.keys = [None for i in range(self.size)]  # fixed-size array
        self.vals = [None for i in range(self.size)]  # fixed-size array
        self.num = 0  # number of tuples in arrays, which is kept in the range [size/8, size/2]

    def _hash(self, key):
        return self.hashObj.hash3(key) % self.size

    def _resize(self, size):
        size, self.size = self.size, size
        keys, self.keys = self.keys, [None for i in range(self.size)]
        vals, self.vals = self.vals, [None for i in range(self.size)]
        num, self.num = self.num, 0
        for i in range(size):
            if keys[i] != None:
                self.put(keys[i], vals[i])

    def get(self, key):
        i = self._hash(key)
        while self.keys[i] != None:
            if self.keys[i] == key:
                return self.vals[i]
            i = (i + 1) % self.size
        return None  # values should not be None

    def put(self, key, value):
        if self.num >= (self.size >> 1):
            self._resize(self.size << 1)
        i = self._hash(key)
        while self.keys[i] != None:
            if self.keys[i] == key:
                self.vals[i] = value
                return
            i = (i + 1) % self.size
        self.keys[i] = key
        self.vals[i] = value
        self.num += 1

    def delete(self, key):
        ret = None  # because values never be None, it also indicates whether the target tuple exists
        i = self._hash(key)
        while self.keys[i] != None:
            if self.keys[i] == key:
                ret = self.vals[i]
                # set the target tuple to None
                self.keys[i] = None
                self.vals[i] = None
                break
            i = (i + 1) % self.size
        if ret != None:
            i = (i + 1) % self.size
            while self.keys[i] != None:
                self.put(key, self.vals[i])  # re-put all tuples after the deleted tuple
                self.keys[i] = None
                self.vals[i] = None
                i = (i + 1) % self.size
            self.num -= 1
            if self.num < (self.size >> 3):
                self._resize(self.size >> 1)
        return ret
