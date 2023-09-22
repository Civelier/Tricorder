import tkinter as tk
import tkinter.ttk as ttk
from ui.plugin import PluginInfo, Plugin
from utils import EventQueue
from widgets.funky_btn import FunkyButton
from widgets.graphics import *


class ExamplePlugin(Plugin):
    def __init__(self, master:tk.Misc, mainEventQueue:EventQueue, **kw):
        super().__init__(master, mainEventQueue, **kw)
        self.backBtn = FunkyButton(BtnInfo(BtnStyle.Style2, BtnShape.Multiply, BtnColor.Red), 80, 10, self, "Back", self.back)
        self.backBtn.grid(column=0,row=0)
        self.grid_propagate(False)


PLUGIN_INFO = PluginInfo("Example", BtnInfo(BtnStyle.Style2, BtnShape.Tags, BtnColor.Orange))
ENTRY_POINT = ExamplePlugin