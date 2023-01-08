
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


def btn_connect(interface):

    # Establish and maintain Bleak connection
    if interface.connected_state == False:
        if interface.ble_rig_addr != None:
            try:
                # connection stuff
                interface.bleLoop = ble_ctl.BleakLoop()
                interface.bleLoop.disconnectSignal.connect(
                    lambda state: Slots.disconnect(interface, state))
                interface.bleLoop.ble_address = interface.ble_rig_addr
                interface.bleLoop.discoverServices = True
                interface.bleLoop.discovered_services.connect(
                    lambda data: Slots.discovered_services(interface, data))
                # interface.bleLoop.errorMsg.connect(
                #     lambda mesg: Slots.errMsg(interface, mesg))
                interface.connected_address = interface.bleLoop.ble_address
                interface.bleLoop.start()

            except Exception as err:
                Console.errMsg(err)
                MiscHelpers.set_connected_icon_color(interface, 'white')
                interface.ui.btnConnect.setText("Connect")
                interface.connected_state = False
        else:
            Console.log("You have to select a device from explore list")
    else:
        try:
            # connection stuff
            interface.bleLoop.disconnect_triggered = True

        except Exception as err:
            Console.errMsg(err)

    # ------------------------------------------------------------------------


def register_button_callbacks(interface):
    interface.ui.btn_connect.clicked.connect(
        lambda state: btn_connect(interface))
