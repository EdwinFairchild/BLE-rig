import serial
import time
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


def open_ports(interface, serial_port=None):
    if serial_port != None:
        interface.serial_port = serial.Serial(
            port=serial_port, baudrate=115200, timeout=0)
        # wait for port to be open
        while interface.serial_port.is_open != True:
            time.sleep(0.1)
        interface.ui.statusbar.showMessage(
            "Serial port connection established!")
        interface.uartConnectionActive = True
        interface.ui.actionConnect_BLE.setEnabled(False)
        interface.ui.actionConnect_Socket.setEnabled(False)


# --------------------------------------------------------------------------------------
'''
Closes instances of ope ports found in global dicitonary
This is only called once dudring test teardown
'''


def close_ports(interface):
    try:
        if isinstance(interface.serial_port, serial.Serial) == True:
            interface.serial_port.close()
            while interface.serial_port.is_open == True:
                time.sleep(0.1)
            interface.ui.statusbar.showMessage(
                "Serial Port Closed Succesfully!")

    except Exception as err:
        interface.ui.statusbar("Cannot close port.")


# --------------------------------------------------------------------------------------
'''
Can optioanlly send a string through serial port
and expect a string in return on  a single port
if timeout is exceeded the test is attempted once more
before failing.
'''


def uart_send_power_ctl(interface, send=None):

    if interface.serial_port.is_open == True:
        # flush junk
        interface.serial_port.reset_input_buffer()
        interface.serial_port.reset_output_buffer()
        # time.sleep(0.1)
        interface.serial_port.write(bytes("\n", encoding='utf-8'))
        # send data if any
        if send != None:
           # time.sleep(0.1)
            char_list = list(send)
            for char in char_list:
                # start test, send command
                interface.serial_port.write(bytes(char, encoding='utf-8'))
                time.sleep(0.001)
