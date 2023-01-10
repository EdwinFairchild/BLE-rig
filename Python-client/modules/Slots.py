from modules import Console

from main_app import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import asyncio



def disconnect(interface, state):
    
    interface.bleLoop.exit()
    interface.connected_state = False
    print("interface set to")