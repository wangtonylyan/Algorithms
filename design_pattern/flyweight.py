# -*- coding: utf-8 -*-
# design pattern: flyweight
# 享元模式，即将公共的、与外部环境无关的元素对象在同类对象之间进行共享，以节省内存占用
# 其作用类似于软件架构级别的内存池、线程池等，以及Python语言级别的__slots__类属性
# 被共享的元素类自身只能拥有intrinsic state，而不能拥有任何extrinsic state
# 享元模式常与抽象工厂模式、组合模式等配合使用
# 抽象工厂模式用于实现享元对象的存储和管理
# 组合模式基于享元模式的优点，可大量地组合享元对象

class FlyweightPattern():
    class AbstractFlyweight():  # 享元类的接口
        def __init__(self):
            self.intrinsicState = 0

        def method(self):
            pass

    class FlyweightFactory():  # 享元对象的创建工厂
        def __init__(self):
            self.flyweights = {}  # 享元对象的存储池

        def getFlyweight(self, cls):
            assert (issubclass(cls, FlyweightPattern.AbstractFlyweight))
            if not cls in self.flyweights.keys():
                assert(callable(cls))
                self.flyweights[cls] = cls()
            return self.flyweights[cls]

    class Flyweight(AbstractFlyweight):
        def __init__(self):
            FlyweightPattern.AbstractFlyweight.__init__(self)

        def method(self):
            print 'do something'

    @staticmethod
    def testcase():
        fac = FlyweightPattern.FlyweightFactory()
        sharedFw1 = fac.getFlyweight(FlyweightPattern.Flyweight)
        sharedFw2 = fac.getFlyweight(FlyweightPattern.Flyweight)
        assert (sharedFw1 is sharedFw2)
        sharedFw1.method()
        sharedFw2.method()
        # 享元模式并不强制共享，也可单独创建非共享的对象
        unsharedFw = FlyweightPattern.Flyweight()
        unsharedFw.method()
        assert (unsharedFw is not sharedFw1)


if __name__ == '__main__':
    FlyweightPattern.testcase()
