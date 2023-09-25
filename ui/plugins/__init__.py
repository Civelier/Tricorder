import importlib
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import List, Tuple
from msgs import Messages
from ui.plugin import Plugin, PluginInfo


PluginsPath = Path('ui/plugins')

Plugins:List[ModuleType] = []
EntryPoints:List[Tuple[PluginInfo,Plugin]] = []
msg = Messages("Plugin loader")

def load():
    if len(Plugins) > 0:
        return
    for module in PluginsPath.iterdir():
        if module.is_dir() and module.name != '__pycache__':
            try:
                msg.info(f"Loading {module.name}.")
                md = importlib.import_module(f'.{module.name}', __name__)
                Plugins.append(md)
                if not md.PLUGIN_INFO.settings.hidden:
                    msg.info(f"Plugin {module.name} is hidden.")
                    EntryPoints.append((md.PLUGIN_INFO, md.ENTRY_POINT))
            except ModuleNotFoundError as e:
                msg.error("Missing module", f"Could not find module {e.name} in {module.name}\n{e}", True)


