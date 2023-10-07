from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk
from cinput import intChoice, menuInput
import settings
from ui.plugin import ClosingHandler, PluginInfo, Plugin
from utils import EventInfo, EventQueue
from widgets.funky_btn import FunkyButton
from widgets.graphics import *

class I2CSettings(settings.PluginSettings):
    def __init__(self):
        super().__init__("I2C Test")
        I2CSettings.rate = self.create_property('rate', 'master.rate', 400000)
        I2CSettings.deviceAddress = self.create_property('deviceAddress', 'device.address', 0x00)
        

PLUGIN_INFO = PluginInfo("I2C Test", BtnInfo(BtnStyle.Style2, BtnShape.Linked, BtnColor.Purple), I2CSettings())


class I2CTest(Plugin):
    def __init__(self, master:tk.Misc, mainEventQueue:EventQueue, **kw):
        super().__init__(master, mainEventQueue, **kw)
        self.backBtn = FunkyButton(BtnInfo(BtnStyle.Style2, BtnShape.Multiply, BtnColor.Red), 80, 10, self, "Back", self.back)
        self.backBtn.grid(column=0,row=0)
        self.errBtn = FunkyButton(BtnInfo(BtnStyle.Style2, BtnShape.Checklist, BtnColor.Orange), 80, 10, self, "Test error", self.test_error)
        self.errBtn.grid(column=1,row=0)
        self.text = tk.Label(self, text=f"Module: {__package__}")
        self.text.grid(column=0,row=1)
        self.grid_propagate(False)
        self.run = True
        self.done = False
        self.devices = []
        self.menus = {
            'Discover': self.discover,
            'Select device': self.select_device
        }
        self.thread = Thread(target=self.run_thread)
        self.thread.start()
    
    def select_device(self):
        r, opt = intChoice("Choose device", self.devices)
        if r == 0:
            return
        PLUGIN_INFO.settings.deviceAddress = opt
    
    def discover(self):
        self.devices.clear()
        
    
    def run_thread(self):
        while self.run:
            menuInput(self.menus, "I2C Test")
    
    def on_closing(self, handler: ClosingHandler):
        self.run = False
        self.thread.join()
        return super().on_closing(handler)    
    
        
    
    def test_error(self):
        PLUGIN_INFO.msg.error("Testing error", "This is an error message")


ENTRY_POINT = I2CTest