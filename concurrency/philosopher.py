# -*- coding: utf-8 -*-

import threading, time, random


class AbstractPhilosopher(object):
    def __init__(self):
        self.philosophers = []

    def run(self):
        for ph in self.philosophers:
            ph.start()
        for ph in self.philosophers:
            ph.join()
        print 'pass:', self.__class__

    @staticmethod
    def main(first, second, block):
        for i in range(10):
            time.sleep(random.random())  # think for a while
            if first.acquire(block):
                try:
                    if second.acquire(block):
                        try:
                            # print threading.currentThread().getName(), 'is eating'
                            time.sleep(random.random())  # eat for a while
                        finally:
                            second.release()
                finally:
                    first.release()


# this will cause deadlock
class Philosopher1(AbstractPhilosopher):
    def __init__(self, num):
        super(Philosopher1, self).__init__()
        chopsticks = [threading.Lock() for i in range(num)]
        self.philosophers = [threading.Thread(target=self.main,
                                              args=[chopsticks[i], chopsticks[i + 1 if i < num - 1 else 0], True])
                             for i in range(num)]


# this will cause livelock
class Philosopher2(AbstractPhilosopher):
    def __init__(self, num):
        super(Philosopher2, self).__init__()
        chopsticks = [threading.Lock() for i in range(num)]
        self.philosophers = [threading.Thread(target=self.main,
                                              args=[chopsticks[i], chopsticks[i + 1 if i < num - 1 else 0], False])
                             for i in range(num)]


# acquiring locks in a global and fixed order will avoid deadlock
# order: 0,1,2,...,num-1
class Philosopher3(AbstractPhilosopher):
    def __init__(self, num):
        super(Philosopher3, self).__init__()
        chopsticks = [threading.Lock() for i in range(num)]
        for i in range(num - 1):
            self.philosophers.append(threading.Thread(target=self.main,
                                                      args=[chopsticks[i], chopsticks[i + 1], True]))
        self.philosophers.append(threading.Thread(target=self.main,
                                                  args=[chopsticks[0], chopsticks[num - 1], True]))


# use condition variable rather than lock
class Philosopher4(AbstractPhilosopher):
    class phThread(threading.Thread):
        def __init__(self):
            super(Philosopher4.phThread, self).__init__()
            self.condition = threading.Condition()
            self.left = None  # left philosopher's condition
            self.right = None  # right philosopher's condition

        # 由于同时持有左右两个锁，因此不存在获取锁的先后问题，也就不会导致死锁
        # 获取左右两个锁的方式都是非阻塞的，获取自身锁则利用条件变量的wait和notify接口
        def run(self):
            # 该循环停不下来，若每个线程都执行有限次循环的话，会出现如下情况的死锁：
            # t[i]完成所有循环并在返回前通知相邻的t[i-1]和t[i+1]
            # 但至多只有一个能够获得其自身的锁，而另一个将等待t[i-2]或t[i+2]的通知
            # 若在无限次循环下，该实现反而有助于平衡每个线程的执行
            while True:
                # i am going to think, so anyway, notify both neighbors first
                if self.left.acquire(False):
                    try:
                        self.left.notifyAll()
                    finally:
                        self.left.release()
                if self.right.acquire(False):
                    try:
                        self.right.notifyAll()
                    finally:
                        self.right.release()
                # think for a while
                time.sleep(random.random())

                # i am going to eat, so both neighbors can't eat meanwhile
                if self.condition.acquire():
                    try:
                        while True:
                            left = self.left.acquire(False)
                            right = self.right.acquire(False)
                            if left and right:
                                break
                            if left:
                                self.left.release()
                            if right:
                                self.right.release()
                            self.condition.wait()
                        try:
                            # eat for a while
                            print threading.currentThread().getName(), 'is eating'
                            time.sleep(random.random())
                            self.left.notifyAll()
                            self.right.notifyAll()
                        finally:
                            self.left.release()
                            self.right.release()
                    finally:
                        self.condition.release()

    def __init__(self, num):
        super(Philosopher4, self).__init__()
        self.philosophers = [Philosopher4.phThread() for i in range(num)]
        for i in range(num):
            self.philosophers[i].left = self.philosophers[i - 1 if i > 0 else 0].condition
            self.philosophers[i].right = self.philosophers[i + 1 if i < num - 1 else 0].condition


class Philosopher5(AbstractPhilosopher):
    class phThread(threading.Thread):
        def __init__(self):
            super(Philosopher5.phThread, self).__init__()

        def run(self):
            pass

    def __init__(self, num):
        super(Philosopher5, self).__init__()


if __name__ == '__main__':
    num = 5  # number of threads
    for cls in [Philosopher1, Philosopher2, Philosopher3, Philosopher4, Philosopher5]:
        ph = cls(num)
        ph.run()
