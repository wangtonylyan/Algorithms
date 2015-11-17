# -*- coding: utf-8 -*-
# design pattern: prototype
# purpose: create a new object through clone
# 在Java中，java.lang.Object定义了一个protected方法clone()，供继承自Object的类定制clone操作
# 同时还提供了Cloneable接口，其将在运行时告知Java虚拟机所有实现了该接口的类都拥有安全的clone方法
# 否则调用clone()将会导致异常。于是任何类只需继承Object类并实现Cloneable接口，就可以支持原型模式了


import copy


class PrototypePattern():
    class Prototype():
        def __init__(self, pt=None):
            if pt:  # do clone
                assert (isinstance(pt, PrototypePattern.Prototype))
                # shallow copy
                self.data = copy.copy(pt.data)
                # or deep copy
                self.data = copy.deepcopy(pt.data)
            else:  # do create
                self.data = 'RandomString'

        def clone(self):
            # return a new instance cloned from myself
            return PrototypePattern.Prototype(self)

    @staticmethod
    def testcase():
        # create the proto
        proto = PrototypePattern.Prototype()
        # create the clone
        clone1 = PrototypePattern.Prototype(proto)  # use constructor function
        clone2 = proto.clone()  # or use clone function
        print proto.data, clone1.data, clone2.data


if __name__ == '__main__':
    PrototypePattern.testcase()
