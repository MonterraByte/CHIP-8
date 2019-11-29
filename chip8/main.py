# -*- coding: utf-8 -*-
#
# Copyright © 2019 Joaquim Monteiro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import pathlib
import sys

from PySide2 import QtCore, QtGui, QtWidgets

from .display import DISPLAY_WIDTH, DISPLAY_HEIGHT
from .emulator import Emulator
from .error import Ui_ErrorWindow
from .window import Ui_MainWindow

FRAME_INTERVAL = 166

parser = argparse.ArgumentParser(description="CHIP-8 emulator")
parser.add_argument("rom", help="Path to the ROM file", type=pathlib.Path, nargs="?")
parser.add_argument("--debug", help="Enable debug output", default=False, action="store_true")


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, args: argparse.Namespace):
        super().__init__(parent=None)
        self.setupUi(self)
        self.setCentralWidget(self.graphicsView)

        self.error_window = ErrorWindow(self)

        self.scale_factor = 1

        self.image = QtGui.QImage(QtCore.QSize(DISPLAY_WIDTH, DISPLAY_HEIGHT), QtGui.QImage.Format_Mono)
        self.image.fill(0)
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        self.graphicsScene = QtWidgets.QGraphicsScene(self)
        self.graphicsPixmapItem = self.graphicsScene.addPixmap(self.pixmap)
        self.graphicsView.setScene(self.graphicsScene)

        self.close_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtGui.QKeySequence.Quit), self)
        self.close_shortcut.activated.connect(self.close)
        self.actionPause.setShortcut(QtGui.QKeySequence.Print)  # Ctrl + P
        self.actionExit.triggered.connect(self.close)
        self.actionOpen.triggered.connect(self.open_rom)

        self.debug = args.debug

        self.keys = {i: False for i in range(16)}
        self.installEventFilter(self)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(FRAME_INTERVAL)

        self.emulator = None
        if args.rom:
            self.new_emulator(args.rom)
            self.timer.start()

        self.actionPause.toggled.connect(self.toggle_emulation)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        QtWidgets.QMainWindow.resizeEvent(self, event)

        self.scale_factor = min(self.graphicsView.width() // DISPLAY_WIDTH, self.graphicsView.height() // DISPLAY_HEIGHT)

    @QtCore.Slot()
    def draw(self):
        self.emulator.video_memory.draw(self.image)
        self.pixmap = QtGui.QPixmap.fromImage(self.image).scaled(QtCore.QSize(DISPLAY_WIDTH * self.scale_factor,
                                                                              DISPLAY_HEIGHT * self.scale_factor))
        self.graphicsPixmapItem.setPixmap(self.pixmap)

    def is_key_pressed(self, key: int) -> bool:
        return self.keys[key]


    @QtCore.Slot()
    def toggle_emulation(self, checked):
        if checked:
            self.timer.stop()
        else:
            self.timer.start()

    @QtCore.Slot()
    def open_rom(self):
        rom_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select ROM")
        if rom_path:
            self.new_emulator(pathlib.Path(rom_path))

    def new_emulator(self, rom_path: pathlib.Path):
        if self.emulator is not None:
            self.emulator.display_changed.disconnect()
            self.emulator.emulation_error.disconnect()
            self.timer.timeout.disconnect(self.emulator.run_once)

        with rom_path.open("rb") as fd:
            self.emulator = Emulator(fd.read(), self, self.debug)
        self.emulator.display_changed.connect(self.draw)
        self.emulator.emulation_error.connect(self.report_error)
        self.timer.timeout.connect(self.emulator.run_once)
        self.actionPause.setChecked(False)
        self.toggle_emulation(False)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.KeyPress or event.type() == QtCore.QEvent.KeyRelease:
            if event.key() == QtCore.Qt.Key_X:
                key = 0
            elif event.key() == QtCore.Qt.Key_1:
                key = 1
            elif event.key() == QtCore.Qt.Key_2:
                key = 2
            elif event.key() == QtCore.Qt.Key_3:
                key = 3
            elif event.key() == QtCore.Qt.Key_Q:
                key = 4
            elif event.key() == QtCore.Qt.Key_W:
                key = 5
            elif event.key() == QtCore.Qt.Key_E:
                key = 6
            elif event.key() == QtCore.Qt.Key_A:
                key = 7
            elif event.key() == QtCore.Qt.Key_S:
                key = 8
            elif event.key() == QtCore.Qt.Key_D:
                key = 9
            elif event.key() == QtCore.Qt.Key_Z:
                key = 10
            elif event.key() == QtCore.Qt.Key_C:
                key = 11
            elif event.key() == QtCore.Qt.Key_4:
                key = 12
            elif event.key() == QtCore.Qt.Key_R:
                key = 13
            elif event.key() == QtCore.Qt.Key_F:
                key = 14
            elif event.key() == QtCore.Qt.Key_V:
                key = 15
            else:
                return QtWidgets.QMainWindow.eventFilter(self, watched, event)

            self.keys[key] = event.type() == QtCore.QEvent.KeyPress
        else:
            return QtWidgets.QMainWindow.eventFilter(self, watched, event)

    @QtCore.Slot(Exception)
    def report_error(self, error: Exception):
        self.actionPause.setChecked(True)
        self.toggle_emulation(True)
        self.error_window.show_error(str(error))

    @QtCore.Slot()
    def error_reported(self):
        self.error_window.hide()
        self.actionPause.setChecked(False)
        self.toggle_emulation(False)

    @QtCore.Slot()
    def restart(self):
        import ctypes
        import os

        argc = ctypes.c_int()
        argv = ctypes.POINTER(ctypes.c_wchar_p)()
        ctypes.pythonapi.Py_GetArgcArgv(ctypes.byref(argc), ctypes.byref(argv))

        arguments = []
        for i in range(argc.value):
            arguments.append(argv[i])

        os.execv(sys.executable, arguments)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.error_window.close()
        QtWidgets.QMainWindow.closeEvent(self, event)


class ErrorWindow(QtWidgets.QDialog, Ui_ErrorWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.continuePushButton.clicked.connect(parent.error_reported)
        self.exitPushButton.clicked.connect(parent.close)
        self.restartPushButton.clicked.connect(parent.restart)

    def show_error(self, error: str):
        self.label.setText(error)
        self.show()


def main():
    args, unparsed_args = parser.parse_known_args()
    app = QtWidgets.QApplication(sys.argv[:1] + unparsed_args)
    window = Window(args)
    window.show()
    sys.exit(app.exec_())
