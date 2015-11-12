# -*- coding: utf-8 -*-
# design pattern: prototype
# purpose: create a new object through clone

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
