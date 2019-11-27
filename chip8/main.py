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

from .window import Ui_MainWindow

parser = argparse.ArgumentParser(description="CHIP-8 emulator")
parser.add_argument("rom", help="Path to the ROM file", type=pathlib.Path)
parser.add_argument("--debug", help="Enable debug output", default=False, action="store_true")


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, args: argparse.Namespace):
        super().__init__(parent=None)
        self.setupUi(self)
        self.setCentralWidget(self.graphicsView)

        self.scale_factor = 1

        self.image = QtGui.QImage(QtCore.QSize(DISPLAY_WIDTH, DISPLAY_HEIGHT), QtGui.QImage.Format_Mono)
        self.image.fill(0)
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        self.graphicsScene = QtWidgets.QGraphicsScene(self)
        self.graphicsPixmapItem = self.graphicsScene.addPixmap(self.pixmap)
        self.graphicsView.setScene(self.graphicsScene)

        self.close_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtGui.QKeySequence.Quit), self)
        self.close_shortcut.activated.connect(self.close)
        self.actionExit.triggered.connect(self.close)
        self.actionOpen.triggered.connect(self.open_rom)

        self.debug = args.debug

        self.emulator = None
        self.new_emulator(args.rom)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        QtWidgets.QMainWindow.resizeEvent(self, event)

        self.scale_factor = min(self.graphicsView.width() // DISPLAY_WIDTH, self.graphicsView.height() // DISPLAY_HEIGHT)

    @QtCore.Slot()
    def draw(self):
        self.emulator.video_memory.draw(self.image)
        self.pixmap = QtGui.QPixmap.fromImage(self.image).scaled(QtCore.QSize(DISPLAY_WIDTH * self.scale_factor,
                                                                              DISPLAY_HEIGHT * self.scale_factor))
        self.graphicsPixmapItem.setPixmap(self.pixmap)

    @QtCore.Slot()
    def open_rom(self):
        rom_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select ROM")
        if rom_path:
            self.new_emulator(pathlib.Path(rom_path))

    def new_emulator(self, rom_path: pathlib.Path):
        if self.emulator is not None:
            self.emulator.display_changed.disconnect(self.draw)

        with rom_path.open("rb") as fd:
            self.emulator = Emulator(fd.read(), self.debug)
        self.emulator.display_changed.connect(self.draw)


def main():
    args, unparsed_args = parser.parse_known_args()
    app = QtWidgets.QApplication(sys.argv[:1] + unparsed_args)
    window = Window(args)
    window.show()
    sys.exit(app.exec_())
