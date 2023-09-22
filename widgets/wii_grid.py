import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable, List, Tuple, Union
from widgets.graphics import BtnColor, BtnInfo, BtnShape, BtnStyle
from widgets.funky_btn import FunkyButton

class WiiGridElement:
    def __init__(self, info:BtnInfo, text:str="", command:Callable=None):
        self.info = info
        self.text = text
        self.command = command


class WiiGrid(ttk.Frame):
    def __init__(self, master:Union[tk.Misc, None], width:int, height:int, textHeight:int, columns:int, **kw):
        super().__init__(master, **kw)
        self.configure(width=width, height=height)
        self.textHeight = textHeight
        self.columns = columns
        self.btns = []
        
    def get_next_pos(self):
        c = len(self.btns) % self.columns
        r = (len(self.btns) - c) // self.columns
        return c, r

    def add_button(self, info:BtnInfo, text:str="", command:Callable=None):
        btn = FunkyButton(info, self['width'] // self.columns, self.textHeight, self, text, command)
        c, r = self.get_next_pos()
        btn.grid(column=c, row=r)
        btn.grid_propagate(False)
        self.btns.append(btn)

    def add_buttons(self, btns:List[WiiGridElement]):
        for btn in btns:
            self.add_button(btn.info, btn.text, btn.command)