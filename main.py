import tkinter as tk
from typing import List, Type
from ui.plugin import Plugin, PluginInfo
from widgets import *
from utils import EventInfo, EventQueue, ScheduledCallback
from widgets.wii_grid import WiiGridElement
from ui.plugins import load as load_plugins
import settings
from common_settings import BaseSettings
from remotelib import Context

RedHomeBtn = BtnInfo(BtnStyle.Style2, BtnShape.Camera, BtnColor.Blue)
SettingsBtnInfo = BtnInfo(BtnStyle.Style2, BtnShape.Cog, BtnColor.Blue)
ExitBtnInfo = BtnInfo(BtnStyle.Style2, BtnShape.Multiply, BtnColor.Red)
PluginsBtnInfo = BtnInfo(BtnStyle.Style2, BtnShape.ViewGrid, BtnColor.Orange)

CommonSettings = BaseSettings()

def main():
    from utils import eventManager
    from remotelib import ContextManager
    root = tk.Tk()
    root.overrideredirect(True)
    max_width = root.winfo_screenwidth()
    max_height = root.winfo_screenheight()
    root.geometry("{0}x{1}+0+0".format(max_width, max_height))
    pluginList = {}
    mainContext = Context("main", None, None)

    def populate_plugins(grid:WiiGrid):
        from ui.plugins import EntryPoints
        from remotelib import ContextManager
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
            pluginsCtx:Context = ContextManager.get_context('main.plugin')
            ctx = pluginsCtx.add_subcontext(pl.name, show_plugin(ep))
            grid.add_button(pl.style, pl.name, ctx)
            pluginList[pl.name] = ctx
            

    def populate_settings(propertylist):
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
            # grid.add_button(pl.style, pl.name, show_plugin(ep))

    
    
    def on_closing():
        root.destroy()
        ContextManager.stop()
        exit()
    root.protocol('WM_DELETE_WINDOW', on_closing)

    def exit_btn():
        root.destroy()
        ContextManager.stop()
        exit()
    mainContext.back = exit_btn
    
    def plugins_btn():
            
        plugins_grid = WiiGrid(root, max_width, max_height, 10, 5)
        populate_plugins(plugins_grid)
        def exit_plugins():
            plugins_grid.destroy()
        plugins_grid.add_button(ExitBtnInfo, 'Back', exit_plugins)
        plugins_grid.place(x=0,y=0,width=max_width,height=max_height)
        return plugins_grid
    pluginsContext = mainContext.add_subcontext('plugins', plugins_btn)

    def settings_btn():
        pass
    settingsContext = mainContext.add_subcontext('settings', settings_btn)

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

    def remote_control():
        plugins_grid:WiiGrid = None
        @eventManager.event(1)
        def open_plugins(info):
            global plugins_grid
            plugins_grid = plugins_btn()
        
        @eventManager.event(2)
        def open_simple_camera(info):
            pluginList['I2C Test']()

    # Start remote control
    ContextManager.active = mainContext
    ContextManager.start()
    
    while True:
        eventManager.run()

if __name__ == "__main__":
    main()