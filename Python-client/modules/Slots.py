from modules import Console

from main_app import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import asyncio


def discovered_services(interface, data):
    pass


def got_char_notify(interface, data):
    # since char handle and data received are 2 seprate lists in the gui
    # the data parameter here will have a "sender" and the data recevied
    # so we look for the same sender in the handles list and get the row nubmer
    # then in the corresponding row for the data recevied we add the new data
    # I over complicated this
    pass
    # string = str(data[0]).split()[2][:-2]
    # item = interface.ui.list_EnabledNotify.findItems(string, QtCore.Qt.MatchExactly)
    # row = interface.ui.list_EnabledNotify.row(item[0])
    # item = interface.ui.list_EnabledNotifyValue.item(row)
    # data = str(data[1]).removeprefix("bytearray(b\'\\")
    # data = str(data).removesuffix("\')")
    # item.setText(data)
    # Console.log("Received : " + data)


def notify_registered_state(interface, state):
    pass
    # if state == True:
    #     # add the selected UUID/Handle to the notify list
    #     if interface.ui.btnLabelHandle.text() in interface.notifyEnabledCharsDict:
    #         Console.log("Characteristic notificaiton is already enabled")
    #     else:
    #         interface.notifyEnabledCharsDict[interface.ui.btnLabelHandle.text(
    #         )] = "N/A"
    #         interface.ui.list_EnabledNotify.addItem(
    #             interface.ui.btnLabelHandle.text())
    #         interface.ui.list_EnabledNotifyValue.addItem("N/A")
    #         # interface.notifyEnabledCharsDict[interface.ui.btnLabelHandle.text()] += ["5555"]
    #         # print(str(interface.notifyEnabledCharsDict[interface.ui.btnLabelHandle.text()][1]))
    #         # call function to add this item to list_enabledNotifybtnNoti
    # else:
    #     Console.log("Could not add")


def disconnect(interface, state):
    if state == True:
        interface.bleLoop.exit()
    pass
    # gui stuff
    #     fore = [0, 0, 0]
    #     back = [170, 200, 255]
    #     MiscHelpers.set_alternate_button_mode_color(
    #         interface, interface.ui.btnConnect, fore, back)
    #     MiscHelpers.set_connected_icon_color(interface, 'white')
    #     interface.ui.btnConnect.setText("Connect")
    #     interface.connected_state = False
    #     # clean up tree wdiget stuff
    #     interface.ui.servicesTreeWidget.clear()
    #     interface.ui.list_EnabledNotify.clear()
    #     interface.ui.list_discoveredDevices.clear()
    #     interface.ui.list_EnabledNotifyValue.clear()
    #     interface.notifyEnabledCharsDict = {}
    #     if interface.advertised_name == "OTAS":
    #         interface.ui.frm_otas.setVisible(False)
    #         interface.bleLoop.otas_progress_value.emit(0)

    # else:

    #     fore = [255, 255, 255]
    #     back = [170, 66, 66]
    #     MiscHelpers.set_alternate_button_mode_color(
    #     interface, interface.ui.btnConnect, fore, back)
    #     # gui stuff
    #     MiscHelpers.set_connected_icon_color(interface, 'blue')
    #     interface.ui.btnConnect.setText("Disconnect")
    #     interface.connected_state = True
    #     if interface.advertised_name == "OTAS":
    #         interface.ui.frm_otas.setVisible(True)
    #         interface.bleLoop.otas_progress_value.connect(
    #                 lambda value: otas_progress_update(interface, value))


def read_char(interface, data):
    pass


def scan(interface, device):
    pass
    # #interface.ui.list_discoveredDevices.addItem(f" " + device[0][0:17] + " | " + device[0][18:] + " ")
    # interface.ui.list_discoveredDevices.addItem(f" " + str(device[0]))
    # # device[1] has rssi


def serial_data(interface, data):
    pass
    # interface.ui.txtSerial.append(data.strip())


def serial_connected(interface, state):
    pass
    # if state == True:
    #     fore = [255, 255, 255]
    #     back = [170, 66, 66]
    #     MiscHelpers.set_alternate_button_mode_color(
    #         interface, interface.ui.btnSerialConnect, fore, back)
    #     interface.ui.btnSerialConnect.setText("Disconnect")
    #     interface.serial_connected_state = True
    # else:
    #     interface.serialLoop.quit()
    #     fore = [0, 0, 0]
    #     back = [170, 200, 255]
    #     MiscHelpers.set_alternate_button_mode_color(
    #         interface, interface.ui.btnSerialConnect, fore, back)
    #     interface.ui.btnSerialConnect.setText("Connect")
    #     interface.serial_connected_state = False


def otas_progress_update(interface, value):
    pass
    # interface.ui.otasProgress.setValue(value)
