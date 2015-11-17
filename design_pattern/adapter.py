# -*- coding: utf-8 -*-
# design pattern: adapter (wrapper)
# 与代理和装饰模式不同的是，它们提供的是与被代理/修饰类完全相同的接口，只是提供一层indirection
# 而适配器模式的目的则正好在于要转变被适配类/对象的当前接口

class AdapterPattern():
    # Adapter adapts Adaptee to Interface
    # which avoids Adaptee from inheriting Interface
    class Interface():
        def request(self):
            pass

    class Adaptee():
        def specificRequest(self):
            print 'do something'

    # strategy1: class adapter
    # 优点是Adapter类直接继承至Adaptee类，易于Adapter去封装Adaptee的行为
    # 缺点是Adapter类绑定至了Adaptee，使得Adaptee不易扩展
    class AdapterClass(Interface, Adaptee):  # in C++, inherit publicly from Interface and privately from Adaptee
        def request(self):
            return self.specificRequest()

    # strategy2: object adapter
    # 其优缺点与class adapter正好相反
    class AdapterObject(Interface):
        def __init__(self, adaptee):
            self.adaptee = adaptee

        def request(self):
            return self.adaptee.specificRequest()

    # strategy3：pluggable adapter by using delegate
    # 委托模式是将某个类自身的部分功能委托给另一个类来实现，通常委托类可以完全地访问被委托类的属性
    class Target(Interface):
        def __init__(self):
            self.delegate = None

        def setDelegate(self, delegate):
            self.delegate = delegate

        def request(self):
            # do something before
            if self.delegate:
                self.delegate.subrequest(self)  # 部分功能由委托类来实现
                # do something after

    # 此方式中，委托类将同时扮演适配器的角色
    # 使用委托的意义在于，其从Interface中提取出了与Adaptee适配所需功能的最小交集
    # 这样就避免了Adapter直接继承于Interface
    class AdapterDelegate(Adaptee):
        def subrequest(self, target):
            # access target to do something related to Interface
            self.specificRequest()  # adapt Adaptee

    @staticmethod
    def testcase():
        # 调用的始终是Interface子类的接口
        # strategy1
        a1 = AdapterPattern.AdapterClass()
        a1.request()
        # strategy2
        at = AdapterPattern.Adaptee()
        a2 = AdapterPattern.AdapterObject(at)
        a2.request()
        # strategy3
        a3 = AdapterPattern.AdapterDelegate()
        tg = AdapterPattern.Target()
        tg.setDelegate(a3)
        tg.request()


if __name__ == '__main__':
    AdapterPattern.testcase()
