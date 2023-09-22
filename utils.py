from queue import Empty, Queue
import time
from typing import Callable


class StopWatch:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.init = time.time_ns()

    def __enter__(self):
        self.start = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.time_ns()

    @property
    def total_elapsed_ns(self):
        return self.init - time.time_ns()

    @property
    def elapsed_ns(self):
        return self.start - time.time_ns()
    
    @property
    def total_elapsed(self):
        return (self.init - time.time_ns()) / 1000000000

    @property
    def elapsed(self):
        return (self.start - time.time_ns()) / 1000000000
    

class EventInfo:
    def __init__(self):
        self.ns = 0
        self.nextrun = 0
        self.repeat = False
    
    def skip_time(self, seconds:float):
        self.nextrun = int(seconds*1000000000)
    
    def repeat_every(self, seconds:float):
        ns = int(seconds * 1000000000)
        if not self.repeat or self.ns != ns:
            self.repeat = True
            self.nextrun = time.time_ns() + ns
            self.ns = ns

    def exit(self):
        self.repeat = False
        self.ns = 0
        self.nextrun = 0
    
    def update(self):
        if self.repeat:
            # Ex:
            # now = 10
            # ns = 3
            # nextrun should be 12
            # offest = 10 % 3 = 1
            # nextrun = 10 - 1 + 3 = 12

            now = time.time_ns()
            # To catch up while debugging
            offset = (now - self.nextrun) % self.ns
            self.nextrun = now - offset + self.ns

ScheduledCallback = Callable[[EventInfo],None]

class EventQueue:
    HZ60=(1/60)

    def __init__(self):
        self._queue = Queue()
        
    def run(self):
        while True:
            try:
                info, func = self._queue.get_nowait()
                info:EventInfo
                func:ScheduledCallback
                
                if info.nextrun <= time.time_ns():
                    info.nextrun = 0
                    func(info)
                    if info.repeat or info.nextrun != 0:
                        info.update()
                        self._queue.put((info, func))
                else:
                    self._queue.put((info, func))
            except Empty:
                break

    def schedule(self, callback:ScheduledCallback, seconds:float=None, repeat:bool=False):
        info = EventInfo()
        if seconds!=None:
            if repeat:
                info.repeat_every(seconds)
            else:
                info.skip_time(seconds)
        info.repeat = repeat
        self._queue.put((info, callback))
    
    def event(self, seconds:float=None, repeat:bool=False):
        def hook(func:ScheduledCallback):
            self.schedule(func, seconds, repeat)
            def call(info:EventInfo):
                func(info)
            return call
        return hook

