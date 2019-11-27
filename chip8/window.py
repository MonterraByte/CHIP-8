# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chip8/window.ui',
# licensing of 'chip8/window.ui' applies.
#
# Created: Wed Nov 27 14:35:31 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAcceptDrops(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.graphicsView = QtWidgets.QGraphicsView(MainWindow)
        self.graphicsView.setAcceptDrops(False)
        self.graphicsView.setObjectName("graphicsView")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEmulation = QtWidgets.QMenu(self.menubar)
        self.menuEmulation.setObjectName("menuEmulation")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionPause = QtWidgets.QAction(MainWindow)
        self.actionPause.setCheckable(True)
        self.actionPause.setObjectName("actionPause")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menuEmulation.addAction(self.actionPause)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEmulation.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "CHIP-8", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menuEmulation.setTitle(QtWidgets.QApplication.translate("MainWindow", "Emulation", None, -1))
        self.actionOpen.setText(QtWidgets.QApplication.translate("MainWindow", "Open...", None, -1))
        self.actionExit.setText(QtWidgets.QApplication.translate("MainWindow", "Exit", None, -1))
        self.actionPause.setText(QtWidgets.QApplication.translate("MainWindow", "Pause", None, -1))

