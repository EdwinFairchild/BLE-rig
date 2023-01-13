
from main_app import *
from modules import Slots
from modules import Console
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import zlib
import sys
import time

BUFFER_SIZE = 8192
fileLen = 0

on_fore = [0, 0, 0]
on_back = [170, 200, 255]
off_fore = [0, 0, 0]
off_back = [255, 255, 255]

def get_crc32():
    global fileLen
    with open("max32655.bin", 'rb') as f:
        crc = 0
        fileLen = 0
        while True:
            data = f.read(BUFFER_SIZE)
            fileLen += len(data)
            if not data:
                break
            crc = zlib.crc32(data, crc)
    return crc
# ------------------------------------------------------------------------


def btnMainMe17(interface):
    state = not Slots.devices["me17_main"][2]
    Slots.set_device_power_settings(interface,"me17_main",state)
    
    # ------------------------------------------------------------------------


def btnMe17(interface):
    state = not Slots.devices["me17"][2]
    Slots.set_device_power_settings(interface,"me17",state)
    # ------------------------------------------------------------------------


def btnMe14(interface):
    state = not Slots.devices["me14"][2]
    Slots.set_device_power_settings(interface,"me14",state)

    # ------------------------------------------------------------------------


def btnMe18(interface):
    state = not Slots.devices["me18"][2]
    Slots.set_device_power_settings(interface,"me18",state)
    # ------------------------------------------------------------------------


def btnAllOn(interface):
    pass
    # ------------------------------------------------------------------------


def btnAllOff(interface):
    pass

def register_button_callbacks(interface):
    # interface.ui.btn_connect.clicked.connect(
    #     lambda state: btn_connect(interface))
    interface.ui.btn_main_me17.clicked.connect(lambda state: btnMainMe17(interface))
    interface.ui.btn_me17.clicked.connect(lambda state: btnMe17(interface))
    interface.ui.btn_me14.clicked.connect(lambda state: btnMe14(interface))
    interface.ui.btn_me18.clicked.connect(lambda state: btnMe18(interface))
    interface.ui.btn_all_off.clicked.connect(lambda state: btnAllOff(interface))
    interface.ui.btn_all_on.clicked.connect(lambda state: btnAllOn(interface))
