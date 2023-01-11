from modules import Console

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
    "me17_main":[],
    "me14":[],
    "me17":[],
    "me18":[]
}

text_color = [0, 0, 0]
on_background = [170, 200, 255]
off_background= [255, 255, 255]

def disconnect(interface, state):
    
    interface.bleLoop.exit()
    interface.connected_state = False
    print("interface set to")

def set_device_power_settings(interface, device,state):
    global devices, text_color, on_background, off_background
    # update power state variable
    devices[device][2] = state
    #update power control file
    file = open('power_ctl.log', 'r')
    lines = file.readlines()
    lines[devices[device][1]] = f"{state}\n"
    with open('power_ctl.log', 'w') as file:
        file.writelines( lines )
    #update button stylesheet
    if state == True:
        set_alternate_button_mode_color(interface, devices[device][0], text_color, on_background)
    else:
        set_alternate_button_mode_color(interface, devices[device][0], text_color, off_background)

    # notfiy ble-loop    
    interface.bleLoop.writeChar = True
    



def set_alternate_button_mode_color(interface, button, fore, back):
    stylesheet = f"QPushButton{{ text-align: center; background-color: rgb({back[0]}, {back[1]}, {back[2]});  ;border-radius:5px;color: rgb({fore[0]}, {fore[1]}, {fore[2]});border:none;}}QPushButton:hover{{color: rgb(255, 255, 255);background-color: rgb(170, 77, 77);}}QPushButton:pressed{{color: rgb(255, 255, 255);background-color: rgb(170, 27, 27);}}"
    button.setStyleSheet(stylesheet)