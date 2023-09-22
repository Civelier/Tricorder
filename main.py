import tkinter as tk
from typing import Type
from ui.plugin import Plugin, PluginInfo
from widgets import *
from utils import EventInfo, EventQueue, ScheduledCallback
from widgets.wii_grid import WiiGridElement
from ui.plugins import load as load_plugins
import settings

RedHomeBtn = BtnInfo(BtnStyle.Style2, BtnShape.Camera, BtnColor.Blue)
SettingsBtnInfo = BtnInfo(BtnStyle.Style2, BtnShape.Cog, BtnColor.Blue)
ExitBtnInfo = BtnInfo(BtnStyle.Style2, BtnShape.Multiply, BtnColor.Red)
PluginsBtnInfo = BtnInfo(BtnStyle.Style2, BtnShape.ViewGrid, BtnColor.Orange)




def main():
    root = tk.Tk()
    eventManager = EventQueue()
    root.overrideredirect(True)
    max_width = root.winfo_screenwidth()
    max_height = root.winfo_screenheight()
    root.geometry("{0}x{1}+0+0".format(max_width, max_height))

    # home0 = FunkyButton(RedHomeBtn, 50, 8, root, text="Home0")
    # home0.place(x=0, y=0, anchor=tk.NW)

    # home1 = FunkyButton(RedHomeBtn, 70, 10, root, text="Home1")
    # home1.place(x=50, y=0, anchor=tk.NW)

    # home2 = FunkyButton(RedHomeBtn, 90, 12, root, text="Home2")
    # home2.place(x=0, y=70, anchor=tk.NW)

    def populate_plugins(grid:WiiGrid):
        from ui.plugins import EntryPoints
        load_plugins()

        # Create plugin btn command
        def show_plugin(ep:Type):
            def show():
                entrypoint:Plugin = ep(root, eventManager, width=max_width, height=max_height)
                entrypoint.place(x=0,y=0,width=max_width,height=max_height)

            return show

        for x in EntryPoints:
            pl, ep = x
            pl:PluginInfo
            grid.add_button(pl.style, pl.name, show_plugin(ep))

    
    
    def on_closing():
        root.destroy()
        exit()
    root.protocol('WM_DELETE_WINDOW', on_closing)

    def exit_btn():
        root.destroy()
        exit()
    
    def plugins_btn():
            
        plugins_grid = WiiGrid(root, max_width, max_height, 10, 5)
        populate_plugins(plugins_grid)
        def exit_plugins():
            plugins_grid.destroy()
        plugins_grid.add_button(ExitBtnInfo, 'Back', exit_plugins)
        plugins_grid.place(x=0,y=0,width=max_width,height=max_height)

    def settings_btn():
        pass

    btns = [
        WiiGridElement(ExitBtnInfo, "Exit", exit_btn),
        WiiGridElement(SettingsBtnInfo, "Settings", settings_btn),
        WiiGridElement(PluginsBtnInfo, "Plugins", plugins_btn),
    ]
    
    main_grid = WiiGrid(root, max_width, max_height, 10, 5)
    main_grid.place(x=0,y=0,width=max_width,height=max_height)
    main_grid.add_buttons(btns)


    @eventManager.event(0.01, True)
    def update_ui(info:EventInfo):
        root.update()
        root.mainloop(1)


    while True:
        eventManager.run()

if __name__ == "__main__":
    main()