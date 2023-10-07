from mvvm.common import *



Tb = TypeVar('Tb', int, float, str, bool, ModelBase)

class PropertyChangedEventArgs(EventArgs, Generic[Tb]):
    def __init__(self, name:str, oldVal:Tb, newVal:Tb):
        super().__init__()
        self.name = name
        self.oldVal = oldVal
        self.newVal = newVal
    
class Model(ModelBase):
    def __init__(self):
        super().__init__()
        self.properties:Dict[str, ModelItem] = {}
        self.propertyChanged:Event[Model, PropertyChangedEventArgs] = Event()
        
    def on_property_changed(self, name:str, oldValue:Tb, newValue:Tb):
        self.propertyChanged(self, PropertyChangedEventArgs(name, oldValue, newValue))
        self.updated(self, ModelUpdatedEventArgs())
    
    def bind_property(self, m1, m2):
        m1:ModelItem
        m2:ModelItem
        binder = Binder(m1, m2)
        binder.bind()
    
    def bind_all(self, other):
        other:Model
        for prop in self.properties.values():
            self.bind_property(prop, other.properties[prop.name])
            
    def unbind(self, item):
        item:ModelItem
        item.unbind()
        
    def unbind_all(self):
        for prop in self.properties.values():
            prop.unbind()
    
    def create_property(self, name:str, default:BaseType, *, isPublic:bool=True, isReadonly:bool=False):
        if hasattr(self, name):
            return getattr(self, name)
        setattr(self, f'_{name}_notify', None)
        def getter(slf:Model):
            return getattr(slf, f'_{name}')
        
        def setter(slf:Model, value):
            old = getattr(slf, f'_{name}')
            if old != value:
                setattr(slf, f'_{name}', value)
                getattr(slf, f'_{name}_notify', value)(slf, value)
                slf.on_property_changed(name, old, value)
        
        prop = property(getter, setter)
        
        item = ModelItem(default, name, self, isPublic=isPublic, isReadonly=isReadonly)
        self.properties[name] = item
        setattr(self, f'_{name}', item.default)
        
        return prop
    
class ModelItem:
    def __init__(
        self,
        fdefault:BaseType,
        name:str,
        parent:Model,
        *,
        isPublic:bool=True,
        isReadonly:bool=False,
    ):
        self.isPublic = isPublic
        self.isReadonly = isReadonly
        self.parent = parent
        self.default = fdefault
        self.name = name
        self.binder:Binder = None
        
    def bind(self, other):
        binder = Binder(self, other)
        binder.bind()
        
    def unbind(self):
        if self.binder != None:
            self.binder.unbind()
        
class BindingError(Exception):
    def __init__(self, source:ModelItem, other:ModelItem, because:str = None):
        self.message = f"Unable to bind {source.name} with {other.name}. "
        if because != None:
            self.message += because
        super().__init__(self.message)
    
class Binder:
    def __init__(self, m1:ModelItem, m2:ModelItem):
        self.m1 = m1
        self.m2 = m2
        
    def bind(self):
        if self.m1.binder != None:
            raise BindingError(self.m1, self.m2, f"{self.m1.name} is already binded.")
        if self.m2.binder != None:
            raise BindingError(self.m1, self.m2, f"{self.m2.name} is already binded.")
        self.m1.binder = self.m2.binder = self
        setattr(self.m1.parent, f"_{self.m1.name}_notify", lambda slf, val: self.p1_p2(val))
        setattr(self.m2.parent, f"_{self.m2.name}_notify", lambda slf, val: self.p2_p1(val))
        self.p1_p2(getattr(self.m1.parent, self.m1.name))
        
    def unbind(self):
        if self.m1.binder == None or self.m2.binder == None:
            return False
        self.m1.binder = None
        self.m2.binder = None
        setattr(self.m1.parent, f"_{self.m1.name}_notify", None)
        setattr(self.m2.parent, f"_{self.m2.name}_notify", None)
        
    def p1_p2(self, val):
        old = getattr(self.m2.parent, self.m2.name)
        if old != val:
            setattr(self.m2.parent, self.m2.name, val)
            
    def p2_p1(self, val):
        old = getattr(self.m1.parent, self.m1.name)
        if old != val:
            setattr(self.m1.parent, self.m1.name, val)
        
