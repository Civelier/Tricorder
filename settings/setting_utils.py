from email.policy import default
from pathlib import Path
from typing import Any, Callable, Union, Dict
import toml
import mvvm

import msgs
from mvvm.models.model import ModelItem, PropertyChangedEventArgs

BaseType = Union[str, bool, int, float]

PLUGINS_PATH = Path("ui/plugins")
PLUGINS_SETTINGS_PATH = Path("settings/plugins")

DEVICES_PATH = Path("devices")
DEVICES_SETTINGS_PATH = Path("settings/devices")

COMMON_SETTINGS_PATH = Path("settings/common")

msg = msgs.Messages("Settings")


def fullname_to_cat_name(fullname:str):
    full = fullname.split('.')
    name = full[-1]
    full.remove(name)
    cat = '.'.join(full)
    return cat, name

def cat_name_to_fullname(cat:str, name:str):
    return '.'.join([cat,name])

def set_at_category(d:dict, category:str, name:str, value):
    """Set value at a specific level in dict (toml style) and create sub dictionaries as needed

    Args:
        d (dict): Dict to iterate over
        category (str): '.' separated category name
        name (str): Variable name
        value (Union[BaseType,Dict]): Value to set

    Returns:
        Dict[str, Any]: The resulting dict with the new categories added
    """

    if category == "": # At base level
        d[name] = value # Set value at base level
        return d
    categories = category.split('.')
    cat = categories[0] # Get the next category
    categories.remove(cat) # Get the categories for the next recursion
    if d[cat] == None: # If dict doesn't exist, create it
        d[cat] = {}
    d[cat] = set_at_category(d[cat], '.'.join(categories), name, value)
    return d

def get_at_category(default:BaseType, d:dict, category:str, name:str):
    """Set value at a specific level in dict (toml style) and create sub dictionaries as needed

    Args:
        d (dict): Dict to iterate over
        category (str): '.' separated category name
        name (str): Variable name
        value (Union[BaseType,Dict]): Value to set

    Returns:
        Dict[str, Any]: The resulting dict with the new categories added
    """
    if category == "": # At base level
        try:
            return d[name]
        except KeyError:
            key = '.'.join([category,name])
            return default
    categories = category.split('.') 
    cat = categories[0] # Get the next category
    categories.remove(cat) # Get the categories for the next recursion
    try:
        d[cat] == None # If dict doesn't exist, create it
    except KeyError:
        d[cat] = {}
    return get_at_category(default, d[cat], '.'.join(categories), name)

class Settings(mvvm.ModelBase):
    NOT_INITIALIZED = 0
    INITIALIZING = 1
    INITIALIZED = 2
    def __init__(self, path:Path):
        super().__init__()
        self.path = path
        self.cache = {}
        self.properties:Dict[str, ModelItem] = {}
        self._state = Settings.NOT_INITIALIZED
        self.propertyChanged:mvvm.Event[Settings, PropertyChangedEventArgs] = mvvm.Event()
    
    def on_property_changed(self, name:str, oldValue, newValue):
        self.propertyChanged(self, mvvm.PropertyChangedEventArgs(name, oldValue, newValue))
        self.updated(self, mvvm.ModelUpdatedEventArgs())
    
    def bind_property(self, m1, m2):
        m1:mvvm.ModelItem
        m2:mvvm.ModelItem
        binder = mvvm.Binder(m1, m2)
        binder.bind()
    
    def bind_all(self, other):
        other:mvvm.Model
        for prop in self.properties.values():
            self.bind_property(prop, other.properties[prop.name])
            
    def unbind(self, item):
        item:mvvm.ModelItem
        item.unbind()
        
    def unbind_all(self):
        for prop in self.properties.values():
            prop.unbind()
    
    def create_property(self, name:str, fullname:str, default:BaseType, *, isPublic:bool=True, isReadonly:bool=False):
        s = setting(default, name, fullname, self, isPublic=isPublic, isReadonly=isReadonly)
        s.add_to_parent()
        
        setattr(self, f'_{s.name}_notify', None)
        # If the property is already attached, get the 
        if hasattr(self, s.name):
            return getattr(self, s.name)
        def setter(slf:Settings, value):
            old = slf.get(fullname)
            if old != value:
                slf.set(fullname, value)
                getattr(slf, f'_{name}_notify', value)(slf, value)
                slf.on_property_changed(s.name, old, value)
        
        prop = property(lambda self: self.get(fullname), setter)
        return prop
        
    def reset_defaults(self):
        for k, v in self.properties.items():
            v:setting
            self.set(k, v.default)
    
    def get(self, fullname:str):
        cat, name = fullname_to_cat_name(fullname)
        old = get_at_category(self.properties[fullname].default, self.cache, cat, name)
        self.load()
        val = get_at_category(self.properties[fullname].default, self.cache, cat, name)
        if old != val:
            self.set(fullname, val)
        return val
    
    def set(self, fullname:str, val:BaseType):
        cat, name = fullname_to_cat_name(fullname)
        
        # Get property info
        s = self.properties[fullname]
        
        # Get old value
        old = get_at_category(s.default, self.cache, cat, name)
        if old != val:
            self.cache = set_at_category(self.cache, cat, name, val)
            self.save()
            self.on_property_changed(s.name, old, val)
    
    def load(self):
        if not self.path.exists() and self._state == self.NOT_INITIALIZED:
            self._state = self.INITIALIZING
            self.reset_defaults()
            self._state = self.INITIALIZED
            return
        try:
            with self.path.open('r', encoding='utf-8') as rd:
                self.cache = toml.load(rd)
                self._state = self.INITIALIZED
        except toml.TomlDecodeError as e:
            print(e)
            self.path.rename(self.path.as_posix()+'.broken')

    def save(self):
        if not self.path.exists() and self._state == self.NOT_INITIALIZED:
            self._state = self.INITIALIZING
            self.reset_defaults()
            self._state = self.INITIALIZED
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch()
        with self.path.open('w', encoding='utf-8') as wr:
            toml.dump(self.cache, wr)
            self._state = self.INITIALIZED

class setting(ModelItem):
    def __init__(
        self,
        fdefault:BaseType,
        name:str,
        fullname:str,
        parent:Settings,
        *,
        isPublic:bool=True,
        isReadonly:bool=False,
    ):
        super().__init__(fdefault, name, parent, isPublic=isPublic, isReadonly=isReadonly)
        self.fullname = fullname
        self.parent:Settings

    def add_to_parent(self):
        cat, name = fullname_to_cat_name(self.fullname)
        self.parent.properties[self.fullname] = self
        v = get_at_category(None, self.parent.cache, cat, name)
        if v == None:
            self.parent.set(self.fullname, self.default)

class PluginSettings(Settings):
    def __init__(self, pluginName:str):
        self.pluginName = pluginName
        super().__init__(PLUGINS_SETTINGS_PATH.joinpath(f'{pluginName}/active.toml'))
        PluginSettings.hidden = self.create_property('plugin.hidden', 'hidden', False)
        PluginSettings.version = self.create_property('plugin.version', 'version', '1.0', isReadonly=True)

class DeviceSettings(Settings):
    def __init__(self, deviceName:str):
        self.deviceName = deviceName
        super().__init__(DEVICES_SETTINGS_PATH.joinpath(f'{deviceName}/active.toml'))
        self.load()

class CommonSettings(Settings):
    def __init__(self, componentName:str):
        self.componentName = componentName
        super().__init__(COMMON_SETTINGS_PATH.joinpath(f'{componentName}/active.toml'))
        self.load()

class test_data(CommonSettings):
    def __init__(self):
        super().__init__('TestData')
        test_data.val1 = self.create_property('val1', 'base.val1', 4)
        self.load()
    
class test_model(mvvm.Model):
    def __init__(self):
        super().__init__()
        test_model.val1 = self.create_property('val1', 4)

def test_val1():
    dat = test_data()
    dat.load()
    dat.save()

    # print(f"Name: {dat.properties['base.val1'].name}  Is public: {dat.properties['base.val1'].isPublic}  Value: {dat.val1}")
    print(f"Value: {dat.val1}")
    val = input("Insert value: ")
    dat.val1 = int(val)
    print(f"Value: {dat.val1}")

def test_bind():
    dat = test_data()
    modl = test_model()
    
    dat.bind_all(modl)
    
    dat.load()
    dat.save()

    print(f"dat: {dat.val1}\tmodl: {modl.val1}")
    dat.val1 += 1
    print(f"dat: {dat.val1}\tmodl: {modl.val1}")
    modl.val1 += 5
    print(f"dat: {dat.val1}\tmodl: {modl.val1}")

test_bind()
# test_val1()