# -*- coding: utf-8 -*-
# design pattern: proxy & decorator
# 两种模式的实现非常相似，但两者的设计目的是截然不同的
# 前者introduces a level of indirection when accessing an object，提供控制某个对象的访问管理
# 后者更注重扩展：装饰类可以与被装饰类处于同一个继承层次，通过装饰而不是继承之，实现更为灵活的扩展

import inspect


# 在实践中，关于被代理对象的访问管理还可包括消息的预/后处理、过滤、转发等功能
class ProxyPattern():
    class AbstractSubject():  # interface for both Subject and Proxy
        def doSomething(self):
            pass

    # strategy1: 静态代理
    class SubjectStatic(AbstractSubject):
        def doSomething(self):
            print 'do something via proxy'
    class ProxyStatic(AbstractSubject):
        def __init__(self, subject):
            # Proxy can also be bound to a Subject class rather than an object
            self.subject = subject
        # you can also specify the Subject as a parameter of this method
        def doSomething(self):
            return self.subject.doSomething()

    # strategy2: 强制代理，直接调用对象的接口将会导致异常，且代理将由对象而非用户创建
    # 非强制，则还是允许直接调用对象本身的接口
    # 优点是用户无需知道该使用哪个代理类
    class SubjectCompulsive(AbstractSubject):
        def __init__(self):
            self.proxy = None
        def getProxy(self):
            if self.proxy == None:
                self.proxy = ProxyPattern.ProxyStatic(self)
            return self.proxy
        def doSomething(self):
            # use python inspection to check if this is called via Proxy
            # 若语言中没有此类语法机制，通常只能检查self.proxy是否为None，以确认用户是否已尝试获取了代理
            if 'self.subject.doSomething()' in inspect.stack()[1][4][0] and self.proxy:
                print 'do something via proxy'
            else:
                raise Exception('This is compulsive proxy pattern!')

    # strategy3: 虚拟代理，维护的是被代理对象的标识（而非其本身）
    # 但最终还是将通过标识获取到被代理对象，并实现对于用户的接口
    # 即虚拟代理与被代理者之间又建立起了一层indirection

    # strategy4: 动态代理，利用动态语法机制使得一个代理类可以动态地代理多种类
    class ProxyDynamic():  # 无需绑定任何接口
        def __init__(self):
            self.subject = None  # 被代理类的对象
            self.methods = []
        def newProxyInstance(self, cls):
            self.methods = []  # reset
            self.subject = apply(cls, ())  # 创建一个被代理类的对象
            for m in dir(self.subject):  # 获取该类的所有接口信息
                if not m.startswith('_') and not m.startswith('__') and not m.endswith('_') \
                        and callable(getattr(self.subject, m)):
                    self.methods.append(m)
        # 此内置方法可以截获所有对于当前类中不存在的属性或方法的调用
        def __getattr__(self, name):
            if name in self.methods and self.subject:
                if hasattr(self.subject, name) and callable(getattr(self.subject, name)):
                    return getattr(self.subject, name)
            return AttributeError()

    @staticmethod
    def testcase():
        # strategy1: static proxy
        s = ProxyPattern.SubjectStatic()  # create the Subject
        p = ProxyPattern.ProxyStatic(s)  # create its Proxy
        p.doSomething()  # access Subject via Proxy
        # strategy2: compulsive proxy
        s = ProxyPattern.SubjectCompulsive()
        p = s.getProxy()
        p.doSomething()
        # s.doSomething() #this will cause an exception
        # strategy3: virtual proxy
        # strategy4: dynamic proxy
        p = ProxyPattern.ProxyDynamic()
        p.newProxyInstance(ProxyPattern.SubjectStatic)
        p.doSomething()  # Proxy就可以直接调用被代理对象的方法了


class DecoratorPattern():
    # 装饰类与被装饰类都继承于此接口
    class AbstractSubject():
        def doSomething(self):
            pass
    class Subject(AbstractSubject):
        def doSomething(self):
            print 'do something via decorator'

    # Decorator的继承树是可选的，可以直接用单个Decorator类实现
    class AbstractDecorator(AbstractSubject):
        def __init__(self, subject):
            self.subject = subject
        def doSomething(self):  # this method can be purely virtual
            self.subject.doSomething()  # just for instance, it acts like Proxy
    class Decorator(AbstractDecorator):
        def __init__(self, subject):
            DecoratorPattern.AbstractDecorator.__init__(self, subject)
        def doSomething(self):
            # do anything before
            self.subject.doSomething()
            # do anything after

    @staticmethod
    def testcase():
        s = DecoratorPattern.Subject()
        d = DecoratorPattern.Decorator(s)
        d.doSomething()


if __name__ == '__main__':
    ProxyPattern.testcase()
    DecoratorPattern.testcase()
