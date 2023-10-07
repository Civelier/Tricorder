from threading import Thread
from typing import Callable, Dict, overload
from cinput import intChoice

class _ContextManager:
    def __init__(self):
        self.active:Context = None
        self.contexts:Dict[str, Context] = {}
        self.thread = Thread(None, self.run)
        self._running = False
        
    @overload
    def get_context(self, id:str):
        return self.contexts[id]
    
    def run(self):
        while self._running:
            self.active.manage()
    
    def start(self):
        self._running = True
        self.thread.start()
    
    def stop(self):
        self._running = False
        self.thread.join()
  
ContextManager = _ContextManager()

class Context:
    def __init__(self, name:str, parent, callback:Callable, *args, **kwargs):
        self.name = name
        self.cb = callback
        self.args = args
        self.kwargs = kwargs
        self.subcontexts:Dict[str, Context] = {}
        self.back:Callable = None
        self.parent = parent
        
    def __call__(self):
        if self.cb == None:
            return
        self.cb(*self.args, **self.kwargs)
        
    def add_subcontext(self, name:str, callback:Callable, *args, **kwargs):
        c = Context(name, self, callback, *args, **kwargs)
        self.subcontexts[name] = c
        ContextManager.contexts['.'.join([self.name, name])] = c
        return c
    
    def manage(self):
        r, opt = intChoice(self.name, list(self.subcontexts.keys()))
        if r == 0:
            if self.parent == None:
                exit()
            ContextManager.active = self.parent
            if self.back != None:
                self.back()
            return
        ContextManager.active = self.subcontexts[opt]
    
    def step_out(self):
        ContextManager.active = self.parent