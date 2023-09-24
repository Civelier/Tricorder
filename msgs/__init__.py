import logging
import sys
import tkinter as tk
from tkinter import messagebox as msg
import utils
from colorama import Fore, Style

def get_format(level):
    FORMATS = {
        logging.DEBUG: Fore.LIGHTGREEN_EX,
        logging.INFO: Fore.CYAN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.LIGHTRED_EX + Style.BRIGHT
    }
    col = FORMATS.get(level)
    format = f"[{col}%(levelname)s{Fore.RESET}{Style.RESET_ALL}]:%(name)s - %(message)s"
    return format

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = get_format(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def init():
    formatter = CustomFormatter()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.basicConfig(handlers=[handler])

init()

class Messages:
    def __init__(self, name:str):
        self.name = name
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)

    def error(self, title:str = None, message:str=None, as_event:bool=False, **options):
        from utils import eventManager
        self._logger.error(f"{title}: {message}")
        if as_event:
            def fcall(info:utils.EventInfo):
                msg.showerror(title, message=message,**options)
            eventManager.schedule(fcall)
        else:
            msg.showerror(title, message=message,**options)

    def warning(self, title:str = None, message:str = None, as_event:bool=False, **options):
        from utils import eventManager
        self._logger.warning(f"{title}: {message}")
        if as_event:
            def fcall(info:utils.EventInfo):
                msg.showwarning(title, message, **options)
            eventManager.schedule(fcall)
        else:
            msg.showwarning(title, message, **options)

    def info(self, message:str):
        self._logger.info(message)