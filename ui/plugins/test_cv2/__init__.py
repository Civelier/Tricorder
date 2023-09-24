import tkinter as tk
import tkinter.ttk as ttk
import settings
from ui.plugin import ClosingHandler, PluginInfo, Plugin
from utils import EventInfo, EventQueue
from widgets.funky_btn import FunkyButton
from widgets.graphics import *
import cv2
from PIL import Image, ImageTk
from pygubu.widgets.scrolledframe import ScrolledFrame


class TestCV2Plugin(Plugin):
    def __init__(self, master:tk.Misc, mainEventQueue:EventQueue, **kw):
        super().__init__(master, mainEventQueue, **kw)
        btnSize = 80
        btnTextSize = 10

        # Menu bar
        self.menuBar = tk.Frame(self, width=kw['width'], height=btnSize)
        self.backBtn = FunkyButton(BtnInfo(BtnStyle.Style2, BtnShape.Multiply, BtnColor.Red), btnSize, btnTextSize, self.menuBar, "Back", self.back)
        self.backBtn.grid(column=0,row=0)
        self.menuBar.pack(side='top')
        self.menuBar.grid_propagate(False)

        # Main UI area
        self.mainFrame = tk.Frame(self, width=kw['width'],height=kw['height']-btnSize)
        self.scrollFrame = ScrolledFrame(self.mainFrame, scrolltype='both', width=kw['width'],height=kw['height']-btnSize)
        binfo = cv2.getBuildInformation()
        w = 0
        h = 0
        for l in binfo.splitlines():
            w = max(w, len(l))
            h+=1
        self.textBox = tk.Text(self.scrollFrame.innerframe, wrap='none', height=h, width=w)
        self.textBox.insert("0.0", binfo)
        self.textBox.pack(anchor="nw", expand=True, fill="both", side="top")
        self.scrollFrame.pack(anchor="nw", fill="both", side="top")
        self.scrollFrame.pack_propagate(False)
        self.mainFrame.pack(side='top')
        self.mainFrame.pack_propagate(False)

class TestCV2Settings(settings.PluginSettings):
    def __init__(self):
        super().__init__("TestCV2")

PLUGIN_INFO = PluginInfo("Test CV2", BtnInfo(BtnStyle.Style2, BtnShape.BubbleBigText, BtnColor.DarkGray), TestCV2Settings())
ENTRY_POINT = TestCV2Plugin