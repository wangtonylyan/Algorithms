# 【函数传参】
# *args与**kwargs，两者是独立的，被分别称为positional和keyword argument
# 前者不包括任何指定了关键字的传参，后者仅包括了已指定关键字的传参
# 在函数应用中，前者必须先于后者，即一旦某个传参指定了关键字，则后续传参都需指定关键字
# 类似地，在函数声明中，前者也必须先于后者，即\先于*

# 【类中的方法】
# 类中的staticmethod，适用于
# 1. 该函数仅被该类中的方法所调用，定义于类中，不会污染类外的代码
# 特殊情况：
# 1. 该函数会递归调用自身，由于类中的函数都需要通过self或cls来引用
# 因此，无法直接通过函数名来调用自身，而只能引入如下的额外实现层次
class Class:
    @staticmethod
    def recur(*args):
        def main(*args):
            return main(*args)
        main(*args)

# 此处的iterate与traverse区别在于，
# 前者是单次、同向、无重复，后者是前后来回、多次

# iterable object，可迭代对象，
# 实现了__iter__()方法，返回的是迭代器对象
# iterator object，迭代器对象，
# 实现了__next__()方法，
# 关键词for、in等都作用于迭代器对象
# 一般，迭代器对象本身也是可迭代的，所有会实现__iter__()方法并返回自身

# 两种实现思路：
# 1. 容器本身就是迭代器，即__iter__()返回容器自身
# 这种实现方式的缺陷在于，该容器在迭代完成后，需要手动重置迭代状态
# 例如，range、xrange等类，都以此方式来实现
# 2. 容器可生成一个迭代器，即__iter__()返回容器自身的迭代器
# 类似地，由iter()返回的每个迭代器对象，都只能对原容器进行一次遍历
# 多次遍历只需调用多次iter()即可


class Container:
    def __init__(self, size):
        self.size = size

    def __iter__(self):
        return Iterator(self.size)


class Iterator():
    def __init__(self, end):
        self.idx = 0
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        while self.idx < self.end:
            self.idx += 1
            return self.idx
        raise StopIteration


if __name__ == '__main__':
    c = Container(10) # iterable object

    for e in c: # call __iter__() to get a new iterator object
        print(e)

    it = iter(c) # explicitly get a new iterator object
    print(1 in it) # True，遍历至1
    print(2 in it) # True，遍历至2
    print(2 in it) # False，从3开始遍历至结束
    print(3 in it) # false，迭代器it已遍历结束

    list(iterator) # 接受迭代器传参，返回列表

    f = (lambda: 1)
    f()
