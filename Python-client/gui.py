# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(711, 483)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btn_all_on = QtWidgets.QPushButton(self.centralwidget)
        self.btn_all_on.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.btn_all_on.setFont(font)
        self.btn_all_on.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btn_all_on.setObjectName("btn_all_on")
        self.verticalLayout_4.addWidget(self.btn_all_on)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_main_me17 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_main_me17.setMinimumSize(QtCore.QSize(0, 100))
        self.btn_main_me17.setMaximumSize(QtCore.QSize(99999, 99999))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.btn_main_me17.setFont(font)
        self.btn_main_me17.setStyleSheet("")
        self.btn_main_me17.setObjectName("btn_main_me17")
        self.verticalLayout.addWidget(self.btn_main_me17)
        self.btn_me17 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_me17.setMinimumSize(QtCore.QSize(0, 100))
        self.btn_me17.setMaximumSize(QtCore.QSize(99999, 99999))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.btn_me17.setFont(font)
        self.btn_me17.setStyleSheet("")
        self.btn_me17.setObjectName("btn_me17")
        self.verticalLayout.addWidget(self.btn_me17)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_me14 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_me14.setMinimumSize(QtCore.QSize(0, 100))
        self.btn_me14.setMaximumSize(QtCore.QSize(99999, 99999))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.btn_me14.setFont(font)
        self.btn_me14.setStyleSheet("")
        self.btn_me14.setObjectName("btn_me14")
        self.verticalLayout_2.addWidget(self.btn_me14)
        self.btn_me18 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_me18.setMinimumSize(QtCore.QSize(0, 100))
        self.btn_me18.setMaximumSize(QtCore.QSize(99999, 99999))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.btn_me18.setFont(font)
        self.btn_me18.setStyleSheet("")
        self.btn_me18.setObjectName("btn_me18")
        self.verticalLayout_2.addWidget(self.btn_me18)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.btn_all_off = QtWidgets.QPushButton(self.centralwidget)
        self.btn_all_off.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.btn_all_off.setFont(font)
        self.btn_all_off.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btn_all_off.setObjectName("btn_all_off")
        self.verticalLayout_4.addWidget(self.btn_all_off)
        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 711, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_all_on.setText(_translate("MainWindow", "All On"))
        self.btn_main_me17.setText(_translate("MainWindow", "ME17_Main"))
        self.btn_me17.setText(_translate("MainWindow", "ME17"))
        self.btn_me14.setText(_translate("MainWindow", "ME14"))
        self.btn_me18.setText(_translate("MainWindow", "ME18"))
        self.btn_all_off.setText(_translate("MainWindow", "All OFF"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
