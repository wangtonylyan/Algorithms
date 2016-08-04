# -*- coding: utf-8 -*-
# @problem: event-driven simulation
# @reference: <Algorithm_4Ed> P856


from data_structure.heap import MinHeap


class Particle():
    def __init__(self, (px, py), (vx, vy), radius, mass):
        self.px, self.py = px, py  # position
        self.vx, self.vy = vx, vy  # velocity
        self.radius = radius
        self.mass = mass
        self.cnt = 0

    def move(self, dt):
        self.px += self.vx * dt
        self.py += self.vy * dt

    def timeToHit(self, pb):
        pass

    def timeToHitHorizontalWall(self):
        pass

    def timeToHitVerticalWall(self):
        pass

    def bounceOff(self, pb):
        pass

    def bounceOffHorizontalWall(self):
        pass

    def bounceOffVerticalWall(self):
        pass


class Event():
    # a != None == b: collision between particle and vertical wall
    # a == None != b: collision between particle and horizontal wall
    # a != None != b: collision between two particles
    # a == None == b: redraw all particles
    def __init__(self, time, pa, pb):
        assert (time != None and time >= 0)
        assert (pa == None or isinstance(pa, Particle))
        assert (pb == None or isinstance(pb, Particle))
        self.time = time  # when this event occurs
        self.pa = pa
        self.pb = pb
        self.cntA = pa.cnt if pa != None else None
        self.cntB = pb.cnt if pb != None else None

    def isValid(self):
        if self.pa != None and self.cntA != self.pa.cnt:
            return False
        if self.pb != None and self.cntB != self.pb.cnt:
            return False
        return True


class Collision():
    def __init__(self, particles):
        assert (all(isinstance(x, Particle) for x in particles))
        self.particles = particles[:]
        self.evtQue = None

    def predict(self, pa, time, limit):
        assert (pa != None and isinstance(pa, Particle))
        for pb in self.particles:
            if pb != pa:
                dt = pa.timeToHit(pb)
                if dt != None and time + dt <= limit:
                    self.evtQue.push(Event(time + dt, pa, pb))
        dt = pa.timeToHitVerticalWall()
        if time + dt <= limit:
            self.evtQue.push(Event(time + dt, pa, None))
        dt = pa.timeToHitHorizontalWall()
        if time + dt <= limit:
            self.evtQue.push(Event(time + dt, None, pa))

    def simulate(self, limit, hz):
        # reset and restart
        time = 0
        self.evtQue = MinHeap(key=lambda x: x.time)
        self.evtQue.push(Event(time, None, None))
        map(lambda x: self.predict(x, time, limit), self.particles)
        # main loop
        while len(self.evtQue) > 0:
            # get the nearest event
            evt = self.evtQue.pop()
            if not evt.isValid():
                continue
            # update all particles
            for pa in self.particles:
                pa.move(evt.time - self.time)
            self.time = evt.time
            # handle collision and predict the future
            if evt.pa != None and evt.pb != None:
                evt.pa.bounceOff(evt.pb)
                self.predict(evt.pa, time, limit)
                self.predict(evt.pb, time, limit)
            elif evt.pa != None and evt.pb == None:
                evt.pa.bounceoffVerticalWall()
                self.predict(evt.pa, time, limit)
            elif evt.pa == None and evt.pb != None:
                evt.pb.bounceOffHorizontalWall()
                self.predict(evt.pb, time, limit)
            else:
                self.redraw(hz)

    def redraw(self, hz):
        pass


if __name__ == '__main__':
    cls = Collision()
    cls.simulate(10000, 10)
    print 'done'
