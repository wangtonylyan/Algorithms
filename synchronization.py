# atomic primitives
# m=memory,v=value,e=expected
def atomic_load(m): pass  # get m


def atomic_store(m, v): pass  # set m = v


def atomic_exchange(m, v): pass  # set m = v, and return the old m


def atomic_compare_exchange(m, e, v): pass  # set m = (v if m == e else m), and return the old m


def atomic_fetch_inc(m): pass  # set m+=1, and return the old m


def atomic_fetch_des(m): pass  # set m-=1, and return the old m


def atomic_fetch_add(m, v): pass  # set m+=v, and return the old m


def atomic_fetch_sub(m, v): pass  # set m-=v, and return the old m


def memory_barrier(): pass  # synchronize data between cache and memory, and prevent statements forwards or backwards


class SpinLock():
    def __init__(self):
        self.lock = 0  # unlocked

    def try_acquire(self):
        return atomic_exchange(self.lock, 1)

    def acquire(self):
        while True:
            if not atomic_exchange(self.lock, 1):  # if the old self.lock equals 0
                break
            if self.lock:
                continue  # spinning
        memory_barrier()

    def release(self):
        memory_barrier()
        self.lock = 0
