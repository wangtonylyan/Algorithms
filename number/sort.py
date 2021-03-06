
class SelectionSort(Sort):
    def main_recur(self, lst):
        # inner loop: select the minimum of lst[ind:] and return its index
        def select(ind):
            if ind >= len(lst) - 1:
                return ind
            m = select(ind + 1)
            return ind if lst[ind] <= lst[m] else m

        # outer loop: select and (tail) recursion
        if len(lst) < 2:
            return lst
        m = select(0)
        lst[0], lst[m] = lst[m], lst[0]
        return [lst[0]] + self.main_recur(lst[1:])


class BubbleSort(Sort):
    def main_recur(self, lst):
        # inner loop: bubble up the maximum into lst[-1]
        def bubble(lst):
            if len(lst) < 2:
                return lst
            if lst[0] > lst[1]:
                lst[0], lst[1] = lst[1], lst[0]
            return [lst[0]] + bubble(lst[1:])

        # outer loop: bubble and (tail) recursion
        if len(lst) < 2:
            return lst
        lst = bubble(lst)
        return self.main_recur(lst[:-1]) + [lst[-1]]


class HeapSort(Sort):
    def __init__(self):
        super(HeapSort, self).__init__()
        self.funcs.append(self.main)
        self.funcs.append(self.main_heap)

    def main(self, lst):
        return MaxBinaryHeap.heapsort(lst)

    # 堆排序也可以完全通过堆的封装接口来实现
    def main_heap(self, lst):
        # build heap
        hp = MaxBinaryHeap(lst)
        # sort by heap
        for i in range(len(lst) - 1, -1, -1):
            lst[i] = hp.pop()
        return lst


# O(n+k), k is the range of input
# Counting sort is efficient if the range of input data is not
# significantly greater than the number of objects to be sorted.
# Consider the situation where the input sequence is 10, 5, 10K, 5K.
class CountingSort(Sort):
    def __init__(self):
        super(CountingSort, self).__init__()
        self.funcs.append(self.main)

    def main(self, lst):
        low, high = min(lst), max(lst)  # calculate the range
        cnt = [0] * (high - low + 2)  # index 0 is reserved
        for i in range(len(lst)):
            cnt[lst[i] - low + 1] += 1
        for i in range(len(cnt) - 1):
            cnt[i + 1] += cnt[i]
        cpy = lst[:]
        for i in range(len(cpy)):
            lst[cnt[cpy[i] - low]] = cpy[i]
            cnt[cpy[i] - low] += 1

        return lst


# Radix sort弥补了counting sort不适用于大范围输入域的缺陷
# 但逐个数位的比较也降低了效率
class RadixSort(Sort):
    def __init__(self):
        super(RadixSort, self).__init__()
        self.funcs.append(self.main)

    def main(self, lst):
        def count(ind):  # stable
            ind = 10 ** ind  # 10-based
            cnt = [0] * (11)  # index 0 is reserved
            for i in lst:
                cnt[i / ind % 10 + 1] += 1
            for i in range(len(cnt) - 1):
                cnt[i + 1] += cnt[i]
            cpy = lst[:]
            for i in cpy:
                lst[cnt[i / ind % 10]] = i
                cnt[i / ind % 10] += 1

        m, i = max(lst), 0
        while m > 0:
            count(i)
            m /= 10
            i += 1
        return lst


# input should be uniformly distributed across the range
class BucketSort(Sort):
    def __init__(self):
        super(BucketSort, self).__init__()
        self.funcs.append(self.main)

    def main(self, lst):
        # 哈希算法本身还需要维护不同bucket中数据之间的相对顺序
        # 例如bucket[0]中的数据都必须小于bucket[1]中的，以此类推
        def hash(x): return x / 10  # for simplicity
        bucket = [[] for _ in range(hash(max(lst)) + 1)]
        for i in lst:
            bucket[hash(i)].append(i)
        map(list.sort, bucket)
        return reduce(lambda x, y: x + y, bucket, [])


# @problem: convert an unsorted array into Zig-Zag fashion in O(n) time
class ConvertZigZagArray():
    # 只需确保偶数索引项(驼峰)大于左右两边的奇数索引项
    def main_1(self, lst):
        for i in range(0, len(lst), 2):
            if i > 0 and lst[i] < lst[i - 1]:
                lst[i], lst[i - 1] = lst[i - 1], lst[i]
            if i < len(lst) - 1 and lst[i] < lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]

    # 基于冒泡思想
    def main_2(self, lst):
        flag = True  # > if True else <
        for i in range(len(lst) - 1):
            if flag:
                if lst[i] < lst[i + 1]:
                    lst[i], lst[i + 1] = lst[i + 1], lst[i]
            else:
                if lst[i] > lst[i + 1]:
                    lst[i], lst[i + 1] = lst[i + 1], lst[i]
            flag = not flag


# @problem: Find the closest pair from two sorted arrays in O(n) time
class FindClosestPair():
    def main(self, lst1, lst2, sum):
        i, j = 0, len(lst2) - 1
        m = abs(lst1[i] + lst2[j] - sum)
        while i < len(lst1) and j >= 0:
            t = abs(lst1[i] + lst2[j] - sum)
            if t < m:
                m = t
            if lst1[i] + lst2[j] > sum:
                j -= 1
            elif lst1[i] + lst2[j] < sum:
                i += 1
            else:
                break
        return m

    def testcase(self):
        assert (self.main([1, 4, 5, 7], [10, 20, 30, 40], 32) == 1)
        assert (self.main([1, 4, 5, 7], [10, 20, 30, 40], 50) == 3)
        print 'pass:', self.__class__

