# -*- coding: utf-8 -*-
# design pattern: composite
# 组合模式解决的问题是如何构建一个组合类使得其同时具有多个同种子部件类的特性
# 常规的实现方案是将组合类多继承于所有的子部件类，子部件类通过暴露内部属性/方法供其使用
# 而利用该模式则可以有效地避免多继承


class CompositePattern():
    # component's interface
    class AbstractComponent():
        def interface(self):
            pass

    class Component1(AbstractComponent):
        def interface(self):
            print 'do something1'

    class Component2(AbstractComponent):
        def interface(self):
            print 'do something2'

    # 其与子部件类继承于相同的接口，是为了保持“一个类是否是组合而成”对于用户的透明性
    class CompositeComponent(AbstractComponent):
        def __init__(self):
            self.components = []

        def addComponent(self, com):
            assert (isinstance(com, CompositePattern.AbstractComponent))
            self.components.append(com)

        def interface(self):
            for com in self.components:
                com.interface()

    @staticmethod
    def testcase():
        com1 = CompositePattern.Component1()
        com2 = CompositePattern.Component2()
        coms = CompositePattern.CompositeComponent()
        coms.addComponent(com1)
        coms.addComponent(com2)
        coms.interface()


if __name__ == '__main__':
    CompositePattern.testcase()
