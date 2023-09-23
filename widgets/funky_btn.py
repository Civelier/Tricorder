import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from widgets.graphics import BtnColor, BtnInfo, BtnShape, BtnStyle

class FunkyButton(ttk.Frame):
    def __init__(self, info:BtnInfo, size:int, textSize:int, master:tk.Misc = None, text="", command=None):
        self._info = info
        img = self._info.with_size((size, size))
            
        super().__init__(master)

        self.btn = ttk.Button(self)
        if img != None:
            self.img = img
        self.lbl = ttk.Label(self)
        fg = '#' + (hex(self._info.fg_color)[2:].zfill(6))
        bg = '#' + (hex(self._info.bg_color)[2:].zfill(6))
        ft = "{Bahnschrift} " + str(textSize) + " {}"
        self.lbl.configure(anchor="nw", text=text, font=ft, justify=tk.CENTER, foreground=fg, background=bg, takefocus=False)
        # self.lbl.pack(side="bottom")
        self.lbl.place(y=5, x=5)
        if img != None:
            self.btn.configure(image=self.img, takefocus=False, command=command)
        else:
            self.btn.configure(takefocus=False, command=command)
        self.btn.pack(side="top")
        self.configure(height=size+textSize, width=size, takefocus=False)


        
