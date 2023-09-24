import importlib
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import List, Tuple
from ui.plugin import Plugin, PluginInfo

PluginsPath = Path('ui/plugins')

Plugins:List[ModuleType] = []
EntryPoints:List[Tuple[PluginInfo,Plugin]] = []

def load():
    if len(Plugins) > 0:
        return
    for module in PluginsPath.iterdir():
        if module.is_dir() and module.name != '__pycache__':
            md = importlib.import_module(f'.{module.name}', __name__)
            Plugins.append(md)
            if not md.PLUGIN_INFO.settings.hidden:
                EntryPoints.append((md.PLUGIN_INFO, md.ENTRY_POINT))


