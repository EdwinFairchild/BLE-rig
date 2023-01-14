from modules import Console
from modules import BLE_functions as ble_ctl
from modules import serialReader
from main_app import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import asyncio

# items in device list:
# Index         Descript
#   0           Button Object
#   1           Location in control file
#   2           Power state
devices = {
    "me17_main": [],
    "me14": [],
    "me17": [],
    "me18": []
}

text_color = [0, 0, 0]
on_background = [170, 200, 255]
off_background = [255, 255, 255]


def disconnect(interface, state):

    interface.bleLoop.exit()
    interface.PowerCtlFile_thread.exit()
    interface.connected_state = False


def set_device_power_settings(interface, device, state):
    global devices, text_color, on_background, off_background
    # update power state variable
    devices[device][2] = state
    # update power control file
    file = open('power_ctl.log', 'r')
    lines = file.readlines()
    lines[devices[device][1]] = f"{state}\n"
    with open('power_ctl.log', 'w') as file:
        file.writelines(lines)
    # update button stylesheet
    if state == True:
        set_alternate_button_mode_color(
            interface, devices[device][0], text_color, on_background)
    else:
        set_alternate_button_mode_color(
            interface, devices[device][0], text_color, off_background)

    # trigger connection events
    if interface.bleConnectionActive == True:
        # notfiy ble-loop
        interface.bleLoop.writeChar = True

    if interface.uartConnectionActive == True:
        # change from "me17_main" to "me17main"
        serialReader.uart_send_power_ctl(
            interface, f"{device.replace('_', '')} {int(state)}\n")

    if interface.socketConnectionActive == True:
        pass


def connect_BLE(interface):
    # Establish and maintain Bleak connection
    interface.ui.statusbar.showMessage(
        "Attempting to establish BLE connection")
    if interface.connected_state == False:
        try:
            # connection stuff
            interface.bleLoop = ble_ctl.BleakLoop()
            interface.PowerCtlFile_thread = ble_ctl.Power_Ctl_File()
            interface.PowerCtlFile_thread.bleLoop = interface.bleLoop
            interface.PowerCtlFile_thread.interface = interface
            interface.bleLoop.disconnectSignal.connect(
                lambda state: Slots.disconnect(interface, state))
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


def connect_UART(interface):
    interface.ui.statusbar.showMessage(
        "Attempting to establish UART connection")


def connect_Socket(interface):
    interface.ui.statusbar.showMessage("Listening to socket connection")


def set_alternate_button_mode_color(interface, button, fore, back):
    stylesheet = f"QPushButton{{ text-align: center; background-color: rgb({back[0]}, {back[1]}, {back[2]});  ;border-radius:5px;color: rgb({fore[0]}, {fore[1]}, {fore[2]});border:none;}}QPushButton:hover{{color: rgb(255, 255, 255);background-color: rgb(170, 77, 77);}}QPushButton:pressed{{color: rgb(255, 255, 255);background-color: rgb(170, 27, 27);}}"
    button.setStyleSheet(stylesheet)


def connectUART():
    print("Connect uart")
