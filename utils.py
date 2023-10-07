from queue import Empty, Queue
import time
from typing import Callable


class StopWatch:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.init = time.time()

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end = time.time()

    @property
    def total_elapsed(self):
        return (self.init - time.time())

    @property
    def elapsed(self):
        return (self.start - time.time())
    

class EventInfo:
    def __init__(self):
        self.seconds = 0
        self.nextrun = 0
        self.repeat = False
    
    def skip_time(self, seconds:float):
        self.nextrun = time.time() + seconds
    
    def repeat_every(self, seconds:float):
        if not self.repeat or self.seconds != seconds:
            self.repeat = True
            self.nextrun = time.time() + seconds
            self.seconds = seconds

    def exit(self):
        self.repeat = False
        self.seconds = 0
        self.nextrun = 0
    
    def update(self):
        if self.repeat:
            # Ex:
            # now = 10
            # ns = 3
            # nextrun should be 12
            # offest = 10 % 3 = 1
            # nextrun = 10 - 1 + 3 = 12

            now = time.time()
            # To catch up while debugging
            offset = (now - self.nextrun) % self.seconds
            self.nextrun = now - offset + self.seconds

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
                
                if info.nextrun <= time.time():
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

eventManager = EventQueue()

