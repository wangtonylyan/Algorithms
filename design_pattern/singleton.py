# -*- coding: utf-8 -*-
# design pattern: singleton
# purpose: get the exactly same object instead of creating a new one

class SingletonPattern():
    # strategy: in python, use generator instead of static
    class Singleton():
        instance = None
        def __init__(self):
            self.instance = None
        @classmethod
        def getInstanceClassLevel(cls):
            cls.instance = SingletonPattern.Singleton()
            while True:
                yield cls.instance
        def getInstanceObjectLevel(self):
            self.instance = SingletonPattern.Singleton()
            while True:
                yield self.instance
        @staticmethod
        def getInstanceFunctionLevel():
            instance = SingletonPattern.Singleton()
            while True:
                yield instance

    @staticmethod
    def testcase():
        # create generators at each level (just for instance)
        clg = SingletonPattern.Singleton.getInstanceClassLevel()
        olg = SingletonPattern.Singleton().getInstanceObjectLevel()
        flg = SingletonPattern.Singleton.getInstanceFunctionLevel()
        # initialize the Singleton at each level
        clg.send(None)
        olg.send(None)
        flg.send(None)
        # call next() to get the Singleton every time
        for i in range(0, 5):
            print clg.next(), olg.next(), flg.next()


if __name__ == '__main__':
    SingletonPattern.testcase()
