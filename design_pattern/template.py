# -*- coding: utf-8 -*-
# design pattern: template method
# 模板方法模式：使得子类可以不改变一个算法的结构，就可以重定义（即扩展）该算法得某些特定步骤
# 1）该模式充分体现了the Hollywood principle：Don't call us, we'll call you
# 在好莱坞，把简历递交给演艺公司后就只有回家等待。演艺公司对整个项目拥有完全控制，
# 演员只能被动式的接受公司的差使，在需要的环节中，完成自己的演出。
# 2）由父类完全控制着子类的逻辑,这体现的是控制反转（IoC）。
# 子类可以定制可变的细节部份，但主体上必须继承并遵循于父类的业务逻辑。
# 3）该模式也是对于继承和多态的一种具体实践

class TemplateMethodPattern():
    # strategy1: 常规的实现方式，应用例如Java中Thread类的run方法
    class Template1():
        def __init__(self):
            self.flag = 0  # 提供子类该变量以定制模板中的局部逻辑
        def templateMethod(self):  # 此方法在Java中最好被定义成final，以避免被子类修改
            # do something before
            if self.flag:
                self.run()  # defined by subclass
            # do something after
        def run(self):
            pass
    # this class must not override the template method
    class Subprocess1(Template1):
        def __init__(self):
            self.flag = 1
        def run(self):
            print 'do something'

    # strategy2: 一方面，父类与子类不再直接耦合，使用接口代替了继承
    # 另一方面，对子类也隐藏了父类，避免子类覆盖模板方法，更为安全
    class SubprocessInterface():  # interface
        def run(self):
            pass
    class Template2():
        def templateMethod(self, subprocess):
            # do something before
            subprocess.run()
            # do something after
    class Subprocess2(SubprocessInterface):
        def run(self):
            print 'do something'

    @staticmethod
    def testcase():
        s1 = TemplateMethodPattern.Subprocess1()
        s1.templateMethod()  # 通过具体实现类调用模板方法
        s2 = TemplateMethodPattern.Subprocess2()
        t2 = TemplateMethodPattern.Template2()
        t2.templateMethod(s2)  # 通过模板方法类调用模板方法


if __name__ == '__main__':
    TemplateMethodPattern.testcase()
