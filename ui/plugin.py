import tkinter as tk
import tkinter.ttk as ttk
from utils import EventQueue
from widgets import *
import msgs
from settings import PluginSettings

class PluginInfo:
    def __init__(self, name:str, style:BtnInfo, settings:PluginSettings):
        self.name = name
        self.style = style
        self.msg = msgs.Messages(name)
        self.settings = settings

class ClosingHandler:
    def __init__(self):
        self.cancel = False

class Plugin(tk.Frame):
    def __init__(self, master:tk.Misc, mainEventQueue:EventQueue, **kw):
        super().__init__(master, **kw)
        self.eventQueue = mainEventQueue

    def on_closing(self, handler:ClosingHandler):
        pass

    def back(self):
        handler = ClosingHandler()
        self.on_closing(handler)
        if handler.cancel:
            return
        self.destroy()