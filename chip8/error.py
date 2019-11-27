# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chip8/error.ui',
# licensing of 'chip8/error.ui' applies.
#
# Created: Wed Nov 27 20:27:50 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ErrorWindow(object):
    def setupUi(self, ErrorWindow):
        ErrorWindow.setObjectName("ErrorWindow")
        ErrorWindow.resize(322, 142)
        ErrorWindow.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ErrorWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ErrorWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.continuePushButton = QtWidgets.QPushButton(ErrorWindow)
        self.continuePushButton.setObjectName("continuePushButton")
        self.horizontalLayout.addWidget(self.continuePushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.restartPushButton = QtWidgets.QPushButton(ErrorWindow)
        self.restartPushButton.setObjectName("restartPushButton")
        self.horizontalLayout.addWidget(self.restartPushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.exitPushButton = QtWidgets.QPushButton(ErrorWindow)
        self.exitPushButton.setDefault(True)
        self.exitPushButton.setObjectName("exitPushButton")
        self.horizontalLayout.addWidget(self.exitPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ErrorWindow)
        QtCore.QMetaObject.connectSlotsByName(ErrorWindow)

    def retranslateUi(self, ErrorWindow):
        ErrorWindow.setWindowTitle(QtWidgets.QApplication.translate("ErrorWindow", "Error", None, -1))
        self.continuePushButton.setText(QtWidgets.QApplication.translate("ErrorWindow", "Continue", None, -1))
        self.restartPushButton.setText(QtWidgets.QApplication.translate("ErrorWindow", "Restart", None, -1))
        self.exitPushButton.setText(QtWidgets.QApplication.translate("ErrorWindow", "Exit", None, -1))

