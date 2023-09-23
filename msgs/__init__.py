from logging import *
import tkinter
from typing import AnyStr
from tkinter import messagebox as msg
import utils

class Messages:
    def __init__(self, module:str):
        self.module = module
        self._logger = Logger(self.module)
    
    def error(self, title:str = None, message:str=None, as_event:bool=False, **options):
        from utils import eventManager
        self._logger.error(f"{title}: {message}")
        if as_event:
            def fcall(info:utils.EventInfo):
                msg.showerror(title, message=message,**options)
            eventManager.schedule(fcall)
        else:
            msg.showerror(title, message=message,**options)

    def warning(self, title:str = None, message:str=None, as_event:bool=False, **options):
        from utils import eventManager
        self._logger.warning(f"{title}: {message}")
        if as_event:
            def fcall(info:utils.EventInfo):
                msg.showwarning(title, message, **options)
            eventManager.schedule(fcall)
        else:
            msg.showwarning(title, message, **options)
