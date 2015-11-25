# -*- coding: utf-8 -*-
# design pattern: bridge (handle)
# 桥接模式提供了一种“直接继承”的可替代方案，其使得接口类与实现类可以各自独立地演化
# 两者将拥有各自的继承树，类似于Java中的Interface语法机制
# 相比于适配器模式，后者是在不修改现有类代码的前提下，耦合两个原本无关的类
# 而前者则是在设计上就预留扩展性，允许接口类和实现类被演化得截然不同


class BridgePattern():
    # 接口类的继承树（演化过程）
    class AbstractInterface():
        def __init__(self, imp):
            # 桥接体现在对象层面，而非类层面
            self.imp = imp
        def method(self):
            self.imp.methodImp()
    class Interface1(AbstractInterface):
        def method1(self):
            # 接口类与实现类的耦合性并没有因桥接模式而降低
            # 该模式只是使得各自的继承关系更为独立而清晰
            self.imp.methodImp1()
            self.imp.methodImp2()
    class Interface2(AbstractInterface):
        def method2(self):
            self.imp.methodImp3()
            self.imp.methodImp4()

    # 实现类的继承树（实现类甚至可以提供与接口类不同的方法）
    class AbstractImplementor():
        def methodImp(self):
            print 'do something'
    class Implementor1(AbstractImplementor):
        def methodImp1(self):
            print 'do something1'
        def methodImp2(self):
            print 'do something2'
    class Implementor2(AbstractImplementor):
        def methodImp3(self):
            print 'do something3'
        def methodImp4(self):
            print 'do something4'

    @staticmethod
    def testcase():
        imp1 = BridgePattern.Implementor1()
        int1 = BridgePattern.Interface1(imp1)
        int1.method1()
        imp2 = BridgePattern.Implementor2()
        int2 = BridgePattern.Interface2(imp2)
        int2.method2()


if __name__ == '__main__':
    BridgePattern.testcase()
