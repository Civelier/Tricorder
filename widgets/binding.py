from typing import Callable, Union

BaseType = Union[str, bool, int, float]


class PropertyBinder:
    def __init__(self):
        self.onChange = []
        self.lastValue = None

    def attach(self, func:Callable[[BaseType],None]):
        self.onChange.append(func)
    
    def on_changed(self, value:BaseType):
        if self.lastValue != value:
            self.lastValue = value
            for c in self.onChange:
                c(value)