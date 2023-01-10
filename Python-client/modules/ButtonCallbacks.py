
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


def connect(interface):

    # Establish and maintain Bleak connection
    if interface.connected_state == False:
        
        try:
            # connection stuff
            interface.bleLoop = ble_ctl.BleakLoop()
            interface.PowerCtlFile_thread = ble_ctl.Power_Ctl_File()
            interface.PowerCtlFile_thread.bleLoop = interface.bleLoop
            interface.bleLoop.disconnectSignal.connect(lambda state: Slots.disconnect(interface, state))
            interface.bleLoop.ble_address = interface.ble_rig_addr
            interface.connected_address = interface.bleLoop.ble_address
            interface.bleLoop.start()
            interface.PowerCtlFile_thread.start()
            interface.connected_state = True
        except Exception as err:
            Console.errMsg(err)
            interface.connected_state = False
  
    else:
        try:
            # connection stuff
            interface.bleLoop.disconnect_triggered = True

        except Exception as err:
            Console.errMsg(err)
    # ------------------------------------------------------------------------


def btnMainMe17(interface):
    current_val = int.from_bytes(interface.bleLoop.ME17_MAIN_STATE, "little")
    if current_val == 1:
        interface.bleLoop.ME17_MAIN_STATE = (0).to_bytes(1, byteorder='little', signed=False)
    else:
        interface.bleLoop.ME17_MAIN_STATE = (1).to_bytes(1, byteorder='little', signed=False)
        interface.bleLoop.ALL_OFF = (0).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.writeChar = True
    # ------------------------------------------------------------------------


def btnMe17(interface):
    current_val = int.from_bytes(interface.bleLoop.ME17_STATE, "little")
    if current_val == 1:
        interface.bleLoop.ME17_STATE = (0).to_bytes(1, byteorder='little', signed=False)
    else:
        interface.bleLoop.ME17_STATE = (1).to_bytes(1, byteorder='little', signed=False)
        interface.bleLoop.ALL_OFF = (0).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.writeChar = True
    # ------------------------------------------------------------------------


def btnMe14(interface):
    current_val = int.from_bytes(interface.bleLoop.ME14_STATE, "little")
    if current_val == 1:
        interface.bleLoop.ME14_STATE = (0).to_bytes(1, byteorder='little', signed=False)
    else:
        interface.bleLoop.ME14_STATE = (1).to_bytes(1, byteorder='little', signed=False)
        interface.bleLoop.ALL_OFF = (0).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.writeChar = True

    # ------------------------------------------------------------------------


def btnMe18(interface):
    current_val = int.from_bytes(interface.bleLoop.ME18_STATE, "little")
    if current_val == 1:
        interface.bleLoop.ME18_STATE = (0).to_bytes(1, byteorder='little', signed=False)
    else:
        interface.bleLoop.ME18_STATE = (1).to_bytes(1, byteorder='little', signed=False)
        interface.bleLoop.ALL_OFF = (0).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.writeChar = True
    # ------------------------------------------------------------------------


def btnAllOn(interface):
    interface.bleLoop.ALL_OFF = (0).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.ALL_ON = (1).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.ME18_STATE = (1).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.ME14_STATE = (1).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.ME17_STATE = (1).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.ME17_MAIN_STATE = (1).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.writeChar = True
    # ------------------------------------------------------------------------


def btnAllOff(interface):
    interface.bleLoop.ALL_OFF = (1).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.ALL_ON = (0).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.ME18_STATE = (0).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.ME14_STATE = (0).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.ME17_STATE = (0).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.ME17_MAIN_STATE = (0).to_bytes(1, byteorder='little', signed=False)
    interface.bleLoop.writeChar = True

def register_button_callbacks(interface):
    # interface.ui.btn_connect.clicked.connect(
    #     lambda state: btn_connect(interface))
    interface.ui.btn_main_me17.clicked.connect(lambda state: btnMainMe17(interface))
    interface.ui.btn_me17.clicked.connect(lambda state: btnMe17(interface))
    interface.ui.btn_me14.clicked.connect(lambda state: btnMe14(interface))
    interface.ui.btn_me18.clicked.connect(lambda state: btnMe18(interface))
    interface.ui.btn_all_off.clicked.connect(lambda state: btnAllOff(interface))
    interface.ui.btn_all_on.clicked.connect(lambda state: btnAllOn(interface))
