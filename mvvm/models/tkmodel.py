from typing import Dict, Union
from mvvm.common import BaseType
from mvvm.models.model import Model, ModelItem
import tkinter as tk

class TKModel(Model):
    def __init__(self, master:tk.Misc=None):
        self.master = master
        self.variables:Dict[str, Union[tk.StringVar, tk.IntVar, tk.DoubleVar, tk.BooleanVar]] = {}
        super().__init__()
        
    def create_property(self, name: str, default: BaseType, *, isPublic: bool = True, isReadonly: bool = False):
        if hasattr(self, name):
            return getattr(self, name)
        setattr(self, f'_{name}_notify', None)
        if isinstance(default, str):
            self.variables[name] = tk.StringVar(self.master, default, name)
        elif isinstance(default, int):
            self.variables[name] = tk.IntVar(self.master, default, name)
        elif isinstance(default, float):
            self.variables[name] = tk.DoubleVar(self.master, default, name)
        elif isinstance(default, bool):
            self.variables[name] = tk.BooleanVar(self.master, default, name)
        else:
            raise TypeError(message="Argument 'default' was not a basetype.")
        
        def getter(slf:TKModel):
            return slf.variables[name].get()
        
        def setter(slf:TKModel, value):
            old = slf.variables[name].get()
            if old != value:
                slf.variables[name].set(value)
                slf.on_property_changed(name, old, value)
        
        prop = property(getter, setter)
        
        item = ModelItem(default, name, self, isPublic, isReadonly)
        self.properties[name] = item
        
        
        return prop