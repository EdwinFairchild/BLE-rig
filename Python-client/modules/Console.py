from main_app import *
from modules import Slots


interface = None


def console_init(main_interface):
    global interface
    pass
    interface = main_interface


def log(data):
    global interface
    print(data)
    #interface.ui.console.append("> " + str(data))
    # interface.ui.console.verticalScrollBar().setSliderPosition(10)


def log_status():
    global interface
    pass
   # log("Connected state: " + str(interface.connected_state))


def errMsg(data):
    log(str(data))
