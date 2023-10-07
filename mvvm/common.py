from typing import Callable, Generic, List, TypeVar, Union, Dict, Any

BaseType = Union[str, int, float, bool]

class EventArgs:
    pass

Ts = TypeVar('Ts')

Ta = TypeVar('Ta')

class Event(Callable[[Ts,Ta],None], Generic[Ts, Ta]):
    def __init__(self):
        self.invokelist:List[Callable[[Ts,Ta],None]] = []
    
    def __radd__(self, cb:Callable[[Ts,Ta],None]):
        self.invokelist.append(cb)
        
    def __rsub__(self, cb:Callable[[Ts,Ta],None]):
        self.invokelist.remove(cb)
    
    def __call__(self, sender:Ts, args:Ta):
        for c in self.invokelist:
            c(sender, args)
            
class ModelUpdatedEventArgs(EventArgs):
    def __init__(self):
        pass

class ModelBase:
    def __init__(self):
        self.updated:Event[ModelBase, ModelUpdatedEventArgs] = Event()