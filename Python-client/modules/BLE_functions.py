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

'''******************************************************************************************
        Implements an infinite asyncio loop charged with registering
        notifications, read/write and signal emition of each event to
        GUI application
*******************************************************************************************'''


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

    power_setting = None

    def run(self):
        self.connect = True
        asyncio.run(self.bleakLoop())

    # -------------------------------------------------------------------------
    def handle_disconnect(self, _: BleakClient):
        # cancelling all tasks effectively ends the program
        self.disconnectSignal.emit(True)
        Console.log("Disconnected")
        # in case this happened because of a failed update

        # for task in asyncio.all_tasks():
        #     task.cancel()
    # -------------------------------------------------------------------------

    async def disconenctBLE(self, client: BleakClient):
        try:
            Console.log("Disconnect triggered...")
            await client.disconnect()
            # self.handle_disconnect(client)
            self.disconnect_triggered = False
            # self.connect = False
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
        ARM_Propietary_Data_Characteristic = "e0262760-08c2-11e1-9073-0e8ac72e0001"

        try:
            if self.power_setting == "ME17_MAIN":
                PACKET_TYPE = (0).to_bytes(1, byteorder='little', signed=False)
                ME14_STATE = (0).to_bytes(1, byteorder='little', signed=False)
                ME17_STATE = (0).to_bytes(1, byteorder='little', signed=False)
                ME17_MAIN_STATE = (1).to_bytes(
                    1, byteorder='little', signed=False)
                ME18_STATE = (0).to_bytes(1, byteorder='little', signed=False)
                ALL_ON = (0).to_bytes(1, byteorder='little', signed=False)
                ALL_OFF = (0).to_bytes(1, byteorder='little', signed=False)
                packet_to_send = PACKET_TYPE + ME14_STATE + ME17_STATE + \
                    ME17_MAIN_STATE + ME18_STATE + ALL_ON + ALL_OFF

            await client.write_gatt_char(ARM_Propietary_Data_Characteristic, bytearray(packet_to_send))

        except Exception as err:
            Console.errMsg(err)
        self.writeChar = False
    # -------------------------------------------------------------------------
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
