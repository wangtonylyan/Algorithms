# -*- coding: utf-8 -*-
# design pattern: builder
# 相比于抽象工厂模式，该模式更强调对于单个产品的组装，例如类的属性的初始化
# 其核心思想是isolating code for construction and representation of an object


class BuilderPattern:
    # this class specifies the representation of Product
    class Product:
        def __init__(self):
            # components
            self.data1 = None
            self.data2 = None
            self.data3 = None

    # this class provides the construction primitives of Product
    class Builder():
        def __init__(self):
            self.product = BuilderPattern.Product()

        def buildPart1(self, part=1):
            self.product.data1 = part

        def buildPart2(self, part=2):
            self.product.data2 = part

        def buildPart3(self, part=3):
            self.product.data3 = part

    # this class directs the whole construction process of Product, and produces it
    class Director():
        def __init__(self, builder):
            assert (isinstance(builder, BuilderPattern.Builder))
            self.builder = builder

        # you can also specify the Builder as a parameter of this method
        # which means Director is not bound to any Builder
        def build(self):
            # takes finer control over the construction process
            # 以下的构造方式（顺序、数值等）可以随意变更
            self.builder.buildPart1(3)
            self.builder.buildPart2()
            self.builder.buildPart3(1)
            return self.builder.product

    @staticmethod
    def testcase():
        # create a Builder corresponding to a specific Product
        b = BuilderPattern.Builder()
        # specify the Builder for Director
        d = BuilderPattern.Director(b)
        # use the Director to construct a Product
        p = d.build()
        print p.data1, p.data2, p.data3


if __name__ == '__main__':
    BuilderPattern.testcase()
