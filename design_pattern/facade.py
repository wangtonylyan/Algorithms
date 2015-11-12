# -*- coding: utf-8 -*-
# design pattern: facade
# purpose:
# 1) Facade模式的作用包含了Java中的interface
# 由于GoF提出23种设计模式是在1994年左右，其基于的语言还停留在Smalltalk和C++
# 随着Java语言的诞生，其将class与interface两者在概念上做了更为细致的分化
# 因此interface在某种程度上就是Facade模式的一种具体实现方案
# 2) Facade Pattern对应的中文翻译为门面模式
# 从字面上即可知，该模式是关注于对一个系统进行封装，目的是对外提供统一的访问接口
# 与Java中interface不同的是，它不仅简化了复杂系统对外的表现（即interface的作用）
# 还同时由于其可以包含系统子模块之间交互的业务逻辑，因此使得子模块之间的耦合度降低了
# 总之，Facade起到的是一个承上启下的作用
# 3) Facade使得系统对外暴露的接口变得简洁了，这还能简化编译上的依赖关系
# 从而提高编译速度，这对于大型系统而言也是至关重要的
class FacadePattern():
    # 以下是同一个系统中的三大子模块
    class Module1():
        def doSomething(self):
            print 'Module1 do something'
    class Module2():
        def doSomething(self):
            print 'Module2 do something'
    class Module3():
        def doSomething(self):
            print 'Module3 do something'

    class AbstractFacade():  # interface
        def interface1(self):
            pass
        def interface2(self):
            pass
        def interface3(self):
            pass
    class Facade(AbstractFacade):
        def __init__(self, module1, module2, module3):
            self.module1 = module1
            self.module2 = module2
            self.module3 = module3
        def interface1(self):
            # 以下体现的是子模块之间的耦合关系
            self.module1.doSomething()
            self.module2.doSomething()
        def interface2(self):
            self.module2.doSomething()
            self.module3.doSomething()
        def interface3(self):
            self.module3.doSomething()
            self.module1.doSomething()

    @staticmethod
    def testcase():
        m1 = FacadePattern.Module1()
        m2 = FacadePattern.Module2()
        m3 = FacadePattern.Module3()
        f = FacadePattern.Facade(m1, m2, m3)
        f.interface1()
        f.interface2()
        f.interface3()


if __name__ == '__main__':
    FacadePattern.testcase()
