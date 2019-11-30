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

from PySide2.QtGui import QImage

DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 32


class VideoMemory(bytearray):
    def __init__(self):
        super().__init__(DISPLAY_WIDTH * DISPLAY_HEIGHT)

    def draw(self, image: QImage):
        for address, data in enumerate(self):
            x = address % DISPLAY_WIDTH
            y = address // DISPLAY_WIDTH
            if data:
                image.setPixel(x, y, 1)
            else:
                image.setPixel(x, y, 0)

    def draw_sprite(self, x, y, sprite):
        collision = False
        for line in range(len(sprite)):
            if y + line < DISPLAY_HEIGHT:
                for offset in range(8):
                    if x + offset < DISPLAY_WIDTH:
                        address = (DISPLAY_WIDTH * (y + line)) + x + offset
                        current_value = self[address]
                        new_value = ((sprite[line] & (0b10000000 >> offset)) >> 7 - offset)

                        if current_value and new_value:
                            collision = True
                            self[address] = 0
                        elif new_value:
                            self[address] = 1

        return collision

    def reset(self):
        self.__init__()

    def __str__(self):
        s = ""
        for address, data in enumerate(self):
            if address % DISPLAY_WIDTH == 0:
                s += "\n"

            if data:
                s += "█"
            else:
                s += "░"
        return s[1:]
