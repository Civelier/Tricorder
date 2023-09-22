import os
from pathlib import Path
from enum import Enum
from time import sleep
from typing import Tuple
import cv2
from PIL import Image, ImageTk
import tkinter as tk

IMAGES_PATH="images"

class BtnStyle(Enum):
    Style1=1
    Style2=2
    Style3=3

class BtnShape(Enum):
    Play=1
    Pause=2
    Skip=3
    Prev=4
    Stop=5
    Rec=6
    Mic=7
    Headphones=8
    Music=9
    MusicNo=10
    SpeakerNo=11
    SpeakerLow=12
    SpeakerMed=13
    SpeakerHigh=14
    SpeakerMute=15
    Camera=16
    Picture=17
    Video=18
    ChartPie=19
    ChartBar=20
    ArrowLeft=21
    ArrowRight=22
    ArrowUp=23
    ArrowDown=24
    ArrowVertical=25
    ArrowHorizontal=26
    ArrowDiagonal=27
    ArrowCW=28
    Medal=29
    i=30
    ArrowHeadLeft=31
    ArrowHeadRight=32
    ArrowHeadUp=33
    ArrowHeadDown=34
    Plus=35
    Minus=36
    Multiply=37
    Check=38
    Star=39
    Heart=40
    ViewGrid=41
    ViewDetailed=42
    JustifyLeft=43
    JustifyCenter=44
    JustifyRight=45
    Justify=46
    Tags=47
    ZoomIn=48
    ZoomOut=49
    Zoom=50
    Locked=51
    Unlocked=52
    LockedCross=53
    LockedCheck=54
    UnlockedCheck=55
    Mail1=56
    Mail2=57
    MailData=58
    MailLoad=59
    MailAt=60
    MailHeart=61
    BubbleBig1=62
    BubbleBig2=63
    BubbleBigText=64
    BubbleBigWriting=65
    BubbleSmall=66
    BubbleSmallText=67
    BubbleSmallWriting=68
    Refresh1=69
    Refresh2=70
    Sliders=71
    Filter=72
    ViewHamburger=73
    Checklist=74
    Home=75
    Building=76
    Store=77
    Cog=78
    Share=79
    Trash=80
    Phone=81
    Web=82
    BatteryFull=83
    BatteryMid=84
    BatteryLow=85
    BatteryEmpty=86
    Profile1=87
    Profile2=88
    Location=89
    File=90
    Copy=90
    Paste=91
    Files=92
    Folder=93
    Write=94
    Shop=95
    Download=96
    Upload=97
    Map=98
    GeoPin=99
    Linked=100

class BtnColor(Enum):
    Pink=1
    Purple=2
    Blue=3
    Green=4
    Yellow=5
    Orange=6
    Red=7
    White=8
    LightGray=9
    Gray=10
    DarkGray=11
    Black=12

    
FG_COLORS = {
    BtnColor.Pink : 0xff92c2,
    BtnColor.Purple : 0x976ddb,
    BtnColor.Blue : 0x269fc7,
    BtnColor.Green : 0x1dd6a8,
    BtnColor.Yellow : 0xffcf27,
    BtnColor.Orange : 0xff9650,
    BtnColor.Red : 0xff7c7c,
    BtnColor.White : 0xd4d4d4,
    BtnColor.LightGray : 0xffffff,
    BtnColor.Gray : 0xd4d4d4,
    BtnColor.DarkGray : 0x929292,
    BtnColor.Black : 0x4e4e4e,
}

BG_COLORS = {
    BtnColor.Pink : 0xffd6e8,
    BtnColor.Purple : 0xceb0ff,
    BtnColor.Blue : 0x7adeff,
    BtnColor.Green : 0x8effe3,
    BtnColor.Yellow : 0xfff999,
    BtnColor.Orange : 0xffd6ab,
    BtnColor.Red : 0xffb0b0,
    BtnColor.White : 0xffffff,
    BtnColor.LightGray : 0xd4d4d4,
    BtnColor.Gray : 0x929292,
    BtnColor.DarkGray : 0x4e4e4e,
    BtnColor.Black : 0x000000,
}


class BtnInfo:
    def __init__(self, style:BtnStyle, shape:BtnShape, color:BtnColor):
        self.style = style
        self.shape = shape
        self.color = color

    @property
    def path(self):
        style = f"style{str(self.style.value).zfill(2)}"
        shape = f"shape{str(self.shape.value).zfill(3)}"
        color = f"color{str(self.color.value).zfill(2)}"
        return f"{IMAGES_PATH}/{style}/{shape}_{style}_{color}.png"

    def save_path(self, size:Tuple[int,int]):
        style = f"style{str(self.style.value).zfill(2)}"
        shape = f"shape{str(self.shape.value).zfill(3)}"
        color = f"color{str(self.color.value).zfill(2)}"
        return f"{IMAGES_PATH}/cache/{shape}_{style}_{color}_{size[0]}x{size[1]}.png"

    @property
    def fg_color(self):
        return FG_COLORS[self.color]

    @property
    def bg_color(self):
        return BG_COLORS[self.color]

    def with_size(self, size:Tuple[int,int]):
        img = Image.open(self.path)
        resized = img.resize(size)
        resized.save(self.save_path(size))
        return tk.PhotoImage(file=self.save_path(size))
