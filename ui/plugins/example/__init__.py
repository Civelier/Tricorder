import tkinter as tk
import tkinter.ttk as ttk
import settings
from ui.plugin import PluginInfo, Plugin
from utils import EventQueue
from widgets.funky_btn import FunkyButton
from widgets.graphics import *

class ExampleSettings(settings.PluginSettings):
    def __init__(self):
        super().__init__("Example")
        

PLUGIN_INFO = PluginInfo("Example", BtnInfo(BtnStyle.Style2, BtnShape.Tags, BtnColor.Orange), ExampleSettings())


class ExamplePlugin(Plugin):
    def __init__(self, master:tk.Misc, mainEventQueue:EventQueue, **kw):
        super().__init__(master, mainEventQueue, **kw)
        self.backBtn = FunkyButton(BtnInfo(BtnStyle.Style2, BtnShape.Multiply, BtnColor.Red), 80, 10, self, "Back", self.back)
        self.backBtn.grid(column=0,row=0)
        self.errBtn = FunkyButton(BtnInfo(BtnStyle.Style2, BtnShape.Checklist, BtnColor.Orange), 80, 10, self, "Test error", self.test_error)
        self.errBtn.grid(column=1,row=0)
        self.text = tk.Label(self, text=f"Module: {__package__}")
        self.text.grid(column=0,row=1)
        self.grid_propagate(False)

    
    def test_error(self):
        PLUGIN_INFO.msg.error("Testing error", "This is an error message")


ENTRY_POINT = ExamplePlugin