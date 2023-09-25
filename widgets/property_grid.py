import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame

class NewprojectWidget(ttk.Frame):
    def __init__(self, master=None, **kw):
        super(NewprojectWidget, self).__init__(master, **kw)
        self.scroll = ScrolledFrame(self, scrolltype="both")
        self.scroll.configure(usemousewheel=False)
        self.mainframe = ttk.Frame(self.scroll.innerframe)
        self.mainframe.configure(height=200, width=200)
        combobox1 = ttk.Combobox(self.mainframe)
        combobox1.grid(column=2, row=0, sticky="ew")
        label1 = ttk.Label(self.mainframe)
        label1.configure(anchor="center", text='label1')
        label1.grid(column=0, row=0, sticky="ew")
        separator2 = ttk.Separator(self.mainframe)
        separator2.configure(orient="vertical")
        separator2.grid(column=1, padx=5, row=0)
        self.mainframe.pack(side="top")
        self.scroll.pack(side="top")
        self.configure(height=200, width=200)
        self.pack(side="top")

if __name__ == "__main__":
    root = tk.Tk()
    widget = NewprojectWidget(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
