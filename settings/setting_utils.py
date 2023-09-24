from pathlib import Path
from typing import Any, Callable, Union
import toml

import msgs

BaseType = Union[str, bool, int, float]

PLUGINS_PATH = Path("ui/plugins")
PLUGINS_SETTINGS_PATH = Path("settings/plugins")

DEVICES_PATH = Path("devices")
DEVICES_SETTINGS_PATH = Path("settings/devices")

COMMON_SETTINGS_PATH = Path("settings/common")

msg = msgs.Messages("Settings")


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

class Settings:
    def __init__(self, path:Path):
        self.path = path
        self.cache = {}
        self.properties = {}
        self.cached = None

    def reset_defaults(self):
        for k, v in self.properties.items():
            v:setting
            self.set(k, v.default)
    
    def get(self, fullname:str):
        self.load()
        parts = fullname.split('.')
        name = parts[-1]
        parts.remove(name)
        cat = '.'.join(parts)
        msg.info(f"{self.path}")
        return get_at_category(self.properties[fullname].default, self.cache, cat, name)
    
    def set(self, fullname:str, val:BaseType):
        parts = fullname.split('.')
        name = parts[-1]
        parts.remove(name)
        cat = '.'.join(parts)
        self.cache = set_at_category(self.cache, cat, name, val)
        self.save()
    
    def load(self):
        if not self.path.exists():
            self.reset_defaults()
            self.save()
            return
        try:
            with self.path.open('r', encoding='utf-8') as rd:
                self.cache = toml.load(rd)
        except toml.TomlDecodeError as e:
            print(e)
            self.path.rename(self.path.as_posix()+'.broken')

    def save(self):
        if not self.path.exists():
            self.reset_defaults()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch()
        with self.path.open('w', encoding='utf-8') as wr:
            toml.dump(self.cache, wr)

class setting:
    def __init__(
        self,
        fdefault:BaseType,
        category:str,
        name:str,
        isPublic:bool=True,
        isReadonly:bool=False,
    ):
        self.isPublic = isPublic
        self.isReadonly = isReadonly
        self.parent:Settings = None
        self.category = category
        self.default = fdefault
        self.name = name
    def __call__(self, __fget:Callable[[Settings], BaseType]):
        def _get(s:Settings):
            if self.parent == None:
                self.parent = s
                self.add_to_parent()
            return __fget(s)
        return _get
    def add_to_parent(self):
        self.parent.properties[f'{self.category}.{self.name}'] = self
        fullname = '.'.join([self.category, self.name])
        v = get_at_category(None, self.parent.cache, self.category, self.name)
        if v == None:
            self.parent.set(fullname, self.default)


class PluginSettings(Settings):
    def __init__(self, pluginName:str):
        self.pluginName = pluginName
        super().__init__(PLUGINS_SETTINGS_PATH.joinpath(f'{pluginName}/active.toml'))
        self.load()

    @property
    @setting(False, 'plugin', 'hidden')
    def hidden(self) -> bool:
        return self.get('plugin.hidden')
    @hidden.setter
    def hidden(self, val:bool):
        self.set('plugin.hidden', val)
    
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
        
    
    @property
    @setting(1, 'base', 'val1')
    def val1(self) -> int:
        return self.get('base.val1')
    @val1.setter
    def val1(self, val:int):
        self.set('base.val1', val)

def test_val1():
    dat = test_data()
    dat.load()
    dat.save()

    # print(f"Name: {dat.properties['base.val1'].name}  Is public: {dat.properties['base.val1'].isPublic}  Value: {dat.val1}")
    print(f"Value: {dat.val1}")
    val = input("Insert value: ")
    dat.val1 = int(val)
    print(f"Value: {dat.val1}")


# test_val1()