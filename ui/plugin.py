import tkinter as tk
import tkinter.ttk as ttk
from typing import Generic, TypeVar, Union
from utils import EventQueue
from widgets import *
import msgs
from settings import PluginSettings
from remotelib import Context

T = TypeVar('T')

class PluginInfo(Generic[T]):
    def __init__(self, name:str, style:BtnInfo, settings:Union[T,PluginSettings]):
        from remotelib import ContextManager
        self.name = name
        self.style = style
        self.msg = msgs.Messages(name)
        self.settings = settings
        self.context = ContextManager.get_context(f'main.plugins.{name}')

class ClosingHandler:
    def __init__(self):
        self.cancel = False

class Plugin(tk.Frame):
    def __init__(self, master:tk.Misc, mainEventQueue:EventQueue, context:Context, **kw):
        super().__init__(master, **kw)
        self.eventQueue = mainEventQueue
        self.context = context

    def on_closing(self, handler:ClosingHandler):
        pass

    def back(self):
        handler = ClosingHandler()
        self.on_closing(handler)
        if handler.cancel:
            return
        self.destroy()