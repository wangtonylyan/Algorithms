# -*- coding: utf-8 -*-
# design pattern: factory method & abstract factory (kit)
# 名字中的factory可以被理解为产品的生产线
# 前者适用于需要生产同一种类但型号不同的产品（即继承于同一个父类）
# 而后者适用于生产不同组合的成套产品（即针对于组合关系）

# 背景：以下是两种彼此不同的独立产品，且各自有两种具体的型号
# 产品族A
class AbstractProductA(object):
    def __init__(self, _data):
        self.data = _data
# 具体产品型号A1
class ProductA1(AbstractProductA):
    def __init__(self):
        super(ProductA1, self).__init__('A1')
# 具体产品型号A2
class ProductA2(AbstractProductA):
    def __init__(self):
        super(ProductA2, self).__init__('A2')
# 产品族B
class AbstractProductB(object):
    def __init__(self, _data):
        self.data = _data
# 具体产品型号B1
class ProductB1(AbstractProductB):
    def __init__(self):
        super(ProductB1, self).__init__('B1')
# 具体产品型号B2
class ProductB2(AbstractProductB):
    def __init__(self):
        super(ProductB2, self).__init__('B2')


# 该模式的核心实现表现于多个相关类中的同名方法中，而这些类的核心职责通常是使用其返回值（自产自销）
class FactoryMethodPattern():
    # strategy1: use one specific class for each product
    # 每新增一个产品就必须新增一个子类，但优点是不用修改现有的类，即满足open closed principle
    class AbstractConsumer():  # interface
        def factoryMethod(self):
            pass
    class Consumer1(AbstractConsumer):
        def factoryMethod(self):
            return ProductA1()
    class Consumer2(AbstractConsumer):
        def factoryMethod(self):
            return ProductA2()

    # strategy2: use a unified class
    class Consumer():
        # and differentiate the various products by an external parameter
        def factoryMethod(self, productId):
            exec 'it = ProductA' + str(productId) + '()'  # or use a switch-case structure instead
            return it

    @staticmethod
    def testcase():
        # use Consumer's factory method to create a Product
        # strategy1
        c1 = FactoryMethodPattern.Consumer1()
        c2 = FactoryMethodPattern.Consumer2()
        p1 = c1.factoryMethod()
        p2 = c2.factoryMethod()
        print p1.data, p2.data,
        # strategy2
        c = FactoryMethodPattern.Consumer()
        p1 = c.factoryMethod(1)
        p2 = c.factoryMethod(2)
        print p1.data, p2.data


# 该模式的核心实现表现为多个类，即这些类的职责就是基于该模式创建对象
class AbstractFactoryPattern():
    # strategy: 为每种组合方案创建一个抽象工厂类
    class AbstractAbstractFactory():  # interface
        def createA(self):
            pass
        def createB(self):
            pass
    class AbstractFactory1(AbstractAbstractFactory):
        def createA(self):  # 这其实也就是一个factory method
            return ProductA1()
        def createB(self):
            return ProductB2()
    class AbstractFactory2(AbstractAbstractFactory):
        def createA(self):
            return ProductA2()
        def createB(self):
            return ProductB1()

    @staticmethod
    def testcase():
        # create a Factory corresponding to a specific Product
        f1 = AbstractFactoryPattern.AbstractFactory1()
        f2 = AbstractFactoryPattern.AbstractFactory2()
        # create Product via its Factory
        p1 = f1.createA()
        p2 = f1.createB()
        print p1.data, p2.data,
        p1 = f2.createA()
        p2 = f2.createB()
        print p1.data, p2.data


if __name__ == '__main__':
    FactoryMethodPattern.testcase()
    AbstractFactoryPattern.testcase()