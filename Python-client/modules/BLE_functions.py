import bleak as ble
from bleak import BleakScanner
from bleak import *
import asyncio
import platform
import sys
import os
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from enum import Enum, auto
from typing import Any, Callable, NamedTuple
from functools import cached_property
from modules import Console
from modules import Slots
import zlib  # used for crc32
BUFFER_SIZE = 8192
fileLen = 0


'''******************************************************************************************
        Scan for devices
*******************************************************************************************'''
'''        
        //uint32_t crc32
        packet_t packet_type;
        power_state_t me14_state;
        power_state_t me17_state;
        power_state_t me17_main_state;
        power_state_t me18_state;
        bool all_on;
        bool all_off;
'''
'''******************************************************************************************
        Implements an infinite asyncio loop charged with registering
        notifications, read/write and signal emition of each event to
        GUI application
*******************************************************************************************'''
class Power_Ctl_File(QThread):
    bleLoop= None
        #TODO : make buttons also update the file and update the previous value so it does not trigger a
        # state change twice
    prevME18 = "0"
    interface = None
    def run(self):
        while self.bleLoop.connect==True:
            self.read_power_ctl()
            QThread.msleep(250)
            

    def read_power_ctl(self):

        file1 = open('power_ctl.log', 'r')
        Lines = file1.readlines()
        count = 0
        # Strips the newline character
        for line in Lines:
            if count == 1:
                if self.prevME18 != line.strip():
                    print(f"Value changed to {line.strip()}")
                    self.prevME18 = line.strip()
                    if line.strip() == "True":
                        Slots.set_device_power_settings(self.interface,"me14",True)     
                    else:
                        Slots.set_device_power_settings(self.interface,"me14",False)
                    self.bleLoop.writeChar = True

   
            count += 1

class BleakLoop(QThread):
    # bleak client stuff
    ble_address = None
    # client = None
    # disconnected state switch
    disconnectSignal = pyqtSignal(bool)
    connect = False
    disconnect_triggered = False

    # used to trigger write char
    writeChar = False

    def run(self):
        self.connect = True
        asyncio.run(self.bleakLoop())

    # -------------------------------------------------------------------------
    def handle_disconnect(self, _: BleakClient):
        # cancelling all tasks effectively ends the program
        #Not working
        Console.log("Disconnected")
        self.connect = False
        self.disconnectSignal.emit(True)
         # atempt connection again
    # -------------------------------------------------------------------------

    async def disconenctBLE(self, client: BleakClient):
        try:
            Console.log("Disconnect triggered...")
            await client.disconnect()
            # self.handle_disconnect(client)
            self.disconnect_triggered = False
            self.disconnectSignal.emit(True)
        except Exception as err:
            Console.errMsg(err)

    # -------------------------------------------------------------------------
    def get_crc32(self, fileName):
        global fileLen
        Console.log("opening file " + str(fileName))
        with open(fileName, 'rb') as f:
            crc = 0
            fileLen = 0
            while True:
                data = f.read(BUFFER_SIZE)
                fileLen += len(data)
                if not data:
                    break
                crc = zlib.crc32(data, crc)
        return crc
    # -------------------------------------------------------------------------

    async def writeCharCallback(self, client: BleakClient):
        """
        uint32_t crc32
        packet_t packet_type;
        power_state_t me14_state;
        power_state_t me17_state;
        power_state_t me17_main_state;
        power_state_t me18_state;
        bool all_on;
        bool all_off;

        """
        #power state index in the Slots.devices dictionary
        power_state_index = 2
        # the char. the device is expecting settings on

        # TODO implement crc32
        
        ARM_Propietary_Data_Characteristic = "e0262760-08c2-11e1-9073-0e8ac72e0001"
        ME17_MAIN_STATE = (int(Slots.devices['me17_main'][power_state_index])).to_bytes(1, byteorder='little', signed=False)
        PACKET_TYPE = (0).to_bytes(1, byteorder='little', signed=False)
        ME14_STATE = (int(Slots.devices['me14'][power_state_index])).to_bytes(1, byteorder='little', signed=False)
        ME17_STATE = (int(Slots.devices['me17'][power_state_index])).to_bytes(1, byteorder='little', signed=False)
        ME18_STATE = (int(Slots.devices['me18'][power_state_index])).to_bytes(1, byteorder='little', signed=False)
        ALL_ON = (0).to_bytes(1, byteorder='little', signed=False)
        ALL_OFF = (0).to_bytes(1, byteorder='little', signed=False)

        try:
            
            packet_to_send = PACKET_TYPE + ME14_STATE + ME17_STATE + \
                ME17_MAIN_STATE + ME18_STATE + ALL_ON + ALL_OFF

            await client.write_gatt_char(ARM_Propietary_Data_Characteristic, bytearray(packet_to_send))

        except Exception as err:
            Console.errMsg(err)
        self.writeChar = False
    # -------------------------------------------------------------------------

    async def bleakLoop(self):
        device = await BleakScanner.find_device_by_filter(
            lambda d, ad: d.name and d.name.lower() == "brig"
        )
        async with BleakClient(device, disconnected_callback=self.handle_disconnect) as client:
            while self.connect == True:
                await asyncio.sleep(0.005)
                # check the flag to disconnect
                if self.disconnect_triggered == True:
                    await self.disconenctBLE(client)
                # -------------- if a single char needs to be read
                if self.writeChar == True:
                    await self.writeCharCallback(client)
