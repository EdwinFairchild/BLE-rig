
from PyQt5 import Qt as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QAbstractAnimation, QPoint, QEasingCurve, pyqtSignal, QSequentialAnimationGroup
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui import Ui_MainWindow
from modules import ButtonCallbacks
from modules import BLE_functions as ble_ctl
from modules import Console
from bleak import *
import asyncio
import platform
import sys
import os
import time
import atexit
from asyncqt import QEventLoop
import webbrowser

QtWidgets.QApplication.setAttribute(
    QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
os.environ["QT_FONT_DPI"] = "96"


class MainInterface(QMainWindow):

    bleLoop = None
    serialLoop = None
    connected_state = False
    ble_rig_addr = "00:18:80:30:88:FB"

    disconnectSignal = pyqtSignal(bool)
    

    def __init__(self):
        QMainWindow.__init__(self)
        # setup gui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.frm_otas.setVisible(False)
        # Console.console_init(self)
        # ListCallbacks.register_list_callbacks(self)
        ButtonCallbacks.register_button_callbacks(self)
        # MiscHelpers.init_icons(self)
        # Console.log("BLE-PyDex initialized")
        # Console.log_status()

    # ------------------------------------------------------------------------
    # def eventFilter(self, source, event):

    #     if event.type() == QtCore.QEvent.Enter and source == self.ui.sideBar:
    #         self.menuAnimate(self.ui.sideBar, True)
    #     if event.type() == QtCore.QEvent.Leave and source == self.ui.sideBar:
    #         self.menuAnimate(self.ui.sideBar, False)
    #     return super().eventFilter(source, event)
    # ------------------------------------------------------------------------

########################################################################################


def exitFunc():
    global interface
    try:
        interface.bleLoop.disconnect_triggered = True
        while interface.bleLoop.connect==True:
            pass
        #     print(interface.connected_state)
    except Exception as e:
        print(e)
    try:
        # close any on running tasks
        for task in asyncio.all_tasks():
            task.cancel()
    except Exception as e:
        pass


    # ------------------------------------------------------------------------
if __name__ == '__main__':
    # todo: compile resurces into python files, not sure if its even necessary at this point
    # pyrcc5 image.qrc -o image_rc.py
    # compile gui
    os.system("pyuic5 -x gui.ui -o gui.py")
    app = qtw.QApplication(sys.argv)
    app.setStyle('Fusion')

    # loop = QEventLoop(app)
    # asyncio.set_event_loop(loop)

    interface = MainInterface()
    interface.show()
    ButtonCallbacks.connect(interface)
    atexit.register(exitFunc)

    app.exec_()
